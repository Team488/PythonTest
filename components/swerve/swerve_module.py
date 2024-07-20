from dataclasses import dataclass

from wpimath.geometry import Translation2d, Rotation2d, Pose2d
from wpimath.kinematics import (
    SwerveModuleState,
)

from components.swerve.drive_module import DriveModule
from components.swerve.steering_module import SteeringModule

@dataclass
class SwerveModuleConfig:
    # where is the module on the robot relative to the center of the robot?
    position: Translation2d
    drive_can_id: int
    steering_can_id: int
    steering_encoder_can_id: int

class SwerveModule:
    # Injected values
    config: SwerveModuleConfig


    _drive_module: DriveModule

    def setup(self):
        self._drive_module = DriveModule(self.config.drive_can_id)
        # self.steering_module = SteeringModule(self.config.steering_can_id, self.config.steering_encoder_can_id)

    @property
    def position_on_robot(self) -> Translation2d:
        return self.config.position

    def set_swerve_state(self, state: SwerveModuleState):
        self._drive_module.set_target_speed(state.speed)
        # self.steering_module.set_target_angle(state.angle)

    def execute(self):
        # TODO: apply drive and steering intents to submodules
        pass