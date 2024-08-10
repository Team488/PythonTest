from dataclasses import dataclass

import magicbot
import ntcore
from wpimath.geometry import Translation2d, Rotation2d
from wpimath.kinematics import (
    SwerveModuleState,
    SwerveModulePosition,
)

from components.swerve.drive_wheel import DriveWheel
from components.swerve.steering import SteeringMechanism

@dataclass
class SwerveModuleConfig:
    # where is the module on the robot relative to the center of the robot
    # remember x positive is robot 'forward' and positive y is robot 'left'
    position: Translation2d
    drive_can_id: int
    steering_can_id: int
    steering_encoder_can_id: int
    prefix: str

class SwerveModule:
    # Injected values
    config: SwerveModuleConfig

    # Private values not injected
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
        return SwerveModuleState(self._drive_module.get_current_speed(), self._steering_module.get_absolute_encoder_position())

    def get_distance_traveled(self) -> float:
        # if _drive_module isn't initialized yet, return 0
        if hasattr(self, '_drive_module') is False:
            return 0
        return self._drive_module.get_current_position()
    
    def get_rotation(self) -> Rotation2d:
        """Get the steer angle as a Rotation2d"""
        return Rotation2d(self.get_angle_integrated())
    
    def get_angle_integrated(self) -> float:
        # if _steering_module isn't initialized yet, return 0
        if hasattr(self, '_steering_module') is False:
            return 0
        return self._steering_module.get_absolute_encoder_position().degrees()

    def get_current_swerve_position(self) -> SwerveModulePosition:
        return SwerveModulePosition(self.get_distance_traveled(), self.get_rotation())

    def execute(self):
        # these sub components are true top level components so we need to call execute() 
        # on them to make sure they apply their outputs
        self._drive_module.execute()
        self._steering_module.execute()