import pathlib
import textwrap
from urllib.parse import urlparse

class Template:
    def __init__(self, working_dir, name):
        # look in _templates/ directory of nist-pages branch
        self.template_path = working_dir / "_templates" / name
        if not self.template_path.exists():
            # look in templates/ directory adjacent to this file
            dir = pathlib.Path(__file__).parent
            self.template_path = dir / "templates" / name

    def read(self):
        with open(self.template_path, mode='r') as template_file:
            template = template_file.read()

        return template

class IFrame(Template):
    def __init__(self, working_dir):
        super().__init__(working_dir=working_dir, name="iframe.html")

class File:
    def __init__(self, repo, path):
        self.repo = repo
        self.path = path

    def format_iframe(self, src):
        iframe_template = IFrame(working_dir=self.repo.working_dir).read()
        return iframe_template.format(src=src)

    def get_contents(self):
        return ""

    def write(self):
        self.path.parent.mkdir(exist_ok=True)
        with self.path.open(mode='w') as file:
            file.write(self.get_contents())
        self.repo.add(self.path)

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

class NoJekyllFile(File):
    # jekyll conflicts with sphinx' underlined directories and files
    def __init__(self, repo):
        super().__init__(repo=repo,
                         path=repo.working_dir / ".nojekyll")

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
