import wpilib
from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state


class DriveForward(StatefulAutonomous):
    # defining this typehint this here will have it be injected into the class
    drive: wpilib.drive.DifferentialDrive

    MODE_NAME = "Drive Forward"
    DEFAULT = True

    def initialize(self):
        # This allows you to tune the variable via the SmartDashboard over
        # networktables
        self.register_sd_var("drive_speed", 1)

    @timed_state(duration=0.5, next_state="drive_forward", first=True)
    def drive_wait(self):
        self.drive.tankDrive(0, 0)

    @timed_state(duration=1, next_state="stop")
    def drive_forward(self):
        self.drive.tankDrive(self.drive_speed, self.drive_speed)

    @state()  # Remove or modify this to add additional states to this class.
    def stop(self):
        self.drive.tankDrive(0, 0)