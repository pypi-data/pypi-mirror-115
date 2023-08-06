from glenv.types.variable import GitlabVariable
from glenv.managers.base import FileManager
from glenv.types.formats import DotEnvFile


class DotEnvManager(FileManager):
    __file_format__ = DotEnvFile

    @staticmethod
    def _line_to_variable(line: str) -> GitlabVariable:
        return GitlabVariable(*line.strip().split("=", maxsplit=1))

    @staticmethod
    def _variable_to_line(var: GitlabVariable) -> str:
        return f"{var.key}={var.value}\n"
