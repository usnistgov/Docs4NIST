from .file import File


class HiddenFile(File):
    # Add a file that indicates docs should not be included in variant menu
    
    def __init__(self, html_dir):
        self.html_dir = html_dir

    @property
    def path(self):
        return self.html_dir / ".hidden"
