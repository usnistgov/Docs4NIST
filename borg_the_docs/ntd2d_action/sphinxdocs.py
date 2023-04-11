import pathlib
# 
class SphinxDocs:
    def __init__(self, docs_dir):
        self.docs_dir = pathlib.Path(docs_dir)

    @property
    def html_dir(self):
        return self.docs_dir / "_build" / "html"
