from .template import IFrame


class File:
    def __init__(self, repo, path):
        self.repo = repo
        self.path = path

    def format_iframe(self, src):
        iframe_template = IFrame(working_dir=self.repo.working_dir).read()
        return iframe_template.format(src=src)

    def get_contents(self):
        return ""

    def write(self):
        self.path.parent.mkdir(exist_ok=True)
        with self.path.open(mode='w') as file:
            file.write(self.get_contents())
        self.repo.add(self.path)
