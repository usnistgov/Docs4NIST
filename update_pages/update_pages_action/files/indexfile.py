import textwrap

from .pagesfile import PagesFile
from .template import PagesTemplate


class IndexFile(PagesFile):
    def __init__(self, repo, variants_url):
        self.variants_url = variants_url
        super().__init__(repo=repo)

    @property
    def path(self):
        return self.repo.working_dir / "index.html"

    def get_contents(self):
        """build index.html with available documentation variants
        """
        variants = self.format_iframe(src=self.variants_url)
        variants = textwrap.indent(versions, "    ")

        index_template = PagesTemplate(working_dir=self.repo.working_dir,
                                       name="index.html").read()
        return index_template.format(variants=variants,
                                     owner=self.repo.owner,
                                     repository=self.repo.repository)
