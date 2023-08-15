import contextlib

class File:
    def __init__(self):
        pass

    @property
    def path(self):
        raise NotImplementedError

    def get_contents(self):
        return ""

    # By [Lukas](https://stackoverflow.com/users/911441/lukas)
    # [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)
    # https://stackoverflow.com/a/42441759/2019542
    @contextlib.contextmanager
    @staticmethod
    def working_directory(path):
        """Changes working directory and returns to previous on exit."""
        prev_cwd = pathlib.Path.cwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(prev_cwd)

    def write(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open(mode='w') as file:
            file.write(self.get_contents())
