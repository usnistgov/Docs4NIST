import github_action_utils as gha_utils
import pathlib
import re

from .file import File


class SphinxLog(File):
    def __init__(self, docs, path):
        self.docs = docs
        self._path = pathlib.Path(path)

    @property
    def path(self):
        return self._path

    def parse_sphinx_warnings(self):
        """Parse and emit a sphinx file containing warnings and errors.

        Inputs look like this:
            /media/sf_shared/workspace/sphinx-action/tests/test_projects/warnings_and_errors/index.rst:19: WARNING: Error in "code-block" directive:
            maximum 1 argument(s) allowed, 2 supplied.

            /cpython/Doc/distutils/_setuptools_disclaimer.rst: WARNING: document isn't included in any toctree
            /cpython/Doc/contents.rst:5: WARNING: toctree contains reference to nonexisting document 'ayylmao'
        """
        with self.path.open(mode='r') as f:
            logs = f.readlines()
            
        prog_lineno = re.compile("(?P<FILE>.*)(?::(?P<LINE>[0-9]+))+?: (?P<TYPE>WARNING|ERROR): (?P<MESSAGE>.*)")
        prog_nolineno = re.compile("(?P<FILE>.*): (?P<TYPE>WARNING|ERROR): (?P<MESSAGE>.*)")
        
        replacements = []
        if has_attr(self.docs, "original_docs"):
            replacements.append([self.docs.docs_dir.as_posix(),
                                 self.original_docs.docs_dir.as_posix()])

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
            message = m["MESSAGE"]

            for old, new in replacements:
                message = message.replace(old, new)

            if m["TYPE"] == "WARNING":
                msg_fn = gha_utils.warning
            if m["TYPE"] == "ERROR":
                msg_fn = gha_utils.error

            msg_fn(message, file=file_name, line=line_number, use_subprocess=True)

            # If this isn't the last line and the next line isn't a warning,
            # treat it as part of this warning message.
            for subsequent in logs[i:]:
                if prog_nolineno.match(subsequent):
                    break
                else:
                    msg_fn(subsequent.strip(), file=file_name, line=line_number, use_subprocess=True)
