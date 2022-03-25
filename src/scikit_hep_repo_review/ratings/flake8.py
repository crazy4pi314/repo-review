from __future__ import annotations

import configparser
import functools
from pathlib import Path
from typing import Any

import tomli as tomllib

# FK: Flake8


class Flake8:
    provides = {"flake8"}

    @staticmethod
    @functools.cache
    def flake8(package: Path) -> dict[str, Any] | None:
        pyproject_path = package / "pyproject.toml"
        if pyproject_path.exists():
            with pyproject_path.open("rb") as f:
                pyproject = tomllib.load(f)
                if "flake8" in pyproject.get("tool", {}):
                    return pyproject["tool"]["flake8"]  # type: ignore[no-any-return]
        flake8_ini_path = package / ".flake8"
        flake8_setup_cfg = package / "setup.cfg"
        flake8_tox_ini = package / "tox.ini"

        for flake8_path in [flake8_ini_path, flake8_setup_cfg, flake8_tox_ini]:
            if flake8_path.exists():
                config = configparser.ConfigParser()
                config.read(flake8_path)
                if "flake8" in config:
                    return dict(config["flake8"])

        return None


class FK001(Flake8):
    "Has Flake8 config"

    @staticmethod
    def check(flake8: dict[str, Any] | None) -> bool:
        """
        All projects should have a pyproject.toml file to support a modern
        build system and support wheel installs properly.
        """
        return flake8 is not None


class FK002(Flake8):
    "Uses extend ignore"
    requires = {"FK001"}

    @staticmethod
    def check(flake8: dict[str, Any]) -> bool:
        """
        extend-ignore should be used instead of ignore, shorter list doesn't wipe defaults.
        """
        return "extend-ignore" in flake8


class FK003(Flake8):
    "Uses extend select"
    requires = {"FK001", "PC131"}

    @staticmethod
    def check(flake8: dict[str, Any]) -> bool:
        """
        extend-ignore should be used instead of ignore, shorter list doesn't wipe defaults.
        """
        return "extend-ignore" in flake8
