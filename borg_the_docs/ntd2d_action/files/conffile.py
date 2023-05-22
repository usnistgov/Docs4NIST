import contextlib
import os
import pathlib

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

    @property
    def path(self):
        return self.docs_dir / "conf.py"

    @property
    def theme_path(self):
        return self.docs_dir / "_themes"

    def read(self):
        # The Sphinx docs says that it
        # [reads conf.py with `importlib.import_module`](https://www.sphinx-doc.org/en/master/usage/configuration.html#module-conf)
        # [It doesn't](https://github.com/sphinx-doc/sphinx/blob/2c83af0aab7080e0b78d4a16981eed878b2cac4c/sphinx/config.py#L353).
        namespace = {}
        namespace['__file__'] = self.path.as_posix()

        with self.path.open(mode='rb') as f:
            code = compile(f.read(), self.path, 'exec')

            with working_directory(self.docs_dir):
                exec(code, namespace)  # NoQA: S102

        return namespace

    def assimilate_theme(self, name):
        configuration = self.read()

        inherited_theme = configuration.get("html_theme", "default")
        self.html_theme_path = configuration.get("html_theme_path", [])

        relative_theme_path = self.theme_path.relative_to(self.docs_dir)
        if relative_theme_path not in self.html_theme_path:
            self.html_theme_path.append(relative_theme_path)

        self.theme = TemplateHierarchy(name=name,
                                       destination_dir=self.theme_path,
                                       inherited_theme=inherited_theme)
        self.theme.write()

    def get_contents(self):
        with self.path.open(mode='r') as f:
            original_contents = f.read()

        conf_template = FileTemplate(name="conf.py").read()

        return conf_template.format(original_contents=original_contents,
                                    html_theme=self.theme.name,
                                    html_theme_path=self.html_theme_path)