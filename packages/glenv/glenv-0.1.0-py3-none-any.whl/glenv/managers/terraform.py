from glenv.types.variable import GitlabVariable
from glenv.managers.base import FileManager
from glenv.types.formats import TerraformFile


class TerraformManager(FileManager):
    __file_format__ = TerraformFile

    @staticmethod
    def _line_to_variable(line: str) -> GitlabVariable:
        key, value = line.strip().split("=", maxsplit=1)
        key = f"TF_VAR_{key}" if not key.startswith("TF_VAR") else key

        return GitlabVariable(key.strip(), value.strip().replace('"', ""))

    @staticmethod
    def _variable_to_line(var: GitlabVariable) -> str:
        return f'{var.key.replace("TF_VAR_", "")} = "{var.value}"\n'
