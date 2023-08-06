from glenv.types.variable import GitlabVariable
from typing import Optional

import os

from glenv.managers.dotenv import DotEnvManager
from glenv.managers.gitlab import GitlabManager
from glenv.managers.utils import get_manager_by_format, get_manager_by_uri
from glenv.types.formats import DotEnvFile


class GlEnv(object):
    """Easily manage Gitlab CI variables from files or repo-to-repo"""

    def __init__(self, gitlab_token: Optional[str] = None):
        self._gitlab_token = self._read_gitlab_token(gitlab_token)

    def _read_gitlab_token(self, gitlab_token: Optional[str] = None):
        if gitlab_token:
            return gitlab_token

        return os.getenv("GLENV_GITLAB_TOKEN", os.getenv("GITLAB_TOKEN"))

    def _set_variable_properties(
        self,
        variable: GitlabVariable,
        masked: Optional[bool],
        protected: Optional[bool],
    ):
        if masked is not None:
            variable.masked = masked

        if protected is not None:
            variable.protected = protected

        return variable

    def copy(
        self,
        src: str,
        dst: str,
        env: Optional[str] = None,
        force_masked: Optional[bool] = None,
        force_protected: Optional[bool] = None,
        create_unsecure: bool = True,
        override_existing: bool = False,
        include_default: bool = True,
    ):
        """
        Copies variables from SRC to DST.

        :param src: path to read variables from. It can be a local path or a Gitlab http/https path
        :param dst: path to write variables to. It can be a local path or a Gitlab http/https path
        :param env: filter variables of this environment
        :param force_masked: save variables as Masked on Gitlab
        :param force_protected: save variables as Protected on Gitlab
        :param create_unsecure: if variable cannot be `Masked` it will create it as `Unmasked` otherwise it will not create it
        :param override_existing: override existing variables with new values
        :param include_default: include variables set as `Default (All)`
        """
        source_manager = get_manager_by_uri(src)
        destination_manager = get_manager_by_uri(dst)
        variables = map(
            lambda var: self._set_variable_properties(
                var, force_masked, force_protected
            ),
            source_manager(src, gitlab_token=self._gitlab_token).read(
                env, include_default
            ),
        )
        destination_manager(dst, gitlab_token=self._gitlab_token).write(
            variables,
            create_unsecure=create_unsecure,
            override_existing=override_existing,
        )

    def pull(
        self,
        src: str,
        filename: Optional[str] = None,
        env: Optional[str] = None,
        format: str = DotEnvFile.__format_name__,
        include_default: bool = False,
    ):
        """
        Pulls variables from SRC and save them to FILENAME.

        :param src: project url for reading from
        :param filename: filename for writing variables
        :param env: environment for filtering
        :param include_default: includes variables set as `Default (All)`
        """
        variables = GitlabManager(src, self._gitlab_token).read(env, include_default)
        writer = get_manager_by_format(format)
        writer(filename).write(variables)

    def push(
        self,
        filename: str,
        dst: str,
        env: Optional[str] = None,
        masked: bool = False,
        protected: bool = True,
        create_unsecure: bool = True,
        override_existing: bool = True,
    ):
        """
        Pushes variables from FILENAME to DST repository.

        :param filename: file for reading variables from
        :param dst: Gitlab repository URL
        :param env: set `environment_scope` for these variables ("*" for setting variables as `Default (All)`)
        :param masked: create variables as `Masked`
        :param protected: create variables as `Protected`
        :param create_unsecure: if variable cannot be `Masked` it will create it as `Unmasked`
        :param override_existing: overrides existing variables with new values
        """
        variables = map(
            lambda var: self._set_variable_properties(var, masked, protected),
            DotEnvManager(filename).read(env),
        )
        GitlabManager(dst, self._gitlab_token).write(
            variables,
            create_unsecure=create_unsecure,
            override_existing=override_existing,
        )
