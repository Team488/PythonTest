import magicbot
import navx
import ntcore
import wpilib
from components.swerve.swerve_module import SwerveModule
from wpimath.kinematics import (
    SwerveDrive4Kinematics,
    ChassisSpeeds,
    SwerveModuleState,
    SwerveModulePosition,
)
from wpimath.geometry import Translation2d, Rotation2d, Pose2d
from wpimath.estimator import SwerveDrive4PoseEstimator


class Drive:
    front_left_swerve_module: SwerveModule
    front_right_swerve_module: SwerveModule
    back_left_swerve_module: SwerveModule
    back_right_swerve_module: SwerveModule
    imu: navx.AHRS

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
        # TODO: set initial pose from a setting based on red vs blue
        initial_pose = Pose2d(0, 0, Rotation2d(0))
        self.estimator = SwerveDrive4PoseEstimator(
            self.kinematics,
            self.imu.getRotation2d(),
            # we can't get current swerve states here because they haven't been setup yet
            self.get_module_positions(),
            initial_pose,
            stateStdDevs=(0.05, 0.05, 0.01),
            visionMeasurementStdDevs=(0.4, 0.4, 0.03),
        )
        self.field = wpilib.Field2d()
        self.field_obj = self.field.getObject("fused_pose")

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

    def field_relative_drive(self, vx: float, vy: float, omega: float) -> None:
        """Field oriented drive commands"""
        current_heading = self.get_rotation()
        self.chassis_speeds = ChassisSpeeds.fromFieldRelativeSpeeds(
            vx, vy, omega, current_heading
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

        self.update_odometry()
        self.publish_data()

    def get_current_swerve_states(self):
        return [module.get_current_swerve_state() for module in self.modules]
    
    def get_module_positions(
        self,
    ) -> tuple[
        SwerveModulePosition,
        SwerveModulePosition,
        SwerveModulePosition,
        SwerveModulePosition,
    ]:
        return (
            self.modules[0].get_current_swerve_position(),
            self.modules[1].get_current_swerve_position(),
            self.modules[2].get_current_swerve_position(),
            self.modules[3].get_current_swerve_position(),
        )
    
    def get_target_swerve_states(self):
        return [module.get_target_swerve_state() for module in self.modules]

    def publish_data(self):
        self.setpoints_publisher.set(self.get_target_swerve_states())
        self.measurements_publisher.set(self.get_current_swerve_states())

    def get_pose(self) -> Pose2d:
        """Get the current location of the robot relative to ???"""
        return self.estimator.getEstimatedPosition()

    def get_rotation(self) -> Rotation2d:
        """Get the current heading of the robot."""
        return self.get_pose().rotation()
    
    def update_odometry(self) -> None:
        self.estimator.update(self.imu.getRotation2d(), self.get_module_positions())
        self.field_obj.setPose(self.get_pose())
