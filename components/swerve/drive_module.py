from rev import CANSparkMax

class DriveModule:
    motor: CANSparkMax

    _target_speed: float = 0

    def set_target_speed(self, target_speed):
        self._target_speed = target_speed

    def execute(self):
        self.motor.set(self._target_speed)
