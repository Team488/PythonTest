

import pytest
from wpimath.geometry import Rotation2d

from components.swerve.steering import compute_error


def test_compute_error__zero():
    assert compute_error(Rotation2d(0), Rotation2d(0)) == 0

def test_compute_error__slight_positive_error():
    assert compute_error(Rotation2d.fromDegrees(90), Rotation2d.fromDegrees(95)) == pytest.approx(5.0)

def test_compute_error__slight_negative_error():
    assert compute_error(Rotation2d.fromDegrees(90), Rotation2d.fromDegrees(85)) == pytest.approx(-5.0)

def test_compute_error__wrap_180():
    assert compute_error(Rotation2d.fromDegrees(179), Rotation2d.fromDegrees(-179)) == pytest.approx(2.0)

def test_compute_error__wrap_180_negative():
    assert compute_error(Rotation2d.fromDegrees(-179), Rotation2d.fromDegrees(179)) == pytest.approx(-2.0)