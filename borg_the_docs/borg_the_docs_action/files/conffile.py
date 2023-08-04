import contextlib
import github_action_utils as gha_utils
import os
import pathlib

from .file import File


# By [Lukas](https://stackoverflow.com/users/911441/lukas)
# [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)
# https://stackoverflow.com/a/42441759/2019542
@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = pathlib.Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)

class ConfFile(File):
    """Sphinx configuration file."""

    def __init__(self, docs_dir, source_rel=""):
        self.docs_dir = pathlib.Path(docs_dir)
        self.source_dir = self.docs_dir / source_rel
        self.theme = None
        self._code = None
        self._configuration = None

    @property
    def configuration(self):
        """Text of configuration file."""

        if self._configuration is None:
            self._configuration = self.read()
        return self._configuration

    @property
    def html_theme_path(self):
        html_theme_path = self.configuration.get("html_theme_path", [])

        relative_path = self.theme_path.relative_to(self.source_dir).as_posix()
        if relative_path not in html_theme_path:
            html_theme_path.append(relative_path)

        return html_theme_path

    @property
    def exclude_patterns(self):
        return self.configuration.get("exclude_patterns", [])

    @property
    def original_contents(self):
        if self._code is None:
            with self.path.open(mode='r') as f:
                self._code = f.read()

        return self._code

    @property
    def path(self):
        return self.source_dir / "conf.py"

    @property
    def project(self):
        return self.configuration["project"]

    @property
    def theme_path(self):
        return self.source_dir / "_themes"

    def read(self):
        # The Sphinx docs says that it
        # [reads conf.py with `importlib.import_module`](https://www.sphinx-doc.org/en/master/usage/configuration.html#module-conf)
        # [It doesn't](https://github.com/sphinx-doc/sphinx/blob/2c83af0aab7080e0b78d4a16981eed878b2cac4c/sphinx/config.py#L353).
        namespace = {}
        namespace['__file__'] = self.path.as_posix()

        code = compile(self.original_contents, self.path, 'exec')

        with working_directory(self.source_dir):
            exec(code, namespace)  # NoQA: S102

        return namespace

    def get_contents(self):
        return self.original_contents
