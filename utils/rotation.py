from wpimath import angleModulus
from wpimath.geometry import Rotation2d

def compute_rotational_error_degrees(current_angle: Rotation2d, target_angle: Rotation2d) -> float:
    error_in_degrees = Rotation2d(
        angleModulus((target_angle - current_angle).radians())
    ).degrees()

    return error_in_degrees

