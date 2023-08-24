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
