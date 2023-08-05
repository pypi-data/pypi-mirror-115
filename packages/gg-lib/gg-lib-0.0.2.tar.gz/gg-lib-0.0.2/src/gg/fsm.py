class StatefulMixin:
    def __init__(self, *args, **kwargs):
        super(StatefulMixin, self).__init__(*args, **kwargs)
        self.state = kwargs.get('state', {})

    def update_state(self, state):
        self.state.update(state)


class StateMachine:
    def __init__(self, *args, **kwargs):
        self.state = kwargs.get('state', {})
