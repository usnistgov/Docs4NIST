#!/usr/bin/env python3
import pathlib

from .files import ConfFile, TemplateHierarchy


class SphinxDocs:
    def __init__(self, docs_dir):
        self.docs_dir = pathlib.Path(docs_dir)

    @property
    def html_dir(self):
        return self.docs_dir / "_build" / "html"

    def assimilate_theme(self):
        conf = ConfFile(docs_dir=self.docs_dir)
        configuration = conf.read()

        inherited_theme = configuration.get("html_theme", "default")

        templates = TemplateHierarchy(name="ntd2d",
                                      destination_dir=self.docs_dir,
                                      inherited_theme=inherited_theme)
        templates.write()

        conf.write()

def main():
    docs = SphinxDocs(docs_dir=os.environ['INPUT_DOCS-FOLDER'])

    docs.assimilate_theme()

if __name__ == "__main__":
    main()
