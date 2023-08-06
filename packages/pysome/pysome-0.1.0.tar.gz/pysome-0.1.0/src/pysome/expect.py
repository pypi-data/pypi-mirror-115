from typing import Any
from pysome import SameState


class expect:
    def __init__(self, data: Any):
        self.data = data

    def to_be(self, other):
        SameState._allow_same_usage = True
        SameState._state = {}
        assert other == self.data
        SameState._state = {}
        SameState._allow_same_usage = False
        return self

    def not_to_be(self, other):
        SameState._allow_same_usage = True
        SameState._state = {}
        assert not other == self.data
        SameState._state = {}
        SameState._allow_same_usage = False
        return self