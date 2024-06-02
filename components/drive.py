from typing import NamedTuple
import wpilib

DriveIntent = NamedTuple("DriveIntent", [("y", float), ("rotation", float)])

class Drive:
    drive_left_motor: wpilib.Talon
    drive_right_motor: wpilib.Talon

    _drive_train: wpilib.drive.DifferentialDrive
    _desired_speed: DriveIntent
    
    def setup(self):
        self._drive_train = wpilib.drive.DifferentialDrive(self.drive_left_motor, self.drive_right_motor)
        self._desired_speed = DriveIntent(0, 0)

    def arcade_drive(self, y: float, rotation: float):
        self._desired_speed = DriveIntent(y, rotation)

    def stop(self):
        self._desired_speed = DriveIntent(0, 0)

    def execute(self):
        self._drive_train.arcadeDrive(*self._desired_speed)