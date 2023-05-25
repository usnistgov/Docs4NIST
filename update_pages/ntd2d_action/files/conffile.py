import contextlib
import github_action_utils as gha_utils
import os
import pathlib
import shutil

from .file import File
from .template import FileTemplate
from .templatehierarchy import TemplateHierarchy

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
    def __init__(self, docs_dir):
        self.docs_dir = pathlib.Path(docs_dir)
        self.theme = None
        self._code = None
        self._configuration = None

    @property
    def configuration(self):
        if self._configuration is None:
            self._configuration = self.read()
        return self._configuration

    @property
    def inherited_theme(self):
        return self.configuration.get("html_theme", "default")

    @property
    def html_theme_path(self):
        return self.configuration.get("html_theme_path", [])

    @property
    def exclude_patterns(self):
        return configuration.get("exclude_patterns", [])

    @property
    def path(self):
        return self.docs_dir / "conf.py"

    @property
    def theme_path(self):
        return self.docs_dir / "_themes"

    @property
    def original_contents(self):
        if self._code is None:
            with self.path.open(mode='r') as f:
                self._code = f.read()

        return self._code

    def read(self):
        # The Sphinx docs says that it
        # [reads conf.py with `importlib.import_module`](https://www.sphinx-doc.org/en/master/usage/configuration.html#module-conf)
        # [It doesn't](https://github.com/sphinx-doc/sphinx/blob/2c83af0aab7080e0b78d4a16981eed878b2cac4c/sphinx/config.py#L353).
        namespace = {}
        namespace['__file__'] = self.path.as_posix()

        code = compile(self.original_contents, self.path, 'exec')

        with working_directory(self.docs_dir):
            exec(code, namespace)  # NoQA: S102

        return namespace

    def assimilate_theme(self, name):
        configuration = self.read()

        relative_path = self.theme_path.relative_to(self.docs_dir).as_posix()
        if relative_path not in self.html_theme_path:
            self.html_theme_path.append(relative_path)

        self.theme = TemplateHierarchy(name=name,
                                       destination_dir=self.theme_path,
                                       inherited_theme=self.inherited_theme)
        self.theme.write()

    def get_contents(self):
        conf_template = FileTemplate(name="conf.py").read()

        return conf_template.format(original_contents=self.original_contents,
                                    html_theme=self.theme.name,
                                    html_theme_path=self.html_theme_path,
                                    exclude_patterns=self.exclude_patterns)

class ClonedConfFile(ConfFile):
    def __init__(self, docs_dir):
        self.original_docs_dir = pathlib.Path(docs_dir)
        borged_docs_dir = self.original_docs_dir.as_posix() + "-BORGED"
        shutil.copytree(self.original_docs_dir, borged_docs_dir)
        super().__init__(docs_dir=borged_docs_dir)

    @property
    def exclude_patterns(self):
        exclude_patterns = super().exclude_patterns

        return exclude_patterns + [self.original_docs_dir]
