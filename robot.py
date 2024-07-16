import wpilib
import wpilib.drive
import magicbot

from rev import CANSparkMax
from phoenix6.hardware import CANcoder

from components.drive import Drive
from components.swerve.drive_module import DriveModule
from components.swerve.steering_module import SteeringModule
from components.swerve.swerve_module import SwerveModule

class MyRobot(magicbot.MagicRobot):
    # Injected components, these will be automatically built by MagicBot
    drive: Drive
    front_left_swerve_module_drive_module: DriveModule
    front_left_swerve_module_steering_module: SteeringModule
    front_left_swerve_module: SwerveModule

    def createObjects(self):
        '''Create motors and stuff here, they'll be passed to injected modules that ask for them by name'''
        self.drive_controller = wpilib.XboxController(0)

        self.front_left_swerve_module_drive_module_motor = CANSparkMax(1, CANSparkMax.MotorType.kBrushless)
        self.front_left_swerve_module_steering_module_motor = CANSparkMax(2, CANSparkMax.MotorType.kBrushless)
        self.front_left_swerve_module_steering_module_encoder = CANcoder(3)

        self.gyro = wpilib.AnalogGyro(1)

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        self.drive.arcade_drive(-self.drive_controller.getLeftY(), -self.drive_controller.getRightX())

    def robotPeriodic(self):
        '''Called in all modes, good for logging kinds of things'''
        pass