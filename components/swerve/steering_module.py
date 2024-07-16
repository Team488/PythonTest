
from phoenix6.hardware import CANcoder
from rev import CANSparkMax
from wpimath.controller import PIDController

class SteeringModule:
    encoder: CANcoder
    motor: CANSparkMax

    _pid: PIDController
    _target_angle: float = 0

    def __init__(self, motor: CANSparkMax, encoder: CANcoder) -> None:
        self.motor = motor
        self.encoder = encoder
        self._pid = PIDController(0.2, 0, 0.005)

    def set_target_angle(self, target_angle):
        self._target_angle = target_angle

    def execute(self):
        self.motor.set(self._pid.calculate(self.encoder.getAbsolutePosition(), self._target_angle))
