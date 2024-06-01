import wpilib
import magicbot

class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        '''Create motors and stuff here'''
        self.lstick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)


        self.drive_left = wpilib.Talon(1)
        self.drive_right = wpilib.Talon(2)

        self.drive = wpilib.drive.DifferentialDrive(self.drive_left, self.drive_right)


    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        self.drive.arcadeDrive(-self.lstick.getY(), self.lstick.getX())
