from .file import File

class ThemeFile(File):
    def __init__(self, docs_dir, inherited_theme):
        self.docs_dir = docs_dir
        self.theme_dir = self.docs_dir / "ntd2d"
        self.inherited_theme = inherited_theme
        super().__init__(path=self.make_path())

    def make_path(self):
        pass

    def get_contents(self):
        conf_template = Template(name="theme.conf").read()

        return conf_template.format(inherited_theme=self.inherited_theme)
