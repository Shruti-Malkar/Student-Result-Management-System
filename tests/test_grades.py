import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services import calculate_percentage, calculate_grade, validate_marks


def test_percentage_calculates_correctly():
    """Percentage should be average of 3 subjects."""
    assert calculate_percentage(90, 80, 70) == 80.0


def test_percentage_rounds_to_two_decimals():
    """Percentage should be rounded to 2 decimal places."""
    result = calculate_percentage(85, 90, 92)
    assert result == round(result, 2)


def test_grade_A_plus_for_90_and_above():
    assert calculate_grade(90) == "A+"
    assert calculate_grade(100) == "A+"
    assert calculate_grade(95.5) == "A+"


def test_grade_A_for_80_to_89():
    assert calculate_grade(80) == "A"
    assert calculate_grade(85) == "A"
    assert calculate_grade(89.9) == "A"


def test_grade_B_for_70_to_79():
    assert calculate_grade(70) == "B"
    assert calculate_grade(75) == "B"


def test_grade_C_for_60_to_69():
    assert calculate_grade(60) == "C"
    assert calculate_grade(65) == "C"


def test_grade_D_for_50_to_59():
    assert calculate_grade(50) == "D"
    assert calculate_grade(55) == "D"


def test_grade_F_below_50():
    assert calculate_grade(49) == "F"
    assert calculate_grade(0) == "F"


def test_validate_marks_raises_for_marks_above_100():
    with pytest.raises(ValueError):
        validate_marks(101, 50, 50)


def test_validate_marks_raises_for_negative_marks():
    with pytest.raises(ValueError):
        validate_marks(-1, 50, 50)


def test_validate_marks_passes_for_valid_input():
    # Should not raise any exception
    validate_marks(0, 50, 100)
