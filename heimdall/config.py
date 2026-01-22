"""Configuration management module for Heimdall application."""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import click

from heimdall.utils.console import error_style, verbose_echo


@dataclass
class ConfigData:
    """
    Data class holding configuration parameters.

    :param tor_data_path: The path to the file with information about the tor proxy
    :type tor_data_path: pathlib.Path
    :param count_parsers: Number of parsers (processes) which will work at the same time
    :type count_parsers: int
    :param count_tor_proxy: The number of tor proxies that will be created for the search
    :type count_tor_proxy: int
    :param save_results: The parameter responsible for saving the results
    :type save_results: bool
    """

    tor_data_path: Optional[Path] = None
    count_parsers: int = 6
    count_tor_proxy: int = 6
    save_results: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConfigData":
        """
        Create ConfigData instance from dictionary.

        Handles conversion of string paths to Path objects and provides default
        values for tor_data_path using XDG_DATA_HOME standard.

        :param data: Dictionary containing configuration parameters
        :type data: Dict[str, Any]
        :return: New ConfigData instance
        :rtype: ConfigData
        """
        data["tor_data_path"] = (
            Path(os.environ.get("XDG_DATA_HOME", "~/.local/share")).expanduser()
            / "heimdall/tor_proxy.json"
            if data["tor_data_path"] is None
            else Path(data["tor_data_path"])
        )

        return cls(
            tor_data_path=data["tor_data_path"],
            count_parsers=data["count_parsers"],
            count_tor_proxy=data["count_tor_proxy"],
            save_results=data["save_results"],
        )


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

        :param config_path: The path to the json configuration file
        :type config_path: Optional[str]
        :param verbose: Enable verbose output
        :type verbose: bool
        """
        self._verbose = verbose
        self._load_config(config_path)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        :param key: Configuration key name
        :type key: str
        :param default: Default value if key not found
        :type default: Any
        :return: Configuration value
        :rtype: Any
        """
        return getattr(self._config, key, default)

    def _generate_config(self) -> ConfigData:
        verbose_echo(
            self._verbose, "Generating a configuration file with standard parameters"
        )
        config_dir = (
            Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
            / "heimdall"
        )
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"

        config = ConfigData()

        with config_file.open("w+", encoding="utf8") as cf:
            json.dump(config.__dict__, cf)
            cf.close()

        return config

    def _load_config(self, config_path: Optional[str]):
        if config_path is None:
            config_dir = (
                Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
                / "heimdall"
            )

            if not (config_dir / "config.json").exists():
                verbose_echo(self._verbose, "Config file not found")
                self._config = self._generate_config()
            else:
                config_file = config_dir / "config.json"
                with config_file.open("r+", encoding="utf8") as cf:
                    try:
                        self._config = ConfigData.from_dict(json.load(cf))
                    except json.decoder.JSONDecodeError as err:
                        click.clear()
                        click.echo(
                            error_style(
                                "Error parsing json configuration (use the '--verbose' flag for more details)"
                            )
                        )
                        verbose_echo(self._verbose, err)
        else:
            config_path: Path = Path(config_path)

            if not config_path.exists():
                verbose_echo(self._verbose, "Config file not found")
                self._config = self._generate_config()
            else:
                with config_path.open("r+", encoding="utf8") as cf:
                    try:
                        self._config = ConfigData.from_dict(json.load(cf))
                    except json.decoder.JSONDecodeError as err:
                        click.clear()
                        click.echo(
                            error_style(
                                "Error parsing json configuration (use the '--verbose' flag for more details)"
                            )
                        )
                        verbose_echo(self._verbose, err)
