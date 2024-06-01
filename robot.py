import wpilib
import magicbot

class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        '''Create motors and stuff here'''
        self.drive_left = wpilib.Talon(1)
        self.drive_right = wpilib.Talon(2)


    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        pass
