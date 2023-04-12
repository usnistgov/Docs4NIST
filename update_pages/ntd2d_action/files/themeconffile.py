from .file import File
from .template import Template


class ThemeConfFile(File):
    def __init__(self, inherited_theme, path):
        self.inherited_theme = inherited_theme
        super().__init__(path=path)

    def get_contents(self):
        conf_template = Template(name="theme.conf").read()

        return conf_template.format(inherited_theme=self.inherited_theme)
