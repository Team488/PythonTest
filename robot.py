import wpilib
import wpilib.drive
import magicbot

from components.drive import Drive

class MyRobot(magicbot.MagicRobot):
    drive: Drive

    def createObjects(self):
        '''Create motors and stuff here'''
        self.drive_controller = wpilib.XboxController(0)

        self.drive_left_motor = wpilib.Talon(1)
        self.drive_right_motor = wpilib.Talon(2)

        self.gyro = wpilib.AnalogGyro(1)

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        self.drive.tank_drive(-self.drive_controller.getLeftY(), -self.drive_controller.getRightY())

    def robotPeriodic(self):
        '''Called in all modes, good for logging kinds of things'''
        pass