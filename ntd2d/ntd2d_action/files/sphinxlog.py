import pathlib
import re

from .file import File


class SphinxLog(File):
    def __init__(self, path):
        self._path = pathlib.Path(path)

    @property
    def path(self):
        return self._path

    def parse_sphinx_warnings():
        """Parses a sphinx file containing warnings and errors into a list of
        status_check.CheckAnnotation objects.

        Inputs look like this:
            /media/sf_shared/workspace/sphinx-action/tests/test_projects/warnings_and_errors/index.rst:19: WARNING: Error in "code-block" directive:
            maximum 1 argument(s) allowed, 2 supplied.

            /cpython/Doc/distutils/_setuptools_disclaimer.rst: WARNING: document isn't included in any toctree
            /cpython/Doc/contents.rst:5: WARNING: toctree contains reference to nonexisting document 'ayylmao'
        """
        with self.path.open(mode='r') as f:
            logs = f.readlines()
            
        prog_lineno = re.compile("(?P<FILE>.*)(?::(?P<LINE>[0-9]+))+?: WARNING: (?P<MESSAGE>.*)")
        prog_nolineno = re.compile("(?P<FILE>.*): WARNING: (?P<MESSAGE>.*)")
        
        for i, line in enumerate(logs):
            m = prog_lineno.match(line)
            if m is None:
                m = prog_nolineno.match(line)
                if m is None:
                    continue
                else:
                    line_number = None
            else:
                line_number = m["LINE"]

            file_name = m["FILE"]
            warning_message = m["MESSAGE"]

            gha_utils.warning(warning_message, file=file_name, line=line_number)

            # If this isn't the last line and the next line isn't a warning,
            # treat it as part of this warning message.
            for subsequent in logs[i:]:
                if "WARNING" in subsequent:
                    break
                else:
                    gha_utils.warning(subsequent.strip(), file=file_name, line=line_number)
        