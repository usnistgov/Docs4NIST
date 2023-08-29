from .pagesfile import PagesFile


class NoJekyllFile(PagesFile):
    # jekyll conflicts with sphinx' underlined directories and files
    # https://github.blog/2009-12-29-bypassing-jekyll-on-github-pages/

    @property
    def path(self):
        return self.repo.working_dir / ".nojekyll"
