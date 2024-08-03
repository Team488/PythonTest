import magicbot
import ntcore
from components.swerve.swerve_module import SwerveModule
from wpimath.kinematics import (
    SwerveDrive4Kinematics,
    ChassisSpeeds,
    SwerveModuleState,
)


class Drive:
    front_left_swerve_module: SwerveModule
    front_right_swerve_module: SwerveModule
    back_left_swerve_module: SwerveModule
    back_right_swerve_module: SwerveModule

    chassis_speeds = magicbot.will_reset_to(ChassisSpeeds(0, 0, 0))
    
    max_translation_speed = magicbot.tunable(2.0)
    single_module_control = magicbot.tunable(False)
    single_module = magicbot.tunable(0)

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

        nt = ntcore.NetworkTableInstance.getDefault().getTable("/components/drive")
        module_states_table = nt.getSubTable("module_states")
        self.setpoints_publisher = module_states_table.getStructArrayTopic(
            "setpoints", SwerveModuleState
        ).publish()
        self.measurements_publisher = module_states_table.getStructArrayTopic(
            "measured", SwerveModuleState
        ).publish()

    def robot_relative_drive(self, x_intent: float, y_intent: float, rot_speed: float):
        # Scale drive speed by the max we'd like to be able to go
        self.chassis_speeds = ChassisSpeeds(
            x_intent * self.max_translation_speed,
            y_intent * self.max_translation_speed,
            rot_speed,
        )

    def stop(self):
        self.chassis_speeds = ChassisSpeeds(0, 0, 0)

    def execute(self):
        desired_states = self.kinematics.toSwerveModuleStates(self.chassis_speeds)
        if self.single_module_control:
            self.modules[self.single_module].set_target_swerve_state(desired_states[self.single_module])
        else:
            for state, module in zip(desired_states, self.modules):
                module.set_target_swerve_state(state)

        self.setpoints_publisher.set(
            [module.get_target_swerve_state() for module in self.modules]
        )
        self.measurements_publisher.set(
            [module.get_current_swerve_state() for module in self.modules]
        )
