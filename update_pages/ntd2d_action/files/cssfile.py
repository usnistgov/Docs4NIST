import textwrap

from .themefile import ThemeFile
from .template import Template


class CSSFile(ThemeFile):

    @property
    def path(self):
        return self.theme_dir / "static" / "ntd2d.css_t"

    def get_contents(self):
        contents = f'@import url("{self.inherited_theme}.css");\n\n'

        return contents + Template(name="ntd2d.css_t").read()
