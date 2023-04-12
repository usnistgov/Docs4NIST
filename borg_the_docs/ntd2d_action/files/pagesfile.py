from .file import File
from .template import IFrame


class PagesFile(File):
    def __init__(self, repo):
        self.repo = repo
        super().__init__()

    def format_iframe(self, src):
        iframe_template = IFrame(working_dir=self.repo.working_dir).read()
        return iframe_template.format(src=src)

    def write(self):
        super().write()
        self.repo.add(self.path)
