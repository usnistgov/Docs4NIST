#!/usr/bin/env python3
import pathlib


class SphinxDocs:
    def __init__(self, docs_dir, build_rel):
        self.docs_dir = pathlib.Path(docs_dir)
        self.build_dir = self.docs_dir / build_rel

    @property
    def html_dir(self):
        return self.build_dir / "html"
