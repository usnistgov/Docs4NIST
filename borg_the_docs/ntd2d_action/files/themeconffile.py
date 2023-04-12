from .themefile import ThemeFile
from .template import Template


class ThemeConfFile(ThemeFile):
    def make_path(self):
        return self.theme_dir / "theme.conf"

    def get_contents(self):
        conf_template = Template(name="theme.conf").read()

        return conf_template.format(inherited_theme=self.inherited_theme)
