#!/usr/bin/env python3
"""Sphinx configuration directory.
"""
__docformat__ = 'restructuredtext'

import github_action_utils as gha_utils
import os
import pathlib
import shlex
import shutil
import subprocess
import tempfile

from .files import ConfFile
from .files import SphinxLog, BorgedConfFile, TemplateHierarchy


class SphinxDocs:
    """Sphinx configuration directory."""

    def __init__(self, docs_dir):
        self.docs_dir = pathlib.Path(docs_dir)

        if (self.docs_dir / "source" / "conf.py").is_file():
            self.source_dir = self.docs_dir / "source"
            self.build_dir = self.docs_dir / "build"
        else:
            self.source_dir = self.docs_dir
            self.build_dir = self.docs_dir / "_build"

        self.conf = self.make_conf_file()

    def make_conf_file(self):
        return ConfFile(source_dir=self.source_dir)

    @property
    def html_dir(self):
        return self.build_dir / "html"

    @property
    def epub_file(self):
        return self.build_dir / "epub" / f"{self.conf.project}.epub"

    @property
    def pdf_file(self):
        return self.build_dir / "latex" / f"{self.conf.project.lower()}.pdf"

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
                print(f"[sphinx-action] Running: {build_command}")

                subprocess.check_output(
                    build_command,
                    env=dict(os.environ, SPHINXOPTS=sphinx_options),
                    cwd=self.docs_dir.as_posix(),
                    stderr=subprocess.STDOUT
                )
            else:
                build_command += shlex.split(sphinx_options)
                print(f"[sphinx-action] Running: {build_command}")

                subprocess.check_output(
                    build_command,
                    cwd=self.docs_dir.as_posix(),
                    stderr=subprocess.STDOUT
                )

            if log_file.exists():
                log = SphinxLog(docs=self, path=log_file)
                log.parse_sphinx_warnings()

        return return_code


class BorgedSphinxDocs(SphinxDocs):
    """Sphinx configuration directory modified by NISTtheDocs2Death.

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
                              original_docs=self.original_docs)

    @property
    def inherited_theme(self):
        return self.original_docs.conf.html_theme

    def assimilate_theme(self, name):
        """Replace configuration directory with customized html theme."""

        self.theme = TemplateHierarchy(name=name,
                                       destination_dir=self.conf.theme_path,
                                       inherited_theme=self.inherited_theme)
        self.theme.write()

        self.conf.set_html_theme(name=name)
        self.conf.write()
