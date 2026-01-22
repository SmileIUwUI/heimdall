"""
Tor proxy configuration management module for Heimdall application.

This module provides classes and functions for managing Tor proxy configurations,
including data structures for proxy settings and a manager class for loading,
saving, and handling Tor proxy configuration files.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import click

from heimdall.utils.console import error_style, verbose_echo


@dataclass
class TorProxyData:
    """
    Data class representing configuration for a single Tor proxy instance.

    :param port: SOCKS5 port number for the Tor proxy
    :type port: int
    :param control_port: Control port number for Tor controller
    :type control_port: int
    :param dir_path: Directory path for Tor data files
    :type dir_path: Path
    """

    port: int
    control_port: int
    dir_path: Path

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert TorProxyData instance to dictionary for serialization.

        :return: Dictionary representation of Tor proxy configuration
        :rtype: Dict[str, Any]
        """
        return {
            "port": self.port,
            "control_port": self.control_port,
            "dir_path": self.dir_path,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TorProxyData":
        """
        Create TorProxyData instance from dictionary.

        :param data: Dictionary containing Tor proxy configuration
        :type data: Dict[str, Any]
        :return: New TorProxyData instance
        :rtype: TorProxyData
        """
        return cls(
            port=data["port"],
            control_port=data["control_port"],
            dir_path=Path(data["dir_path"]),
        )


@dataclass
class TorData:
    """
    Data class containing collection of Tor proxy configurations.

    :param proxies: List of Tor proxy configurations
    :type proxies: List[TorProxyData]
    """

    proxies: List[TorProxyData] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert TorData instance to dictionary for serialization.

        :return: Dictionary representation of all Tor configurations
        :rtype: Dict[str, Any]
        """
        proxies = []
        for proxy in self.proxies:
            proxies.append(proxy.to_dict())

        return {"proxies": proxies}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TorData":
        """
        Create TorData instance from dictionary.

        :param data: Dictionary containing Tor configurations
        :type data: Dict[str, Any]
        :return: New TorData instance
        :rtype: TorData
        """
        return cls(proxies=data["proxies"])


class TorManager:
    """
    Manager class for handling Tor proxy configurations.

    Responsible for loading, saving, and managing Tor proxy data files.
    """

    _verbose: bool
    _data: TorData

    def __init__(self, data_path: Path, verbose: bool) -> None:
        """
        Initialize TorManager instance.

        :param data_path: Path to Tor proxy data file
        :type data_path: Path
        :param verbose: Enable verbose output mode
        :type verbose: bool
        """
        self._verbose = verbose
        self._load_data(data_path)

    def _load_data(self, data_path: Path) -> None:
        """
        Load Tor proxy data from file or create new if file doesn't exist.

        :param data_path: Path to Tor proxy data file
        :type data_path: Path
        """
        if not data_path.exists():
            click.echo(error_style("The tor proxy data file was not found"))
            verbose_echo(
                self._verbose,
                "Generating a standard file with data about the tor proxy",
            )
            self._data = self._generate_data(data_path)
        else:
            with data_path.open("r", encoding="utf8") as df:
                try:
                    self._data = TorData.from_dict(json.load(df))
                except json.decoder.JSONDecodeError as err:
                    click.clear()
                    click.echo(
                        error_style(
                            "Error parsing json configuration (use the '--verbose' flag for more details)"
                        )
                    )
                    verbose_echo(self._verbose, err)

    def _generate_data(self, path: Path) -> TorData:
        """
        Generate default Tor proxy data and save to file.

        :param path: Path where to save generated data file
        :type path: Path
        :return: New TorData instance with default configuration
        :rtype: TorData
        """
        path.parent.mkdir(exist_ok=True, parents=True)

        data = TorData()
        with path.open("w+", encoding="utf8") as df:
            json.dump(data.to_dict(), df)
            df.close()

        return data
