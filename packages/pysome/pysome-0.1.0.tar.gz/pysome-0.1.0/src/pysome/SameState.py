class default_name:
    def __hash__(self):
        return hash(str(self))


class SameState:
    _allow_same_usage = False
    _state = {}


class same_context(object):
    def __init__(self, state=None):
        if state is None:
            state = {}
        self.state = state

    def __enter__(self):
        SameState._allow_same_usage = True
        SameState._state = self.state
        return self.state

    def __exit__(self):
        SameState._allow_same_usage = False
        SameState._state = {}