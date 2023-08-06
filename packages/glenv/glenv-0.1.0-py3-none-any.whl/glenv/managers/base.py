import abc
from glenv.types.variable import GitlabVariable
from glenv.managers.exceptions import InvalidFile
from glenv.types.formats import FileFormat
from glenv.log import logger

from typing import Iterable, Optional


class Manager(abc.ABC):
    def __init__(self, uri: str, *args, **kwargs):
        self.uri = uri

    @abc.abstractmethod
    def read(
        self, env: Optional[str] = None, include_default: bool = False
    ) -> Iterable[GitlabVariable]:
        ...

    @abc.abstractclassmethod
    def write(self, variables: Iterable[GitlabVariable], **kwargs) -> None:
        ...


class FileManager(Manager, abc.ABC):
    __file_format__: FileFormat = None

    @abc.abstractstaticmethod
    def _line_to_variable(line: str) -> GitlabVariable:
        """Implements how to parse a line for this file"""

    @abc.abstractstaticmethod
    def _variable_to_line(var: GitlabVariable) -> str:
        """Implements how each variable must be saved to a file"""

    def read(
        self, env: Optional[str] = None, include_default: bool = True
    ) -> Iterable[GitlabVariable]:
        logger.info(
            f"Reading variables from file {self.uri} using {self.__file_format__.__format_name__} format"
        )
        variables = []
        with open(self.uri, "r") as f:
            try:
                for line in f:
                    variable = self._line_to_variable(line)
                    variable.environment_scope = env
                    variables.append(variable)
            except ValueError:
                raise InvalidFile
        return variables

    def write(self, variables: Iterable[GitlabVariable], **kwargs) -> None:
        logger.info(
            f"Writing variables to file {self.uri} using {self.__file_format__.__format_name__} format"
        )
        with open(self.uri, "w") as file:
            for var in variables:
                file.write(self._variable_to_line(var))
