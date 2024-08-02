import magicbot
from rev import CANSparkMax, SparkLimitSwitch, CANSparkLowLevel

class DriveWheel:
    motor: CANSparkMax

    _target_speed: float = magicbot.will_reset_to(0.0)
    _meters_per_rotation = 0.0532676904732978
    _min_velocity_to_engage_pid = 0.01

    def __init__(self, can_id):
        self.motor = CANSparkMax(can_id, CANSparkMax.MotorType.kBrushless)
        pid = self.motor.getPIDController()
        pid.setP(0.00001)
        pid.setI(0.000001)
        pid.setIZone(400)
        pid.setD(0.0)
        pid.setFF(0.00015)
        pid.setOutputRange(-1, 1)
        # TODO: set status frame timing
        self.motor.setSmartCurrentLimit(45)
        self.motor.setSecondaryCurrentLimit(80)

        self.motor.setIdleMode(CANSparkMax.IdleMode.kBrake)
        self.motor.enableVoltageCompensation(12.0)
        self.motor.getForwardLimitSwitch(SparkLimitSwitch.Type.kNormallyOpen).enableLimitSwitch(False)
        self.motor.getReverseLimitSwitch(SparkLimitSwitch.Type.kNormallyOpen).enableLimitSwitch(False)

    def get_current_speed(self):
        return self.motor.getEncoder().getVelocity() * DriveWheel._meters_per_rotation / 60.0 # convert to m/s from rpm

    def get_current_position(self):
        return self.motor.getEncoder().getPosition() * DriveWheel._meters_per_rotation

    def set_target_speed(self, target_speed):
        self._target_speed = target_speed

    def execute(self):
        if abs(self._target_speed) < DriveWheel._min_velocity_to_engage_pid:
            # set raw power
            self.motor.set(0)
        else:
            target_speed_rpm = self._target_speed / DriveWheel._meters_per_rotation * 60.0
            self.motor.getPIDController().setReference(target_speed_rpm, CANSparkLowLevel.ControlType.kVelocity, 0)
        