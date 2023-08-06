import os

from tackle.models import BaseHook, Field


class OsSystemHook(BaseHook):
    """Run system commands."""

    hook_type: str = 'os_system'

    command: str = Field(..., description="A shell command.")
    ignore_error: bool = Field(False, description="Ignore errors.")

    args: list = ['command']

    def exec(self) -> None:
        # try:
        os.system(self.command)
        # except
