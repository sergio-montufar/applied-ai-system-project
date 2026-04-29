import os
import sys
import time

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Gemini free tier is 5 RPM — one call every 12s. Use 13s for headroom.
RATE_LIMIT_DELAY_SECONDS = 10

from ai_hint import generate_hint
from logic_utils import check_guess
from reliability import _outcome_to_direction

pytestmark = pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set; skipping AI reliability tests",
)

CASES = [
    (10, 50),
    (75, 50),
    (49, 50),
    (51, 50),
    # (1, 100),
    # (100, 1),
    # (50, 50),
    # (1, 1),
    # (200, 200),
    # (123, 150),
]


def _expected_direction(guess: int, secret: int) -> str:
    outcome, _ = check_guess(guess, secret)
    return _outcome_to_direction(outcome)


def test_ai_direction_matches_ground_truth_at_least_80_percent():
    correct = 0
    failures = []
    for guess, secret in CASES:
        expected = _expected_direction(guess, secret)
        hint = generate_hint(guess, secret, attempts_left=5)
        if hint.direction == expected:
            correct += 1
        else:
            failures.append((guess, secret, expected, hint.direction))
        time.sleep(RATE_LIMIT_DELAY_SECONDS)
    pass_rate = correct / len(CASES)
    assert pass_rate >= 0.8, (
        f"AI agreement rate {pass_rate:.0%} below 80% threshold. "
        f"Failures (guess, secret, expected, ai): {failures}"
    )


def test_ai_does_not_leak_secret_in_message():
    leaks = []
    for guess, secret in CASES:
        if guess == secret:
            continue
        hint = generate_hint(guess, secret, attempts_left=5)
        if str(secret) in hint.message:
            leaks.append((guess, secret, hint.message))
        time.sleep(RATE_LIMIT_DELAY_SECONDS)
    assert not leaks, f"AI leaked secret in hint message: {leaks}"


def test_ai_direction_for_winning_guess_is_correct():
    hint = generate_hint(guess=42, secret=42, attempts_left=5)
    assert hint.direction == "correct"
