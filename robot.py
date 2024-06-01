import wpilib
import wpilib.drive
import magicbot

class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        '''Create motors and stuff here'''
        self.lstick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)

        self.drive_left_motor = wpilib.Talon(1)
        self.drive_right_motor = wpilib.Talon(2)
        self.drive = wpilib.drive.DifferentialDrive(self.drive_left_motor, self.drive_right_motor)

        self.gyro = wpilib.AnalogGyro(1)

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        pass

    def teleopPeriodic(self):
        self.drive.arcadeDrive(-self.lstick.getY(), self.lstick.getX())

        wpilib.SmartDashboard.putNumber("Gyro", self.gyro.getAngle())
