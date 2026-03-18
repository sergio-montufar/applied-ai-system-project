# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  The game looked like a basic guessing game where you guess a number between 1 and 100 with 7 attempts left.
  There is a developer debug info which tells you the secret number, the amount of attempts you made, and your score.
  There is a text box to enter your guess and right under it there's buttons in a row 
  where you submit your guess, make a new game, and show a hint.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

  The hint button does tells you to go higher when lower or vice versa.
  You cannot submit new guesses after the game is finished.
  
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude as my AI tool.
An AI suggestion that was correct was to change "Too High, Go Higher" to say "Too High, Go Lower" and vice versa. I verified the result by guessing a higher number than the secret and it gave the correct hint.

An AI suggestion that was misleading was to create a new file to run code in the testing file when I just wanted it to be in the same file

---


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided a bug was really fixed when the pytest that was made for it ran without failing

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  A test that I ran was checking the guess message and whether it showed the correct message when guessing higher or lower. 

- Did AI help you design or understand any tests? How?
AI did help me design tests since it made it easier to understand what to actually test for.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

The original bug was that the secret was regenerated on every rerun because the if "secret" not in st.session_state guard was missing or the secret was being reset unconditionally on each script execution, meaning every interaction caused Streamlit to re-run the script and pick a new random number.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time a user interacts with a Streamlit app, the entire script reruns from scratch, meaning normal variables reset and disappear. Session state is a persistent dictionary that survives those reruns, letting you hold onto things like a secret number across button clicks.

- What change did you make that finally gave the game a stable secret number?

The fix was wrapping the secret number generation in an if "secret" not in st.session_state guard, so it only runs once on the very first load instead of every rerun. This stores the secret in st.session_state, where it persists across all subsequent reruns until the user explicitly starts a new game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

  I want to reuse the habit of testing since it is very useful to do for stuff like this.

- What is one thing you would do differently next time you work with AI on a coding task?

I would make sure to check everything the AI does before it changes any code in any file.


- In one or two sentences, describe how this project changed the way you think about AI generated code.

It changed the way I think about AI generated code by making sure everything is correct and to not blindly trust it.