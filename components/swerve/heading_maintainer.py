import math
from components.swerve.drive import Drive
import magicbot
import navx
import ntcore
from utils.rotation import compute_rotational_error_degrees
from wpimath.controller import PIDController
from wpimath.geometry import Rotation2d, Translation2d


class HeadingMaintainer:
    drive: Drive
    imu: navx.AHRS

    heading_intent = magicbot.will_reset_to(Rotation2d(0))

    heading_pid_p = magicbot.tunable(4.0)

    def setup(self):
        self.nt = ntcore.NetworkTableInstance.getDefault().getTable("/components/heading_maintainer")
        self.heading_pid = self._pid = PIDController(self.heading_pid_p, 0.0, 0.0)
        self.target_heading = self.imu.getRotation2d()

    def apply_heading(self, heading_intent: Translation2d):
        if abs(heading_intent) > 0.8:
            self.target_heading = heading_intent.angle()
            print(f"Updating target_heading to {self.target_heading}")

    def execute(self):
        current_heading = self.imu.getRotation2d()
        heading_error = compute_rotational_error_degrees(current_heading, self.target_heading)
        # PID to our target heading
        omega = -math.radians(self.heading_pid.calculate(heading_error))
        self.drive.set_rotation(omega)

    def publish_data(self):
        self.nt.putNumber("targetHeadingDeg", self.target_heading.degrees())