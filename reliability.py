import json
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

from ai_hint import Hint, generate_hint
from logic_utils import check_guess

LOG_DIR = Path(__file__).parent / "logs"
LOG_PATH = LOG_DIR / "ai_failures.jsonl"


class VerifiedHint(NamedTuple):
    message: str
    source: str
    ai_agreed: bool


def _outcome_to_direction(outcome: str) -> str:
    if outcome == "Win":
        return "correct"
    if outcome == "Too High":
        return "lower"
    if outcome == "Too Low":
        return "higher"
    return "unknown"


def get_verified_hint(guess: int, secret: int, attempts_left: int) -> VerifiedHint:
    """
    Generate an AI hint, verify against deterministic ground truth, and return
    a VerifiedHint. Falls back to the deterministic message on mismatch or error.
    """
    outcome, fallback_message = check_guess(guess, secret)
    expected_direction = _outcome_to_direction(outcome)

    try:
        hint = generate_hint(guess, secret, attempts_left)
    except Exception as exc:
        _log_failure(
            {
                "kind": "exception",
                "error": repr(exc),
                "guess": guess,
                "secret": secret,
            }
        )
        return VerifiedHint(fallback_message, "fallback", False)

    if hint.direction != expected_direction:
        _log_failure(
            {
                "kind": "direction_mismatch",
                "guess": guess,
                "secret": secret,
                "expected_direction": expected_direction,
                "ai_direction": hint.direction,
                "ai_message": hint.message,
            }
        )
        return VerifiedHint(fallback_message, "fallback", False)

    if str(secret) in hint.message:
        _log_failure(
            {
                "kind": "secret_leak",
                "guess": guess,
                "secret": secret,
                "ai_message": hint.message,
            }
        )
        return VerifiedHint(fallback_message, "fallback", False)

    return VerifiedHint(hint.message, "ai", True)


def _log_failure(payload: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    payload["timestamp"] = datetime.now(timezone.utc).isoformat()
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(payload) + "\n")
