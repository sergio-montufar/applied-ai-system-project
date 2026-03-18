import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, message = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, message = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, message  = check_guess(40, 50)
    assert result == "Too Low"


def test_update_score_win_attempt_1():
    # Win on attempt 1: points = 100 - 10 * 1 = 90
    assert update_score(0, "Win", 1) == 90

def test_update_score_win_minimum_points():
    # Win on attempt 10: 100 - 10*10 = 0, clamped to 10
    assert update_score(0, "Win", 10) == 10

def test_update_score_too_high():
    # Too High should always deduct 5
    assert update_score(50, "Too High", 1) == 45
    assert update_score(50, "Too High", 2) == 45

def test_update_score_too_low():
    # Too Low should deduct 5
    assert update_score(50, "Too Low", 1) == 45

def test_update_score_unknown_outcome():
    # Unknown outcome leaves score unchanged
    assert update_score(50, "Unknown", 1) == 50


def test_get_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_get_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_get_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 200)

def test_get_range_unknown_defaults_to_normal():
    assert get_range_for_difficulty("Unknown") == (1, 100)
