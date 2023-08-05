# -*- coding: utf-8 -*-
from typing import Optional

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.errors import ApplicationException
from pip_services3_components.log import CompositeLogger, LogLevel


class CustomCompositeLogger(CompositeLogger):
    _correlation_id: Optional[str] = None

    def configure(self, config: ConfigParams):
        self._correlation_id = config.get_as_nullable_string("correlation_id")
        super().configure(config)

    def log(self, level: LogLevel, error: ApplicationException, message: str, *args,
            correlation_id: Optional[str] = None, **kwargs):
        super().log(level, correlation_id or self._correlation_id, error, message, *args, **kwargs)

    def fatal(self, error: ApplicationException, message: str, *args, correlation_id: Optional[str] = None, **kwargs):
        super().fatal(correlation_id or self._correlation_id, error, message, *args, **kwargs)

    def error(self, error: ApplicationException, message: str, *args, correlation_id: Optional[str] = None, **kwargs):
        super().error(correlation_id or self._correlation_id, error, message, *args, **kwargs)

    def warn(self, message: str, *args, correlation_id: Optional[str] = None, **kwargs):
        super().warn(correlation_id or self._correlation_id, message, *args, **kwargs)

    def info(self, message: str, *args, correlation_id: Optional[str] = None, **kwargs):
        super().info(correlation_id or self._correlation_id, message, *args, **kwargs)

    def debug(self, message: str, *args, correlation_id: Optional[str] = None, **kwargs):
        super().debug(correlation_id or self._correlation_id, message, *args, **kwargs)

    def trace(self, message: str, *args, correlation_id: Optional[str] = None, **kwargs):
        super().trace(correlation_id or self._correlation_id, message, *args, **kwargs)
