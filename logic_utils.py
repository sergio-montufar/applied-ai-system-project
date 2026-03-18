def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    #FIX: Refactored logic into logic_utils.py using Claude Agent mode
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # FIX: Fixed difficulty being too easy (was 50, now 200)
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    #FIX: Refactored logic into logic_utils.py using Claude Agent mode
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    #FIX: Refactored logic into logic_utils.py using Claude Agent mode
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    #FIX: Refactored logic into logic_utils.py using Claude Agent mode
    if outcome == "Win":
        # FIX: Attempt_number is already at current attempt, no need to increase it
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIX: "Too High" gives +5 points instead of -5 points like "Too Low"
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
