import textwrap

from .file import File
from .template import Template


class MenuFile(File):
    def __init__(self, repo, current_branch, variants_url):
        self.current_branch = current_branch
        self.variants_url = variants_url
        path = (repo.working_dir / "html" / current_branch
                / "_static" / "ntd2d_menu.html")
        super().__init__(repo=repo,
                         path=path)

    def get_contents(self):
        versions = self.format_iframe(src=self.variants_url)

        menu_template = Template(working_dir=self.repo.working_dir,
                                 name="menu.html").read()
        return menu_template.format(versions=textwrap.indent(versions, "    "),
                                    branch=self.current_branch)
