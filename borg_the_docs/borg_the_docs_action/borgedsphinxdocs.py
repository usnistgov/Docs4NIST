import pathlib
import shutil

from .sphinxdocs import SphinxDocs
from .files import BorgedConfFile, TemplateHierarchy


class BorgedSphinxDocs(SphinxDocs):
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
                                       destination_dir=self.theme_path,
                                       inherited_theme=self.inherited_theme)
        self.theme.write()
        
        self.conf.write()
