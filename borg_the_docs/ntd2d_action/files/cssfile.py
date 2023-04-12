import textwrap

from .file import File
from .template import Template


class CSSFile(File):
    def __init__(self, inherited_theme, path):
        self.inherited_theme = inherited_theme
        super().__init__(path=path)

    def get_contents(self):
        contents = f'@import url("{self.inherited_theme}.css");\n\n'

        return contents + Template(name="ntd2d.css_t").read()
