import textwrap
from urllib.parse import urlparse

from .file import File
from .template import Template


class VariantsFile(File):
    def __init__(self, repo, variants, pages_url):
        self.variants = variants
        self.pages_url = pages_url
        self.relative_path = "_includes/ntd2d_variants.html"
        path = repo.working_dir / self.relative_path
        super().__init__(repo=repo, path=path)

    def get_url(self):
        full_url = "/".join([self.pages_url,
                             self.repo.repository,
                             self.relative_path])

        return urlparse(full_url)

    def get_contents(self):
        variants = self.variants.get_variants_html()
        variants = textwrap.indent("\n".join(variants), "  ")

        variants_template = Template(working_dir=self.repo.working_dir,
                                     name="variants.html").read()
        return variants_template.format(variants=variants)
