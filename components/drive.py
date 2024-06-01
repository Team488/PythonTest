import wpilib

class Drive:
    left: wpilib.Talon
    right: wpilib.Talon

    def execute(self):
        # spin in place
        self.left.set(1)
        self.right.set(1)