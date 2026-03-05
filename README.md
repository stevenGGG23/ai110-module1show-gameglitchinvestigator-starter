# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.
- Hard mode is somehow easier than Normal.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app on the default port:
   ```bash
   python -m streamlit run app.py
   ```

   **Or** bind to a specific port (e.g. the Live Server default `5500`):
   ```bash
   python -m streamlit run app.py --server.port 5500
   ```

   Streamlit will print the exact URL it listens on; if you don’t see
   `localhost:5500`, that means it’s still running on the default `8501`.

   You can also set the environment variable `STREAMLIT_SERVER_PORT`:
   ```bash
   export STREAMLIT_SERVER_PORT=5500
   streamlit run app.py
   ```


## 🐛 Known Bugs (Spoilers — try to find them yourself first!)

<details>
<summary>Click to reveal</summary>

| # | File | Bug | Fix |
|---|------|-----|-----|
| 1 | `app.py` | Secret number re-rolls on every rerun | Guard all state init with `if key not in st.session_state` |
| 2 | `app.py` | New Game doesn't clear guess history | Add `st.session_state.history = []` to the New Game handler |
| 3 | `app.py` | Invalid guesses consume an attempt | Refund the attempt counter when `parse_guess` returns an error |
| 4 | `logic_utils.py` | Hard range was `1–50` (easier than Normal's `1–100`) | Changed Hard range to `1–200` |
| 5 | `logic_utils.py` | "Too High" on even attempts rewarded +5 points | Both wrong-guess directions now deduct a flat 5 points |
| 6 | `logic_utils.py` | Misleading `# FIXME` comment on correct hint logic | Removed the comment |

</details>

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask an AI assistant: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong, the difficulty ranges are broken, and scoring is unfair. Fix them.
4. **Refactor & Test.**
   - Confirm all logic lives in `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.

### Game Purpose
This is a number guessing game built with Streamlit. The player picks a difficulty level (Easy, Normal, or Hard), which determines the range of possible numbers and the number of attempts allowed. Each round, a secret number is randomly chosen and the player must guess it within the attempt limit. After each guess, the game provides a hint — "Go Higher" or "Go Lower" — to help narrow it down. Points are awarded for winning and deducted for wrong guesses, with bonus points for winning in fewer attempts.

### Bugs Found

1. **Secret number re-rolled on every rerun** — clicking Submit triggered a Streamlit rerun, which re-executed `random.randint()` and generated a new secret before the guess was even checked.
2. **New Game didn't clear history** — old guesses carried over into the new round because `st.session_state.history` was never reset in the New Game handler.
3. **Hard mode range was smaller than Normal** — `get_range_for_difficulty("Hard")` returned `(1, 50)`, making Hard easier to guess in than Normal's `(1, 100)`.
4. **Score asymmetry** — "Too High" wrong guesses on even-numbered attempts were rewarded +5 points instead of deducted, making the scoring inconsistent.
5. **Misleading FIXME comment** — `check_guess` had a comment implying the hint logic was reversed, but the logic was actually correct, causing unnecessary confusion.

### Fixes Applied

1. **State guards** — wrapped all `st.session_state` initialisation in `if key not in st.session_state` checks so values are only ever set once per session, not on every rerun.
2. **New Game handler** — added `st.session_state.history = []` and `st.session_state.score = 0` to fully reset the game state on a new round.
3. **Hard range corrected** — changed `get_range_for_difficulty("Hard")` to return `(1, 200)` so difficulty scales correctly: Easy (1–20), Normal (1–100), Hard (1–200).
4. **Score fix** — removed the even/odd attempt condition from `update_score`; all wrong guesses now deduct a flat 5 points regardless of direction.
5. **Removed stale comment** — deleted the misleading `# FIXME` comment from `check_guess` since the hint logic was already correct.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]


### 📌 Port configuration

The game itself doesn’t care which port it uses; Streamlit decides it when
it starts.  The instructions above show how to override the default.  The
source code now also displays the current port as an informational message
when the page loads, so you can confirm that the app is running where you
expect.  See the top of `app.py` for the implementation.

## Difficulty Reference

| Difficulty | Range | Attempts |
|------------|-------|----------|
| Easy | 1 – 20 | 10 |
| Normal | 1 – 100 | 7 |
| Hard | 1 – 200 | 5 |