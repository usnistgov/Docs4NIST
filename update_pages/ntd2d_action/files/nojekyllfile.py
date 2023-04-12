from .pagesfile import PagesFile


class NoJekyllFile(PagesFile):
    # jekyll conflicts with sphinx' underlined directories and files

    @property
    def path(self):
        return self.repo.working_dir / ".nojekyll"
