import contextlib
import github_action_utils as gha_utils
import pathlib
import shutil

from .conffile import ConfFile
from .template import FileTemplate
from .templatehierarchy import TemplateHierarchy


class BorgedConfFile(ConfFile):
    def __init__(self, docs_dir, source_rel=""):
        self.original_docs_dir = pathlib.Path(docs_dir)
        borged_docs_dir = self.original_docs_dir.as_posix() + "-BORGED"
        borged_docs_dir = pathlib.Path(borged_docs_dir)
        shutil.copytree(self.original_docs_dir, borged_docs_dir)
        super().__init__(docs_dir=borged_docs_dir, source_rel=source_rel)

    @property
    def exclude_patterns(self):
        exclude_patterns = super().exclude_patterns

        return exclude_patterns + [self.original_docs_dir.as_posix()]

    @property
    def inherited_theme(self):
        return self.configuration.get("html_theme", "default")

    def assimilate_theme(self, name):
        configuration = self.read()

        self.theme = TemplateHierarchy(name=name,
                                       destination_dir=self.theme_path,
                                       inherited_theme=self.inherited_theme)
        self.theme.write()

    def get_contents(self):
        conf_template = FileTemplate(name="conf.py").read()

        return conf_template.format(original_contents=super().get_contents(),
                                    html_theme=self.theme.name,
                                    html_theme_path=self.html_theme_path,
                                    exclude_patterns=self.exclude_patterns)
