#!/usr/bin/env python3
"""Sphinx configuration directory.
"""
__docformat__ = 'restructuredtext'

import github_action_utils as gha_utils
import importlib
import os
import pathlib
import shlex
import shutil
from sphinx.application import Sphinx
from sphinx.theming import HTMLThemeFactory
import subprocess
import sys
import tempfile
import traceback

from .files import ConfFile
from .files import SphinxLog, BorgedConfFile, TemplateHierarchy
from .files.template import FileTemplate


class SphinxDocs:
    """Sphinx configuration directory."""

    def __init__(self, docs_dir):
        self._app = None
        self.docs_dir = pathlib.Path(docs_dir)

        if (self.docs_dir / "source" / "conf.py").is_file():
            self.source_dir = self.docs_dir / "source"
            self.build_dir = self.docs_dir / "build"
        else:
            self.source_dir = self.docs_dir
            self.build_dir = self.docs_dir / "_build"

        self.conf = self.make_conf_file()

    def make_conf_file(self):
        return ConfFile(source_dir=self.source_dir,
                        config=self.sphinx_app.config)

    @property
    def sphinx_app(self):
        if self._app is None:
            self._app = Sphinx(srcdir=self.source_dir,
                               confdir=self.source_dir,
                               outdir=self.build_dir,
                               doctreedir=self.build_dir / "doctrees",
                               buildername="html")
        return self._app

    @property
    def html_dir(self):
        return self.build_dir / "html"

    @property
    def epub_file(self):
        return self.build_dir / "epub" / f"{self.conf.project}.epub"

    @property
    def pdf_file(self):
        return self.build_dir / "latex" / f"{self.conf.project.lower()}.pdf"

    def get_theme(self, theme_name):
        theme_factory = HTMLThemeFactory(self.sphinx_app)
        return theme_factory.create(theme_name)

    @property
    def stylesheet(self):
        theme = self.get_theme(self.sphinx_app.config.html_theme)

        return theme.get_config("theme", "stylesheet")

    def build_docs(self, build_command):
        """Build Sphinx Documentation

        Adapted from https://github.com/ammaraskar/sphinx-action/blob/master/sphinx_action/action.py
        (`Apache-2.0 <https://spdx.org/licenses/Apache-2.0.html>`_).
        """
        if not build_command:
            raise ValueError("Build command may not be empty")

        return_code = 0

        with tempfile.TemporaryDirectory() as tmpdirname:
            log_file = pathlib.Path(tmpdirname) / "sphinx-log"
            log_file.unlink(missing_ok=True)

            sphinx_options = f'--keep-going --no-color -w "{log_file}"'
            # If we're using make, pass the options as part of the SPHINXOPTS
            # environment variable, otherwise pass them straight into the command.
            build_command = shlex.split(build_command)

            if build_command[0] == "make":
                # Pass the -e option into `make`, this is specified to be
                #   Cause environment variables, including those with null values, to override macro assignments within makefiles.
                # which is exactly what we want.
                build_command += ["-e"]
                gha_utils.echo(f"[sphinx-action] Running: {build_command}",
                               use_subprocess=True)

                subprocess.run(
                    build_command,
                    env=dict(os.environ, SPHINXOPTS=sphinx_options),
                    cwd=self.docs_dir.as_posix(),
                    bufsize=1,
                    text=True,
                    check=True
                )
            else:
                build_command += shlex.split(sphinx_options)
                gha_utils.echo(f"[sphinx-action] Running: {build_command}",
                               use_subprocess=True)

                subprocess.run(
                    build_command,
                    cwd=self.docs_dir.as_posix(),
                    bufsize=1,
                    text=True,
                    check=True
                )

            if log_file.exists():
                log = SphinxLog(docs=self, path=log_file)
                log.parse_sphinx_warnings()

        return return_code


class BorgedSphinxDocs(SphinxDocs):
    """Sphinx configuration directory modified by Docs4NIST

    Parameters
    ----------
    original_docs : ~ntd2d_action.sphinxdocs.SphinxDocs
        The configuration directory stored in the
        :class:`~ntd2d_action.repository.Repository`.
    """

    def __init__(self, original_docs):
        self.original_docs = original_docs
        borged_docs_dir = self.original_docs.docs_dir.as_posix() + "-BORGED"
        borged_docs_dir = pathlib.Path(borged_docs_dir)
        shutil.copytree(self.original_docs.docs_dir, borged_docs_dir)
        super().__init__(docs_dir=borged_docs_dir)

    def make_conf_file(self):
        return BorgedConfFile(source_dir=self.source_dir,
                              config=self.sphinx_app.config,
                              original_docs=self.original_docs)

    @property
    def inherited_theme(self):
        return self.original_docs.conf.html_theme

    @property
    def inherited_layout(self):
        """Find inherited layout.html

        Inherited theme may not define its own :file:`layout.html`, but
        rely on a theme that it, in turn, derives from.
        `{% extends "!layout.html" %}` should work, but doesn't.
        https://github.com/sphinx-doc/sphinx/issues/12049
        """
        def get_theme_layout(theme):
            # Handle both old and new Sphinx theme implementations
            theme_dir = None
            
            # Try different ways to get the theme directory
            if hasattr(theme, 'themedir'):
                theme_dir = theme.themedir
            elif hasattr(theme, '_template_dir'):
                theme_dir = theme._template_dir
            elif hasattr(theme, 'get_theme_dir'):
                theme_dir = theme.get_theme_dir()
            elif hasattr(theme, 'dirs'):
                # Some themes store their files in a 'dirs' list
                theme_dir = theme.dirs[0] if theme.dirs else None
                
            if theme_dir is None:
                # If we can't find the theme directory, try to get it from the module
                try:
                    theme_module = __import__(theme.name.replace("-", "_"), fromlist=[''])
                    theme_dir = os.path.dirname(os.path.abspath(theme_module.__file__))
                except ImportError:
                    # If all else fails, try to construct a path from the theme name
                    theme_dir = os.path.join(self.conf.theme_path, theme.name)

            layout_path = pathlib.Path(theme_dir) / "layout.html"
            
            if layout_path.exists():
                return f"{theme.name}/layout.html"
            elif hasattr(theme, 'base') and theme.base is not None:
                return get_theme_layout(theme.base)
            else:
                # If we can't find a layout, return a basic one
                return "basic/layout.html"

        return get_theme_layout(self.get_theme(self.inherited_theme))

    def assimilate_theme(self, name, insert_header_footer=True):
        """Replace configuration directory with customized html theme."""

        if insert_header_footer:
            header_footer = FileTemplate(name="header_footer_script.html").read()
        else:
            header_footer = ""

        self.theme = TemplateHierarchy(name=name,
                                       destination_dir=self.conf.theme_path,
                                       inherited_theme=self.inherited_theme,
                                       inherited_layout=self.inherited_layout,
                                       inherited_css=self.stylesheet,
                                       header_footer_script=header_footer)
        self.theme.write()

        self.conf.set_html_theme(name=name)
        self.conf.write()
