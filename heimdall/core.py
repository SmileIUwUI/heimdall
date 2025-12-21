"""Module containing the main controller class for the application."""
from typing import Optional

import click

from heimdall.config import Config
from heimdall.utils.console import verbose_echo


class Controller:
    """
    Main application controller class.
    
    Manages tor proxy configuration, search operations, and process coordination.
    """

    _query: str
    _config: Config
    _verbose: bool
    _config_path: Optional[str]
    def __init__(self, ctx: click.core.Context, query: str) -> None:
        """
        Initialize the Controller instance.

        :param ctx: The context of the click module
        :type ctx: click.core.Context
        :param query: The string that will be searched for
        :type query: str
        """
        self._query = query
        self._verbose = ctx.obj["verbose"]
        self._config_path = ctx.obj["config_path"]

        verbose_echo(self._verbose, "Initializing the \"Config\" object")
        self._config = Config(self._config_path, self._verbose)