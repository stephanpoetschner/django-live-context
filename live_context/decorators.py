# coding: utf-8
from functools import wraps
import inspect

def read_live_context(view):
    @wraps(view)
    def inner(*args, **kwargs):
        self = args[0]
        argspec = inspect.getargspec(view)

        # try to fill missing arguments from live_context
        missing_args = argspec.args[len(args):]
        if hasattr(self, 'live_context') and self.live_context is not None:
            for missing_arg in missing_args:
                if missing_arg not in kwargs and \
                   missing_arg in self.live_context:
                    kwargs[missing_arg] = self.live_context[missing_arg]

        return view(*args, **kwargs)

    return inner
