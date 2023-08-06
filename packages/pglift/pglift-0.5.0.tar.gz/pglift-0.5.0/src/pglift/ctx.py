import functools
import logging
from abc import ABC, abstractmethod
from typing import Any, Optional, Sequence

from pgtoolkit import ctl
from pluggy import PluginManager

from . import __name__ as pkgname
from . import cmd, util
from .settings import POSTGRESQL_SUPPORTED_VERSIONS, Settings
from .types import CompletedProcess


class BaseContext(ABC):
    """Base class for execution context."""

    def __init__(
        self,
        *,
        plugin_manager: PluginManager,
        settings: Settings,
    ) -> None:
        self.settings = settings
        self.pm = plugin_manager

    @functools.lru_cache(maxsize=len(POSTGRESQL_SUPPORTED_VERSIONS) + 1)
    def pg_ctl(self, version: Optional[str]) -> ctl.PGCtl:
        pg_bindir = None
        version = version or self.settings.postgresql.default_version
        if version is not None:
            pg_bindir = self.settings.postgresql.versions[version].bindir
        pg_ctl = ctl.PGCtl(pg_bindir, run_command=self.run)
        if version is not None:
            installed_version = util.short_version(pg_ctl.version)
            if installed_version != version:
                raise EnvironmentError(
                    f"version mismatch: {installed_version} != {version}"
                )
        return pg_ctl

    @abstractmethod
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        ...

    @abstractmethod
    def run(
        self,
        args: Sequence[str],
        *,
        check: bool = False,
        **kwargs: Any,
    ) -> CompletedProcess:
        """Execute a system command using chosen implementation."""
        ...


class Context(BaseContext):
    """Default execution context."""

    _logger = logging.getLogger(pkgname)

    def debug(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        return self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        return self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        return self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        return self._logger.error(msg, *args, **kwargs)

    def exception(self, msg: Any, *args: Any, **kwargs: Any) -> None:
        return self._logger.exception(msg, *args, **kwargs)

    def run(self, args: Sequence[str], **kwargs: Any) -> CompletedProcess:
        """Execute a system command with :func:`pglift.cmd.run`."""
        return cmd.run(args, logger=self, **kwargs)
