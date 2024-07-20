import magicbot
from rev import CANSparkMax

class DriveModule:
    motor: CANSparkMax

    _target_speed: float = magicbot.will_reset_to(0.0)

    def __init__(self, can_id):
        self.motor = CANSparkMax(can_id, CANSparkMax.MotorType.kBrushless)

    def set_target_speed(self, target_speed):
        self._target_speed = target_speed

    def execute(self):
        self.motor.set(self._target_speed)
