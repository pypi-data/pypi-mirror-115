from dataclasses import asdict
from glenv.types.variable import GitlabVariable
from typing import Iterable, Optional
from urllib.parse import urlparse

from glenv.log import logger
from glenv.managers.base import Manager
from glenv.managers.exceptions import InvalidParams, InvalidValue, KeyAlreadyExists

from gitlab import Gitlab
from gitlab.exceptions import GitlabCreateError


class GitlabManager(Manager):
    def __init__(self, uri: str, gitlab_token: str) -> None:
        super().__init__(uri)

        if not gitlab_token:
            raise InvalidParams("Missing gitlab_token")

        uri_parsed = urlparse(uri)
        gitlab_host = f"{uri_parsed.scheme}://{uri_parsed.netloc}"
        gitlab_path = uri_parsed.path.lstrip("/")

        client = Gitlab(gitlab_host, gitlab_token)

        self.project = client.projects.get(gitlab_path)

    def read(
        self, env: Optional[str] = None, include_default: bool = False
    ) -> Iterable[GitlabVariable]:
        logger.info(
            f"Reading variables from Gitlab (env_scope: {env} | include_default: {include_default})"
        )
        variables = [
            GitlabVariable(
                key=var.key,
                value=var.value,
                mask=var.masked,
                protected=var.protected,
                environment_scope=var.environment_scope,
                variable_type=var.variable_type,
            )
            for var in self.project.variables.list(all=True)
        ]

        if env:
            return self._filter_env_variables(variables, env, include_default)

        return variables

    def write(
        self,
        variables: Iterable[GitlabVariable],
        create_unsecure: bool = True,
        override_existing: bool = True,
    ):
        logger.info(
            f"Writing variables to Gitlab (create_unsecure: {create_unsecure} | override_existing: {override_existing})"
        )
        for var in variables:
            self._create_variable(var, var.mask, create_unsecure, override_existing)

    def _create_variable(
        self,
        var: GitlabVariable,
        masked: bool,
        create_unsecure: bool,
        override_existing: bool,
    ) -> GitlabVariable:
        try:
            var.mask = masked
            created = self.project.variables.create(asdict(var))

            logger.info(f"\tCreated variable {var.key} {'masked' if masked else ''}")
            return created

        except GitlabCreateError as e:
            gitlab_error = self._parse_gitlab_error(e)

            if isinstance(gitlab_error, KeyAlreadyExists) and override_existing:
                updated = self.project.variables.update(
                    id=var.key,
                    new_data=asdict(var),
                    filter={"environment_scope": var.environment_scope},
                )
                logger.info(
                    f"\tUpdated variable {var.key} {'masked' if var.mask else ''}"
                )
                return updated

            if (
                isinstance(gitlab_error, InvalidValue)
                and masked
                and self.create_unsecure
            ):
                return self._create_variable(
                    var, False, create_unsecure, override_existing
                )
            elif isinstance(gitlab_error, InvalidValue):
                logger.error(f"\tError creating variable {var}")

    @staticmethod
    def _filter_env_variables(
        variables: Iterable[GitlabVariable], env: str, include_default: bool
    ) -> Iterable[GitlabVariable]:
        env_vars = {}

        # Sorting variables we get first the default ones so, if there is an environment-specific it will override it
        for var in sorted(variables, key=lambda var: var.environment_scope):
            if var.environment_scope == env or (
                var.environment_scope == "*" and include_default
            ):
                env_vars[var.key] = var

        return env_vars.values()

    @staticmethod
    def _parse_gitlab_error(exception):
        if "has already been taken" in exception.error_message.get("key", [""])[0]:
            return KeyAlreadyExists()
        elif "is invalid" in exception.error_message.get("value", [""])[0]:
            return InvalidValue()
