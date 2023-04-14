import importlib
import pathlib
import textwrap

import os

from .files import FileTemplate, TemplateHierarchy


class SphinxDocs:
    def __init__(self, docs_dir):
        self.docs_dir = pathlib.Path(docs_dir)
        self.conf_file = self.docs_dir / "conf.py"

    @property
    def html_dir(self):
        return self.docs_dir / "_build" / "html"

    def read_conf(self):
        # The Sphinx docs says that it
        # [reads conf.py with `importlib.import_module`](https://www.sphinx-doc.org/en/master/usage/configuration.html#module-conf)
        # [It doesn't](https://github.com/sphinx-doc/sphinx/blob/2c83af0aab7080e0b78d4a16981eed878b2cac4c/sphinx/config.py#L353).
        namespace = {}
        namespace['__file__'] = self.conf_file.as_posix()

        with self.conf_file.open(mode='rb') as f:
            code = compile(f.read(), self.conf_file, 'exec')
            exec(code, namespace)  # NoQA: S102

        return namespace

    def inject_theme(self):
        conf = self.read_conf()
        inherited_theme = conf.get("html_theme", "default")

        templates = TemplateHierarchy(name="ntd2d",
                                      destination_dir=self.docs_dir,
                                      inherited_theme=inherited_theme)
        templates.write()

        suffix = FileTemplate(name="conf_suffix.py")

        with self.conf_file.open(mode='a') as f:
            f.write(suffix.read())
