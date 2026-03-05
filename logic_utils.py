"""
logic_utils.py
~~~~~~~~~~~~~~
Pure-logic helpers for the Glitchy Guesser Streamlit app.
All functions are stateless and fully covered by test_logic_utils.py.
"""


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a given difficulty.

    Ranges are intentionally scaled so that a harder difficulty always has
    a larger search space, making guessing objectively more challenging.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple (low, high) representing the inclusive guessing range.
        Defaults to (1, 100) for any unrecognised difficulty string.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 200)
    """
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 200),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str, low: int, high: int) -> tuple[bool, int | None, str | None]:
    """Parse and validate raw user input into an integer guess.

    Handles None, empty strings, whitespace, decimals, non-numeric text,
    and out-of-range values without raising exceptions.

    Args:
        raw: The raw string entered by the user.
        low: The inclusive lower bound of the valid range.
        high: The inclusive upper bound of the valid range.

    Returns:
        A three-tuple (ok, guess_int, error_message) where:
            - ok (bool): True if the input is valid.
            - guess_int (int | None): The parsed integer, or None if invalid.
            - error_message (str | None): A human-readable error, or None if valid.

    Examples:
        >>> parse_guess("42", 1, 100)
        (True, 42, None)
        >>> parse_guess("abc", 1, 100)
        (False, None, 'That is not a number.')
    """
    if not raw or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    if not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare a guess to the secret number and return an outcome with a hint.

    Args:
        guess: The player's integer guess.
        secret: The secret integer the player is trying to identify.

    Returns:
        A two-tuple (outcome, message) where outcome is one of:
            - "Win"      — guess matches secret.
            - "Too High" — guess is above the secret.
            - "Too Low"  — guess is below the secret.
        message is a short emoji-prefixed hint string for display.

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(80, 50)
        ('Too High', '📉 Go LOWER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return an updated score based on the guess outcome.

    Winning awards between 10 and 100 points depending on how quickly the
    player guessed. Wrong guesses always deduct 5 points regardless of
    direction, keeping scoring fair and predictable.

    Args:
        current_score: The player's score before this guess.
        outcome: The result string from check_guess — "Win", "Too High",
                 "Too Low", or any other string (treated as no-op).
        attempt_number: The 1-based index of the current attempt.

    Returns:
        The updated integer score.

    Examples:
        >>> update_score(0, "Win", 1)
        100
        >>> update_score(50, "Too High", 3)
        45
    """
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score