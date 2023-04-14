import pathlib

from .file import File
from .template import FileTemplate


class ConfFile(File):
    def __init__(self, docs_dir):
        self.docs_dir = pathlib.Path(docs_dir)

    @property
    def path(self):
        return self.docs_dir / "conf.py"

    def read(self):
        # The Sphinx docs says that it
        # [reads conf.py with `importlib.import_module`](https://www.sphinx-doc.org/en/master/usage/configuration.html#module-conf)
        # [It doesn't](https://github.com/sphinx-doc/sphinx/blob/2c83af0aab7080e0b78d4a16981eed878b2cac4c/sphinx/config.py#L353).
        namespace = {}
        namespace['__file__'] = self.path.as_posix()

        with self.path.open(mode='rb') as f:
            code = compile(f.read(), self.path, 'exec')
            exec(code, namespace)  # NoQA: S102

        return namespace

    def write(self):
        suffix = FileTemplate(name="conf_suffix.py")

        with self.path.open(mode='a') as f:
            f.write(suffix.read())
