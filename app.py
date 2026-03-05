"""
app.py
~~~~~~
Glitchy Guesser — fixed and enhanced Streamlit app.
Challenge 2: High score tracker persisted across rounds via session state.
Challenge 4: Color-coded hints, hot/cold proximity emojis, session summary table.
"""

import os
import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

# show the port to make it easier to verify when the app is launched
port = os.environ.get("STREAMLIT_SERVER_PORT") or "8501"
st.info(f"Running on port {port}. (Start with `--server.port 5500` to change.)")

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Glitchy Guesser")
st.caption("A number guessing game — now actually winnable.")

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.header("⚙️ Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {"Easy": 10, "Normal": 7, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# ── Session State Init ────────────────────────────────────────────────────────

if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = difficulty

# Reset game when difficulty changes.
if st.session_state.current_difficulty != difficulty:
    st.session_state.current_difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

if "secret"     not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts"   not in st.session_state:
    st.session_state.attempts = 0
if "score"      not in st.session_state:
    st.session_state.score = 0
if "status"     not in st.session_state:
    st.session_state.status = "playing"
if "history"    not in st.session_state:
    st.session_state.history = []

# Challenge 2: High score tracker — persists across rounds, resets only on
# page refresh (not on New Game), so players can chase their personal best.
if "high_score" not in st.session_state:
    st.session_state.high_score = 0

# ── Helper: proximity emoji (Challenge 4) ─────────────────────────────────────

def proximity_emoji(guess: int, secret: int, rng: int) -> str:
    """Return a hot/cold emoji based on how close the guess is to the secret."""
    distance = abs(guess - secret)
    ratio = distance / rng
    if ratio <= 0.05:
        return "🔥 Scorching!"
    if ratio <= 0.15:
        return "♨️ Very warm"
    if ratio <= 0.30:
        return "😐 Lukewarm"
    if ratio <= 0.50:
        return "🧊 Cold"
    return "❄️ Freezing!"

# ── High Score Sidebar (Challenge 2) ─────────────────────────────────────────

st.sidebar.divider()
st.sidebar.subheader("🏆 High Score")
st.sidebar.metric("Best score", st.session_state.high_score)
st.sidebar.caption("Persists across rounds until you close the tab.")

# ── Debug Panel ───────────────────────────────────────────────────────────────

with st.expander("🛠️ Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# ── Attempts Bar (Challenge 4) ────────────────────────────────────────────────

attempts_left = attempt_limit - st.session_state.attempts
bar_ratio = attempts_left / attempt_limit
st.subheader("Make a guess")
st.progress(bar_ratio, text=f"Attempts remaining: {attempts_left} / {attempt_limit}")

st.info(f"Guess a number between **{low}** and **{high}**.")

# ── Input & Buttons ───────────────────────────────────────────────────────────

raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.success("New game started!")
    st.rerun()

# ── Game Over Guard ───────────────────────────────────────────────────────────

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("🎉 You already won! Start a new game to play again.")
    else:
        st.error("💀 Game over. Start a new game to try again.")
    st.stop()

# ── Guess Submission ──────────────────────────────────────────────────────────

if submit:
    if not raw_guess or raw_guess.strip() == "":
        st.error("Enter a guess before submitting.")
    else:
        ok, guess_int, err = parse_guess(raw_guess, low, high)

        if not ok:
            st.session_state.history.append(raw_guess)
            st.error(err)
        else:
            st.session_state.attempts += 1
            st.session_state.history.append(guess_int)

            outcome, message = check_guess(guess_int, st.session_state.secret)

            # Challenge 4: color-coded feedback + proximity emoji
            if show_hint:
                if outcome == "Win":
                    st.success(message)
                elif outcome == "Too High":
                    prox = proximity_emoji(guess_int, st.session_state.secret, high - low)
                    st.error(f"📉 Go LOWER!  {prox}")
                else:
                    prox = proximity_emoji(guess_int, st.session_state.secret, high - low)
                    st.warning(f"📈 Go HIGHER!  {prox}")

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"
                # Challenge 2: update high score if beaten
                if st.session_state.score > st.session_state.high_score:
                    st.session_state.high_score = st.session_state.score
                    st.toast("🏆 New high score!", icon="🏆")
                st.success(
                    f"🎉 You won! The secret was **{st.session_state.secret}**. "
                    f"Final score: **{st.session_state.score}**"
                )

            elif st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"💀 Out of attempts! "
                    f"The secret was **{st.session_state.secret}**. "
                    f"Score: **{st.session_state.score}**"
                )

# ── Session Summary Table (Challenge 4) ──────────────────────────────────────

if st.session_state.history:
    st.divider()
    st.subheader("📋 Guess History")
    rows = []
    for i, g in enumerate(st.session_state.history, 1):
        if isinstance(g, int):
            if g == st.session_state.secret:
                direction = "✅ Correct!"
            elif g > st.session_state.secret:
                direction = "📉 Too High"
            else:
                direction = "📈 Too Low"
            prox = proximity_emoji(g, st.session_state.secret, high - low)
        else:
            direction = "❌ Invalid"
            prox = "—"
        rows.append({"#": i, "Guess": g, "Result": direction, "Proximity": prox})
    st.table(rows)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")