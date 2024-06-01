from magicbot import AutonomousStateMachine, timed_state

class NoOp(AutonomousStateMachine):
    MODE_NAME = "No Op"
    DEFAULT = True

    @timed_state(first=True, duration=15)
    def dont_do_something(self):
        """This happens first"""
        pass
