import wpilib
from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state

from components.swerve.drive import Drive


class DriveForward(StatefulAutonomous):
    # defining this typehint this here will have it be injected into the class
    drive: Drive

    MODE_NAME = "Drive Forward"
    DEFAULT = True

    def initialize(self):
        # This allows you to tune the variable via the SmartDashboard over
        # networktables
        self.register_sd_var("drive_speed", 1)

    @timed_state(duration=0.5, next_state="drive_forward", first=True)
    def drive_wait(self):
        self.drive.stop()

    @timed_state(duration=1, next_state="stop")
    def drive_forward(self):
        self.drive.robot_relative_drive(0, self.drive_speed, 0)

    @state()  # Remove or modify this to add additional states to this class.
    def stop(self):
        self.drive.robot_relative_drive(0, 0, 0)