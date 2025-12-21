"""Configuration management module for Heimdall application."""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import click

from heimdall.utils.console import error_style, verbose_echo


@dataclass
class ConfigData:
    """
    Data class holding configuration parameters.
    
    :param count_parsers: Number of parsers (processes) which will work at the same time
    :type count_parsers: int
    :param count_tor_proxy: The number of tor proxies that will be created for the search
    :type count_tor_proxy: int
    :param save_results: The parameter responsible for saving the results
    :type save_results: bool
    """
    
    count_parsers: int = 6
    count_tor_proxy: int = 6
    save_results: bool = False

class Config:
    """
    Configuration manager for Heimdall.
    
    Handles loading, saving, and managing application configuration 
    with XDG standard compliance.
    """

    _verbose: bool
    _config: ConfigData
    def __init__(self, config_path: Optional[str], verbose: bool) -> None:
        """
        Initialize configuration manager.

        :param self: Description
        :param config_path: Description
        :type config_path: Optional[str]
        :param verbose: Description
        :type verbose: bool
        """
        self._verbose = verbose
        
        if config_path is None:
            config_dir = Path(os.environ.get('XDG_CONFIG_HOME', '~/.config')).expanduser() / 'heimdall'

            if not (config_dir / 'config.json').exists():
                verbose_echo(self._verbose, "Config file not found")
                self._config = self._generate_config()
            else:
                config_file = config_dir / 'config.json'
                with config_file.open("r+", encoding="utf8") as cf:
                    try:
                        self._config = json.load(cf)
                    except json.decoder.JSONDecodeError as err:
                        click.clear()
                        click.echo(error_style("Error parsing json configuration (use the '--verbose' flag for more details)"))
                        verbose_echo(self._verbose, err)

    def _generate_config(self) -> ConfigData:
        verbose_echo(self._verbose, "Generating a configuration file with standard parameters")
        config_dir = Path(os.environ.get('XDG_CONFIG_HOME', '~/.config')).expanduser() / 'heimdall'
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / 'config.json'

        config = ConfigData()
                
        with config_file.open("w+", encoding="utf8") as cf:
            json.dump(config.__dict__, cf)
            cf.close()
        
        return config