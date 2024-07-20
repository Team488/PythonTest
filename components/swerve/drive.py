import magicbot
from components.swerve.swerve_module import SwerveModule
from wpimath.kinematics import (
    SwerveDrive4Kinematics,
    ChassisSpeeds,
)

class Drive:
    front_left_swerve_module: SwerveModule
    front_right_swerve_module: SwerveModule
    back_left_swerve_module: SwerveModule
    back_right_swerve_module: SwerveModule

    chassis_speeds = magicbot.will_reset_to(ChassisSpeeds(0, 0, 0))
    
    def setup(self):
        self.modules = [
            self.front_left_swerve_module,
            self.front_right_swerve_module,
            self.back_left_swerve_module,
            self.back_right_swerve_module,
        ]
        self.kinematics = SwerveDrive4Kinematics(
            *(module.position_on_robot for module in self.modules)
        )

    def robot_relative_drive(self, x_speed: float, y_speed: float, rot_speed: float):
        self.chassis_speeds = ChassisSpeeds(x_speed, y_speed, rot_speed)

    def stop(self):
        self.chassis_speeds = ChassisSpeeds(0, 0, 0)

    def execute(self):
        desired_states = self.kinematics.toSwerveModuleStates(self.chassis_speeds)
        for state, module in zip(desired_states, self.modules):
            module.set_swerve_state(state)