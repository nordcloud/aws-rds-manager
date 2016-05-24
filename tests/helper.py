from argparse import Namespace
from collections import namedtuple

call_struct = namedtuple('call', ['args', 'kwargs'])


class MockObject(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __setattr__(self, key, value):
        self.__dict__[key] = value


class MockMethod(Namespace):
    def __init__(self, response=None, **kwargs):
        self.response = response
        super(MockMethod, self).__init__(**kwargs)
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append(call_struct(
            args, kwargs
        ))
        return self.response
