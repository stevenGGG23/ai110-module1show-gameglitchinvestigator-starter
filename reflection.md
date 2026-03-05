# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the app, the game appeared to work on the surface — the UI loaded, the input box accepted numbers, and the buttons responded. However, the secret number was regenerating every time I clicked Submit, which made it impossible to actually win because the target kept moving. Two concrete bugs I noticed right away were that the secret number kept changing on every button click, and the difficulty ranges were wrong — Hard mode had a smaller range (1–50) than Normal (1–100), which made it easier, not harder. I also noticed that the score behaved strangely, sometimes going up after a wrong guess depending on which attempt number I was on.

---

## 2. How did you use AI as a teammate?

I used Claude as my primary AI tool throughout this project to help identify bugs, explain Streamlit behavior, and generate fixes. One example of a correct suggestion was when I asked why the secret number kept changing — Claude correctly explained that Streamlit reruns the entire script on every interaction, so any variable assigned outside of `st.session_state` gets reset, and it suggested wrapping all initializations in `if key not in st.session_state` guards, which I verified by opening the Debug Info panel and confirming the secret stayed stable across multiple submissions. One misleading moment was when the `# FIXME` comment in `check_guess` implied the hint logic was reversed — I initially assumed the hints were broken and spent time investigating, but after tracing through the logic manually I confirmed that `guess > secret → Go LOWER` was actually correct and the comment was just a leftover artifact. That taught me not to trust comments as documentation without verifying the actual code behavior.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed when I could reproduce the original broken behavior, apply the fix, and then no longer trigger the same issue through normal gameplay. For the state bug specifically, I manually tested by opening the Developer Debug Info panel, noting the secret number, submitting a guess, and checking whether the secret changed — before the fix it changed every time, and after the fix it stayed the same for the entire round. I also ran `pytest` on `logic_utils.py` to verify that `check_guess`, `parse_guess`, and `update_score` all returned the expected values for known inputs, which caught the scoring asymmetry bug that I had initially missed just from playing the game. Claude helped me understand what to assert in the tests by explaining what each function was supposed to return for edge cases like guessing exactly at the boundary of the range.

---

## 4. What did you learn about Streamlit and state?

The secret number kept changing because Streamlit re-executes the entire Python script from top to bottom every time a user interacts with the app — clicking a button, typing in a field, or changing a selectbox all trigger a full rerun. In the original code, `random.randint()` was called outside any guard, so each rerun generated a brand new secret before the guess was even evaluated. I would explain it to a friend like this: imagine every button click refreshes the whole page, and any variable you set only lasts until the next refresh — `st.session_state` is like a notepad that survives the refresh so you can read what you wrote last time. The fix that stabilized the secret was wrapping the initialization in `if "secret" not in st.session_state`, so the random number is only generated once and then stored in session state for the rest of the game.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is reading the code independently before trusting any AI explanation or comment — in this project, the `# FIXME` comment sent me in the wrong direction and only manual tracing through the logic revealed the truth. Next time I work with AI on a coding task, I would ask it to explain *why* a fix works, not just what to change, so I can verify the reasoning rather than copy-pasting blindly. This project changed how I think about AI-generated code — I came in expecting it to mostly work and just need polish, but I found that AI code can have subtle, compounding bugs that only appear when the pieces interact, so treating it like unreviewed code from a junior developer is the right mindset.

---

## Challenge 5: AI Model Comparison

**Bug tested:** The secret number re-rolling on every Submit click (the Streamlit state bug).

**Claude's fix:** Claude explained that Streamlit reruns the entire script on every interaction, so any variable assigned at the top level gets a fresh value each run. It suggested wrapping all `st.session_state` initialization in `if key not in st.session_state` guards and explained *why* this works — because session state persists across reruns while regular variables do not. The explanation was clear and connected the fix directly to how Streamlit's execution model works.

**ChatGPT's fix:** ChatGPT gave a similar correct fix — also suggesting `st.session_state` guards — but jumped straight to the code change without explaining the underlying rerun mechanism first. The fix worked, but without understanding why, it would be easy to make the same mistake again in a different context.

**Comparison:** Both models produced a working fix. Claude's answer was more useful for learning because it explained the *why* behind the solution, not just the *what*. ChatGPT's response was faster to skim if you just needed the code. For someone new to Streamlit, Claude's explanation would build better mental models; for an experienced developer who just needs a quick fix, ChatGPT's concise answer is efficient. The key takeaway is that the better model depends on your goal — understanding vs. speed.