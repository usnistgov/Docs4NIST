#!/usr/bin/env python3
import pathlib


class SphinxDocs:
    def __init__(self, docs_dir):
        self.docs_dir = pathlib.Path(docs_dir)
        self.build_dir = self.docs_dir / self.build_rel

        self.conf = ConfFile(docs_dir=docs_dir, source_rel=self.source_rel)

    @property
    def html_dir(self):
        return self.build_dir / "html"

    @property
    def epub_file(self):
        return self.build_dir / "epub" / f"{self.conf.project}.epub"

    @property
    def pdf_file(self):
        return self.build_dir / "latex" / f"{self.conf.project.tolower()}.pdf"

class SeparatedSphinxDocs(SphinxDocs):
    build_rel = "build"
    source_rel = "source"

class UnifiedSphinxDocs(SphinxDocs):
    build_rel = "_build"
    source_rel = ""
