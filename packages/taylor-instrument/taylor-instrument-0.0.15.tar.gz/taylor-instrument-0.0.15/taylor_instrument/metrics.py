# -*- coding: utf-8 -*-

from functools import wraps
from typing import Optional, Callable

from taylor_instrument import counters, instrument


def metrics(name: Optional[str] = None):
    """
    Decorator metrics for the functions

    :param name: (optional) the name
    """

    def actual_decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            correlation_id = instrument.get_correlation_id()
            _name = name if name else func.__name__

            # if contains dashes - prepare strings
            if '-' in correlation_id:
                correlation_id = correlation_id.replace('-', '_')
            if '-' in _name:
                _name = _name.replace('-', '_')

            counters.increment_one(f'{correlation_id}.{_name}.calls')
            timing = counters.begin_timing(f'{correlation_id}.{_name}.exec_time')
            return_value = func(*args, **kwargs)
            timing.end_timing()
            return return_value

        return wrapper

    return actual_decorator
