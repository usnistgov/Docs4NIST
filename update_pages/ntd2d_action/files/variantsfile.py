import textwrap
from urllib.parse import urlparse

from .pagesfile import PagesFile
from .template import PagesTemplate


class VariantsFile(PagesFile):
    def __init__(self, repo, variants, pages_url):
        self.variants = variants
        self.pages_url = pages_url
        super().__init__(repo=repo)

    @property
    def path(self):
        return self.repo.working_dir / self.relative_path

    @property
    def relative_path(self):
        return "_includes/ntd2d_variants.html"

    def get_url(self):
        full_url = "/".join([self.pages_url,
                             self.repo.repository,
                             self.relative_path])

        return urlparse(full_url)

    def get_contents(self):
        def _indent(text):
            return textwrap.indent(text, "    ")

        variants = _indent(self.variants.get_html())
        versions = _indent(self.variants.get_versions_html())
        branches = _indent(self.variants.get_branches_html())
        latest = _indent(self.variants.get_latest_html())
        stable = _indent(self.variants.get_stable_html())

        variants_template = PagesTemplate(working_dir=self.repo.working_dir,
                                          name="variants.html").read()
        return variants_template.format(variants=variants,
                                        versions=versions,
                                        branches=branches,
                                        latest=latest,
                                        stable=stable)
