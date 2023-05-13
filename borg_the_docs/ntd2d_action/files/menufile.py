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
        versions = self.format_iframe(src=self.variants_url)

        menu_template = PagesTemplate(working_dir=self.repo.working_dir,
                                      name="menu.html").read()
        return menu_template.format(versions=textwrap.indent(versions, "    "),
                                    branch=self.variant.name)
