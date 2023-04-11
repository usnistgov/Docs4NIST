import textwrap

from .file import File
from .template import Template


class IndexFile(File):
    def __init__(self, repo, variants_url):
        self.variants_url = variants_url
        super().__init__(repo=repo,
                         path=repo.working_dir / "index.html")

    def get_contents(self):
        """build index.html with available documentation versions
        """
        versions = self.format_iframe(src=self.variants_url)
        versions = textwrap.indent(versions, "    ")

        index_template = Template(working_dir=self.repo.working_dir,
                                  name="index.html").read()
        return index_template.format(versions=versions,
                                     repository=self.repo.repository)
