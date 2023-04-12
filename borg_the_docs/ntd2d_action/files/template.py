import pathlib

class Template:
    def __init__(self, name):
        # look in templates/ directory adjacent to this file
        dir = pathlib.Path(__file__).parent
        self.template_path = dir / "templates" / name

    def read(self):
        with open(self.template_path, mode='r') as template_file:
            template = template_file.read()

        return template

class PagesTemplate(Template):
    def __init__(self, working_dir, name):
        # look in _templates/ directory of nist-pages branch
        self.template_path = working_dir / "_templates" / name
        if not self.template_path.exists():
            super().__init__(name=name)

    def read(self):
        with open(self.template_path, mode='r') as template_file:
            template = template_file.read()

        return template

class IFrame(PagesTemplate):
    def __init__(self, working_dir):
        super().__init__(working_dir=working_dir, name="iframe.html")
