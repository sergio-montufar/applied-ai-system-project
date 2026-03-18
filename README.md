# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.

The game's purpose is to guess a secret number from a range of 1 to 20, 100, or 200 depending on the difficulty. When you check the hint button on, the hint tells you whether your guess is higher or lower than the secret number. You get a score for each attempt made and when you guess the correct number, the game ends, and you receive a score based on the attempts you made.

- [ ] Detail which bugs you found.
I found several bugs including:
   * Hard difficulty being easier than normal
   * Backward hints "Go Higher" is now "Go Lower"
   * Secret being cast to a string on event attempts
   * Score calculation by removing off-by-one on attempt number
   * Attempts initializing to 1 instead of 0
   * Info banner hardcoding "1 and 100" and now uses actual range
   * New Game Button did not actually create new game

- [ ] Explain what fixes you applied.
  * Refactored get_range_for_difficulty, parse_guess, check_guess, and update_score out of app.py and into logic_utils.py
  * Fixed Hard difficulty range (was 1–50, now 1–200)
  * Fixed backwards hints ("Too High" now correctly says "Go LOWER")
  * Fixed secret being cast to a string on even attempts, breaking comparisons
  * Fixed score calculation: removed off-by-one on attempt_number, and fixed "Too High" incorrectly awarding +5 instead of deducting 5
  * Fixed attempts initializing to 1 instead of 0 (off-by-one on display)
  * Fixed info banner hardcoding "1 and 100" — now uses actual difficulty range
  * Fixed New Game button: now resets status and history, and uses correct range
  * Expanded test suite to cover update_score, get_range_for_difficulty, and all check_guess outcomes; fixed unpacking of (result, message) tuples
## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

![Winning Game Screenshot](winning_screenshot.png)


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
