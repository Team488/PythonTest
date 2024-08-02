from dataclasses import dataclass

import magicbot
from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import (
    SwerveModuleState,
)

from components.swerve.drive_wheel import DriveWheel
from components.swerve.steering import SteeringMechanism

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


    _drive_module: DriveWheel
    _steering_module: SteeringMechanism
    _swerve_state = magicbot.will_reset_to(SwerveModuleState(0, Rotation2d(0)))

    def setup(self):
        self._drive_module = DriveWheel(self.config.drive_can_id)
        self._steering_module = SteeringMechanism(self.config.steering_can_id, self.config.steering_encoder_can_id)

    @property
    def position_on_robot(self) -> Translation2d:
        return self.config.position

    def set_swerve_state(self, state: SwerveModuleState):
        self._swerve_state = state
        self._drive_module.set_target_speed(self._swerve_state.speed)
        self._steering_module.set_target_angle(self._swerve_state.angle)

    def execute(self):
        # these sub components are true top level components so we need to call execute() 
        # on them to make sure they apply their outputs
        self._drive_module.execute()
        self._steering_module.execute()