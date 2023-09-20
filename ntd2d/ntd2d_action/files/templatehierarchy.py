import github_action_utils as gha_utils
import pathlib

from .template import FileTemplate, Template


class TemplateHierarchy(FileTemplate):
    def __init__(self, name, destination_dir, **substitutions):
        super().__init__(name=name)
        self.destination_dir = pathlib.Path(destination_dir)
        self.substitutions = substitutions

    def write(self):
        for template_path in self.template_path.rglob("*"):
            if (template_path.is_dir()
                or (template_path.name in [".DS_Store"])):
                continue
                
            template = Template(template_path=template_path).read()

            relative_path = template_path.relative_to(self.template_dir)
            destination_path = self.destination_dir / relative_path
            destination_path.parent.mkdir(parents=True, exist_ok=True)

            with destination_path.open(mode='w') as destination:
                destination.write(template.format(**self.substitutions))
            gha_utils.echo(f"wrote {destination_path.as_posix()}", use_subprocess=True)
