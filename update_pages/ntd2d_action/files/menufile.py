import textwrap

from .pagesfile import PagesFile
from .template import PagesTemplate


class MenuFile(PagesFile):
    def __init__(self, variant, variants_url):
        self.variant = variant
        self.variants_url = variants_url
        super().__init__(repo=variant.repo)

    @property
    def path(self):
        return (self.repo.working_dir / "html" / self.variant.name
                / "_static" / "ntd2d_menu.html")

    def get_contents(self):
        variants = self.format_iframe(src=self.variants_url)

        if len(self.variant.downloads) > 0:
            tmpl = PagesTemplate(working_dir=self.repo.working_dir,
                                 name="downloads.html").read()
            downloads = tmpl.format(downloads=self.variant.get_downloads_html())
        else:
            downloads = ""

        menu_template = PagesTemplate(working_dir=self.repo.working_dir,
                                      name="menu.html").read()
        return menu_template.format(variants=textwrap.indent(variants, "    "),
                                    branch=self.variant.name,
                                    downloads=textwrap.indent(downloads, "    "))
