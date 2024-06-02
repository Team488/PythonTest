import wpilib


class Drive:
    drive_left_motor: wpilib.Talon
    drive_right_motor: wpilib.Talon
    
    def setup(self):
        self.drive_train = wpilib.drive.DifferentialDrive(self.drive_left_motor, self.drive_right_motor)
        self.desired_speed = (0, 0)

    def tank_drive(self, left: float, right: float):
        self.desired_speed = (left, right)

    def stop(self):
        self.desired_speed = (0, 0)

    def execute(self):
        self.drive_train.tankDrive(*self.desired_speed)