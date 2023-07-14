import github_action_utils as gha_utils
import textwrap

from .pagesfile import PagesFile

class CSSFile(PagesFile):
    def __init__(self, variant, variants_url):
        self.variant = variant
        self.variants_url = variants_url
        super().__init__(repo=variant.repo)

    @property
    def path(self):
        return (self.repo.working_dir / "html" / self.variant.name
                / "_static" / "ntd2d.css")

    def get_contents(self):
        gha_utils.debug(f"CSSFile.get_contents()")

        contents += textwrap.dedent(f"""
        
        .ntd2d_{self.variant.name} li a {{
          font-style: bold
        }}
        """)

        gha_utils.debug(f"contents = {contents}")

        return contents

    def write(self):
        with self.path.open(mode='a') as file:
            file.write(self.get_contents())
