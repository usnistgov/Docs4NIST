from .file import File
from .template import IFrame


class PagesFile(File):
    def __init__(self, repo, path):
        super().__init__(path=path)
        self.repo = repo

    def format_iframe(self, src):
        iframe_template = IFrame(working_dir=self.repo.working_dir).read()
        return iframe_template.format(src=src)

    def write(self):
        super().write()
        self.repo.add(self.path)
