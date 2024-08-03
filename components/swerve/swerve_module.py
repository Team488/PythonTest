from dataclasses import dataclass

import magicbot
import ntcore
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
    prefix: str

class SwerveModule:
    # Injected values
    config: SwerveModuleConfig


    _drive_module: DriveWheel
    _steering_module: SteeringMechanism
    _target_swerve_state = magicbot.will_reset_to(SwerveModuleState(0, Rotation2d(0)))

    def setup(self):
        self._drive_module = DriveWheel(self.config.drive_can_id)
        self._steering_module = SteeringMechanism(self.config.steering_can_id, self.config.steering_encoder_can_id, self.config.prefix)

    @property
    def position_on_robot(self) -> Translation2d:
        return self.config.position
    
    def get_target_swerve_state(self) -> SwerveModuleState:
        return self._target_swerve_state

    def set_target_swerve_state(self, state: SwerveModuleState):
        self._target_swerve_state = state
        self._drive_module.set_target_speed(self._target_swerve_state.speed)
        self._steering_module.set_target_angle(self._target_swerve_state.angle)

    def get_current_swerve_state(self) -> SwerveModuleState:
        return SwerveModuleState(self._drive_module.get_current_speed(), self._steering_module.get_absolute_encoder_position_degrees())

    def execute(self):
        # these sub components are true top level components so we need to call execute() 
        # on them to make sure they apply their outputs
        self._drive_module.execute()
        self._steering_module.execute()