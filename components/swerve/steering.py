from phoenix6.hardware import CANcoder
from rev import CANSparkMax, SparkLimitSwitch
from wpimath.controller import PIDController
from wpimath.geometry import Rotation2d

class SteeringMechanism:
    encoder: CANcoder
    motor: CANSparkMax

    _pid: PIDController
    _target_angle: Rotation2d

    _degrees_per_rotation = 28.1503
    _max_motor_encoder_drift = 1.0


    def __init__(self, motor_can_id, encoder_can_id) -> None:
        self.motor = CANSparkMax(motor_can_id, CANSparkMax.MotorType.kBrushless)
        self.encoder = CANcoder(encoder_can_id)
        self._pid = PIDController(0.2, 0.0, 0.005)
        
        pid = self.motor.getPIDController()
        pid.setP(0.5)
        pid.setI(0.0)
        pid.setIZone(0)
        pid.setD(0.0)
        pid.setFF(0.0)
        pid.setOutputRange(-1, 1)
        # TODO: set status frame timing
        self.motor.setSmartCurrentLimit(45)
        self.motor.setSecondaryCurrentLimit(80)

        self.motor.setOpenLoopRampRate(0.05)
        self.motor.setClosedLoopRampRate(0.02)

        self.motor.setIdleMode(CANSparkMax.IdleMode.kCoast)
        self.motor.enableVoltageCompensation(12.0)
        self.motor.getForwardLimitSwitch(SparkLimitSwitch.Type.kNormallyOpen).enableLimitSwitch(False)
        self.motor.getReverseLimitSwitch(SparkLimitSwitch.Type.kNormallyOpen).enableLimitSwitch(False)

    def get_absolute_encoder_position_degrees(self):
        return Rotation2d.fromDegrees(self.encoder.get_absolute_position() * 360)

    def set_target_angle(self, target_angle):
        self._target_angle = Rotation2d.fromDegrees(target_angle)

    def execute(self):
        error_in_degrees = self._target_angle - self.get_absolute_encoder_position_degrees()
        power = self._pid.calculate(error_in_degrees)
        self.motor.set(power)