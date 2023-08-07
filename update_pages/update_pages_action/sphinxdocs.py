#!/usr/bin/env python3
import github_action_utils as gha_utils
import pathlib
import subprocess

from .files import ConfFile


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

    def install_requirements(self):
        """Install any packages needed for Sphinx.

        Adapted from https://github.com/ammaraskar/sphinx-action/blob/master/sphinx_action/action.py#LL102C1-L105C1
        [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html)
        """
        docs_requirements = self.docs_dir / "requirements.txt"
        if docs_requirements.is_file():
            gha_utils.debug(f"pip installing")
            subprocess.check_call(["pip", "install", "-r", docs_requirements.as_posix()])
