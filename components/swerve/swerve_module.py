from components.swerve.drive_module import DriveModule
from components.swerve.steering_module import SteeringModule


class SwerveModule:
    drive_module: DriveModule
    # start with just Drive for simplicity
    # steering: SteeringModule

    def execute(self):
        # TODO: apply drive and steering intents to submodules
        pass