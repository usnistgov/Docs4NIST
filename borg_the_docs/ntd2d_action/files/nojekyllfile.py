from .file import File


class NoJekyllFile(File):
    # jekyll conflicts with sphinx' underlined directories and files
    def __init__(self, repo):
        super().__init__(repo=repo,
                         path=repo.working_dir / ".nojekyll")
