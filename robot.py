import wpilib
import wpilib.drive
import magicbot
from networktables import NetworkTables



class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        '''Create motors and stuff here'''
        self.drive_controller = wpilib.XboxController(0)

        self.drive_left_motor = wpilib.Talon(1)
        self.drive_right_motor = wpilib.Talon(2)
        self.drive = wpilib.drive.DifferentialDrive(self.drive_left_motor, self.drive_right_motor)

        self.gyro = wpilib.AnalogGyro(1)

        # NetworkTables.initialize()
        # self.sd = NetworkTables.getTable("SmartDashboard")

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        self.drive.arcadeDrive(-self.drive_controller.getLeftY(), -self.drive_controller.getRightX())

    def robotPeriodic(self):
        '''Called in all modes'''
        pass