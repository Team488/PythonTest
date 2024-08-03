import navx
import wpilib
import wpilib.drive
import magicbot

from wpimath.geometry import Translation2d

from components.swerve.drive import Drive
from components.swerve.swerve_module import SwerveModule, SwerveModuleConfig

class MyRobot(magicbot.MagicRobot):
    # Injected components, these will be automatically built by MagicBot
    drive: Drive
    front_left_swerve_module: SwerveModule
    front_right_swerve_module: SwerveModule
    back_left_swerve_module: SwerveModule
    back_right_swerve_module: SwerveModule



    def createObjects(self):
        '''Create motors and stuff here, they'll be passed to injected modules that ask for them by name'''
        self.drive_controller = wpilib.XboxController(0)

        self.front_left_swerve_module_config = SwerveModuleConfig(
            prefix="front_left",
            position=Translation2d(0.5, 0.5),
            drive_can_id=31,
            steering_can_id=30,
            steering_encoder_can_id=51
        )
        self.front_right_swerve_module_config = SwerveModuleConfig(
            prefix="front_right",
            position=Translation2d(-0.5, 0.5),
            drive_can_id=29,
            steering_can_id=28,
            steering_encoder_can_id=52
        )
        self.back_left_swerve_module_config = SwerveModuleConfig(
            prefix="back_left",
            position=Translation2d(0.5, -0.5),
            drive_can_id=38,
            steering_can_id=39,
            steering_encoder_can_id=53
        )
        self.back_right_swerve_module_config = SwerveModuleConfig(
            prefix="back_right",
            position=Translation2d(-0.5, -0.5),
            drive_can_id=21,
            steering_can_id=20,
            steering_encoder_can_id=54
        )

        self.imu = navx.AHRS.create_spi()
        self.gyro = wpilib.AnalogGyro(1)

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        # drive robot with joysticks
        self.drive.robot_relative_drive(-self.drive_controller.getLeftX(), -self.drive_controller.getLeftY(), -self.drive_controller.getRightX())
       
    def robotPeriodic(self):
        '''Called in all modes, good for logging kinds of things'''
        pass