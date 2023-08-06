from dataclasses import dataclass
from typing import Optional


@dataclass
class GitlabVariable(object):
    key: str
    value: str
    mask: Optional[bool] = False
    protected: Optional[bool] = False
    environment_scope: str = "*"
    variable_type: Optional[str] = "env_var"
