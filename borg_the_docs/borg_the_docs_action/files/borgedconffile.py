from .conffile import ConfFile
from .template import FileTemplate


class BorgedConfFile(ConfFile):
    """Sphinx configuration file that overlays the html theme."""

    def __init__(self, source_dir, original_docs):
        self.original_docs = original_docs
        super().__init__(source_dir=source_dir)

    @property
    def exclude_patterns(self):
        exclude_patterns = super().exclude_patterns

        return exclude_patterns + [self.original_docs.docs_dir.as_posix()]

    @property
    def html_theme_path(self):
        html_theme_path = self.original_docs.conf.html_theme_path.copy()

        relative_path = self.theme_path.relative_to(self.source_dir).as_posix()
        if relative_path not in html_theme_path:
            html_theme_path.append(relative_path)

        return html_theme_path

    def get_contents(self):
        conf_template = FileTemplate(name="conf.py").read()

        return conf_template.format(original_contents=super().get_contents(),
                                    html_theme=self.theme.name,
                                    html_theme_path=self.html_theme_path,
                                    exclude_patterns=self.exclude_patterns)
