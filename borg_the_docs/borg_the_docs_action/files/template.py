import pathlib

class Template:
    def __init__(self, template_path):
        self.template_path = template_path

    def read(self):
        with open(self.template_path, mode='r') as template_file:
            template = template_file.read()

        return template

class FileTemplate(Template):
    def __init__(self, name):
        self.name = name
        # look in templates/ directory adjacent to this file
        self.template_dir = pathlib.Path(__file__).parent / "templates"
        super().__init__(template_path=self.template_dir / name)

class PagesTemplate(FileTemplate):
    def __init__(self, working_dir, name):
        # look in _templates/ directory of nist-pages branch
        self.template_path = working_dir / "_templates" / name
        if not self.template_path.exists():
            super().__init__(name=name)
