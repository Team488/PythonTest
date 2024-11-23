import ntcore
from phoenix6.hardware import CANcoder
from rev import CANSparkMax, SparkLimitSwitch
from wpimath.controller import PIDController
from wpimath.geometry import Rotation2d

from utils.rotation import compute_rotational_error_degrees



class SteeringMechanism:
    encoder: CANcoder
    motor: CANSparkMax

    _pid: PIDController
    _target_angle: Rotation2d

    _degrees_per_rotation = 28.1503
    _max_motor_encoder_drift = 1.0

    def __init__(self, motor_can_id, encoder_can_id, prefix) -> None:
        self.prefix = prefix
        self._target_angle = Rotation2d(0)
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
        self.motor.getForwardLimitSwitch(
            SparkLimitSwitch.Type.kNormallyOpen
        ).enableLimitSwitch(False)
        self.motor.getReverseLimitSwitch(
            SparkLimitSwitch.Type.kNormallyOpen
        ).enableLimitSwitch(False)

        nt = ntcore.NetworkTableInstance.getDefault().getTable(
            "/components/drive/" + prefix
        )
        module_states_table = nt.getSubTable("steering")
        self.target_angle_publisher = module_states_table.getDoubleTopic(
            "target"
        ).publish()
        self.current_angle_publisher = module_states_table.getDoubleTopic(
            "current"
        ).publish()
        self.current_power_publisher = module_states_table.getDoubleTopic(
            "output"
        ).publish()

        self.scaled_error_publisher = module_states_table.getDoubleTopic(
            "scaled_error"
        ).publish()
        self.error_publisher = module_states_table.getDoubleTopic("error").publish()

    def get_absolute_encoder_position(self) -> Rotation2d:
        return Rotation2d.fromDegrees(self.encoder.get_absolute_position().value * 360)

    def set_target_angle(self, target_angle: Rotation2d):
        self._target_angle = target_angle

    def execute(self):
        error_in_degrees = compute_rotational_error_degrees(
            self._target_angle, self.get_absolute_encoder_position()
        )
        scaled_error = error_in_degrees / 90.0
        if scaled_error < -1:
            scaled_error = -1
        if scaled_error > 1:
            scaled_error = 1

        power = self._pid.calculate(scaled_error, 0)

        self.scaled_error_publisher.set(scaled_error)
        self.error_publisher.set(error_in_degrees)
        self.current_angle_publisher.set(
            self.get_absolute_encoder_position().degrees()
        )
        self.target_angle_publisher.set(self._target_angle.degrees())
        self.current_power_publisher.set(power)

        self.motor.set(power)
