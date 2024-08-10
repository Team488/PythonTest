from rev import CANSparkMax, SparkLimitSwitch, CANSparkLowLevel

class DriveWheel:
    motor: CANSparkMax

    _target_speed: float
    _meters_per_rotation = 0.0532676904732978
    _min_velocity_to_engage_pid = 0.01

    def __init__(self, can_id):
        self._target_speed = 0
        self.motor = CANSparkMax(can_id, CANSparkMax.MotorType.kBrushless)

        self._motor_pid = self.motor.getPIDController()
        self._motor_pid.setP(0.00001)
        self._motor_pid.setI(0.000001)
        self._motor_pid.setIZone(400)
        self._motor_pid.setD(0.0)
        self._motor_pid.setFF(0.00015)
        self._motor_pid.setOutputRange(-1, 1)
        # TODO: set status frame timing
        self.motor.setSmartCurrentLimit(45)
        self.motor.setSecondaryCurrentLimit(80)

        self.motor.setIdleMode(CANSparkMax.IdleMode.kBrake)
        self.motor.enableVoltageCompensation(12.0)
        self.motor.getForwardLimitSwitch(SparkLimitSwitch.Type.kNormallyOpen).enableLimitSwitch(False)
        self.motor.getReverseLimitSwitch(SparkLimitSwitch.Type.kNormallyOpen).enableLimitSwitch(False)

        self.motor_encoder = self.motor.getEncoder()

    def get_current_speed(self):
        return self.motor_encoder.getVelocity() * DriveWheel._meters_per_rotation / 60.0 # convert to m/s from rpm

    def get_current_position(self):
        # AS: What's this used for?
        return self.motor_encoder.getPosition() * DriveWheel._meters_per_rotation

    def set_target_speed(self, target_speed):
        self._target_speed = target_speed

    def execute(self):
        if abs(self._target_speed) < DriveWheel._min_velocity_to_engage_pid:
            # set raw power
            self.motor.set(0)
        else:
            target_speed_rpm = self._target_speed / DriveWheel._meters_per_rotation * 60.0
            self._motor_pid.setReference(target_speed_rpm, CANSparkLowLevel.ControlType.kVelocity, 0)
        
