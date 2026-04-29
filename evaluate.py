"""
AI Hint Reliability Evaluation Script

Runs the AI Hint Coach over a set of predefined (guess, secret) cases and
prints a human-readable summary: per-case pass/fail, agreement rate,
secret-leak count, and overall verdict.

Usage:
    python3 evaluate.py
"""
import os
import sys
import time

from dotenv import load_dotenv

from ai_hint import generate_hint
from logic_utils import check_guess
from reliability import _outcome_to_direction

load_dotenv()

CASES = [
    (10, 50),
    (75, 50),
    (49, 50),
    (51, 50),
    (1, 100),
    (100, 1),
    (50, 50),
    (1, 1),
    (200, 200),
    (123, 150),
]

RATE_LIMIT_DELAY_SECONDS = 13
AGREEMENT_THRESHOLD = 0.80


def main() -> int:
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: GEMINI_API_KEY is not set. Copy .env.example to .env and add your key.")
        return 1

    print(f"Running AI Hint Reliability evaluation over {len(CASES)} cases.")
    print(f"Pacing calls at {RATE_LIMIT_DELAY_SECONDS}s to stay under Gemini free-tier 5 RPM limit.\n")
    print(f"{'#':>3}  {'STATUS':<6}  {'guess':>5}  {'secret':>6}  {'expected':<8}  {'ai':<8}  {'latency':>7}")
    print("-" * 70)

    direction_correct = 0
    leaks = 0
    errors = 0
    failure_details: list[str] = []

    for i, (guess, secret) in enumerate(CASES, start=1):
        outcome, _ = check_guess(guess, secret)
        expected = _outcome_to_direction(outcome)

        try:
            t0 = time.monotonic()
            hint = generate_hint(guess, secret, attempts_left=5)
            latency = time.monotonic() - t0

            direction_match = hint.direction == expected
            leaked = guess != secret and str(secret) in hint.message

            if direction_match:
                direction_correct += 1
            if leaked:
                leaks += 1

            if direction_match and not leaked:
                status = "PASS"
            else:
                status = "FAIL"
                if not direction_match:
                    failure_details.append(
                        f"  [#{i}] direction mismatch: expected={expected}, ai={hint.direction}, "
                        f"message='{hint.message}'"
                    )
                if leaked:
                    failure_details.append(
                        f"  [#{i}] secret leak: secret={secret} appears in message='{hint.message}'"
                    )

            print(
                f"{i:>3}  {status:<6}  {guess:>5}  {secret:>6}  {expected:<8}  "
                f"{hint.direction:<8}  {latency:>6.2f}s"
            )

        except Exception as exc:
            errors += 1
            print(f"{i:>3}  {'ERROR':<6}  {guess:>5}  {secret:>6}  {expected:<8}  {'-':<8}  {'-':>7}")
            failure_details.append(f"  [#{i}] {type(exc).__name__}: {exc}")

        if i < len(CASES):
            time.sleep(RATE_LIMIT_DELAY_SECONDS)

    successful_calls = len(CASES) - errors
    agreement_rate = direction_correct / successful_calls if successful_calls else 0.0

    print("\n=== Summary ===")
    print(f"Total cases:           {len(CASES)}")
    print(f"Successful API calls:  {successful_calls}/{len(CASES)}")
    print(f"Direction agreement:   {direction_correct}/{successful_calls} ({agreement_rate:.0%})")
    print(f"Secret leaks:          {leaks}")
    print(f"API errors:            {errors}")

    if failure_details:
        print("\n=== Failure details ===")
        for detail in failure_details:
            print(detail)

    overall_pass = (
        successful_calls > 0
        and agreement_rate >= AGREEMENT_THRESHOLD
        and leaks == 0
    )

    print(
        f"\nOVERALL: {'PASS' if overall_pass else 'FAIL'} "
        f"(agreement >= {AGREEMENT_THRESHOLD:.0%}, no leaks, at least one successful call)"
    )

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
