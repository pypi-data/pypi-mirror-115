from typing import Type
from urllib.parse import urlparse

from glenv.managers.base import Manager
from glenv.managers.dotenv import DotEnvManager
from glenv.managers.gitlab import GitlabManager
from glenv.managers.terraform import TerraformManager
from glenv.types.formats import DotEnvFile, FileFormat, TerraformFile


def get_file_format(path: str) -> FileFormat:
    if path.endswith(".tfvars") or path.endswith(".tf"):
        return TerraformFile
    return DotEnvFile


def get_manager_by_uri(uri: str) -> Type[Manager]:
    source = urlparse(uri)

    if source.scheme == "http" or source.scheme == "https":
        return GitlabManager

    file_format = get_file_format(source.path)

    if file_format == TerraformFile:
        return TerraformManager

    return DotEnvManager


def get_manager_by_format(fmt: str) -> Type[Manager]:
    if fmt == TerraformFile.__format_name__:
        return TerraformManager

    return DotEnvManager
