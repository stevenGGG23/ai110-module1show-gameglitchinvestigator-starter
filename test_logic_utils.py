import pytest
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

class TestGetRangeForDifficulty:
    def test_easy_range(self):
        assert get_range_for_difficulty("Easy") == (1, 20)
    def test_normal_range(self):
        assert get_range_for_difficulty("Normal") == (1, 100)
    def test_hard_range(self):
        assert get_range_for_difficulty("Hard") == (1, 200)
    def test_unknown_difficulty_returns_default(self):
        assert get_range_for_difficulty("Impossible") == (1, 100)
    def test_hard_range_larger_than_normal(self):
        _, hard_high = get_range_for_difficulty("Hard")
        _, normal_high = get_range_for_difficulty("Normal")
        assert hard_high > normal_high

class TestParseGuess:
    def test_valid_integer(self):
        ok, val, err = parse_guess("50", 1, 100)
        assert ok and val == 50 and err is None
    def test_valid_lower_boundary(self):
        ok, val, _ = parse_guess("1", 1, 100)
        assert ok and val == 1
    def test_valid_upper_boundary(self):
        ok, val, _ = parse_guess("100", 1, 100)
        assert ok and val == 100
    def test_decimal_truncated(self):
        ok, val, _ = parse_guess("7.9", 1, 100)
        assert ok and val == 7
    def test_empty_string(self):
        ok, val, err = parse_guess("", 1, 100)
        assert not ok and err is not None
    def test_none_input(self):
        ok, val, err = parse_guess(None, 1, 100)
        assert not ok and err is not None
    def test_negative_number(self):
        ok, _, err = parse_guess("-1", 1, 100)
        assert not ok and err is not None
    def test_above_range(self):
        ok, _, err = parse_guess("101", 1, 100)
        assert not ok and err is not None
    def test_extremely_large_value(self):
        ok, _, err = parse_guess("999999999", 1, 100)
        assert not ok and err is not None
    def test_letters(self):
        ok, _, err = parse_guess("abc", 1, 100)
        assert not ok and err is not None

class TestCheckGuess:
    def test_correct_guess(self):
        outcome, _ = check_guess(50, 50)
        assert outcome == "Win"
    def test_guess_too_high(self):
        outcome, msg = check_guess(80, 50)
        assert outcome == "Too High" and "LOWER" in msg.upper()
    def test_guess_too_low(self):
        outcome, msg = check_guess(20, 50)
        assert outcome == "Too Low" and "HIGHER" in msg.upper()

class TestUpdateScore:
    def test_win_on_first_attempt(self):
        assert update_score(0, "Win", 1) == 100
    def test_win_score_minimum_is_10(self):
        assert update_score(0, "Win", 100) == 10
    def test_too_high_deducts_5(self):
        assert update_score(50, "Too High", 1) == 45
    def test_too_low_deducts_5(self):
        assert update_score(50, "Too Low", 1) == 45
    def test_too_high_even_attempt_still_deducts(self):
        assert update_score(50, "Too High", 2) == 45
    def test_unknown_outcome_unchanged(self):
        assert update_score(50, "Unknown", 1) == 50
