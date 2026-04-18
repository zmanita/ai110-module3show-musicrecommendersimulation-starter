# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

real-world recommendations  use both collaborative filtering (using other users' behavior) and content-based filtering (using song attributes).
Some features that each `Song` uses in my system: genre, mood, artist, energy, tempo_bpm, valence, danceability, acousticness
My `UserProfile` stores history of genre and mood for each user. 
`Recommender` computes a score for each song via combining song attributes (such as genre, mood, energy, tempo) and user preference with mathmatical operations. 

**Algorithm Recipe & Bias Note:** For each song in the CSV, the system adds bonus points for a genre match and a mood match (both binary), then subtracts the numerical distance between the song's energy, tempo, valence, and danceability and the user's targets — the song with the highest combined score wins. The clearest risk is genre over-prioritization: because genre is all-or-nothing, a song that perfectly matches the user's energy and mood but sits in a neighboring genre (e.g., "indie pop" vs. "pop") can be outranked by a mediocre same-genre track, causing the system to miss great recommendations that a real listener would enjoy.

![Music Recommender Simulation Screenshot](Screenshot%202026-04-16%20at%204.24.10%20PM.png)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

**GENRE_SUPREMACY** — metal genre + peaceful mood + calm numerical targets. Illustrates how a strong genre match can override mood and energy signals.

![GENRE_SUPREMACY profile run](Screenshot%202026-04-17%20at%204.06.46%E2%80%AFPM.png)

**NO_GENRE_MATCH** — k-pop genre not present in catalog. Shows how the system falls back to numerical attribute distances when no genre bonus is available.

![NO_GENRE_MATCH profile run](Screenshot%202026-04-17%20at%204.07.36%E2%80%AFPM.png)

**ACOUSTIC_GHOST** — `likes_acoustic=True` field is present in the profile but never used in scoring. Highlights a feature that exists in the data but is silently ignored by the algorithm.

![ACOUSTIC_GHOST profile run](Screenshot%202026-04-17%20at%204.08.09%E2%80%AFPM.png)

**TEMPO_EXTREMIST** — target tempo of 268 bpm, beyond the catalog maximum of 168 bpm. Demonstrates edge-case behavior when user targets fall outside the data range.

![TEMPO_EXTREMIST profile run](Screenshot%202026-04-17%20at%204.08.45%E2%80%AFPM.png)

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

The most concrete thing I learned is how much leverage a single number has in a formula like this. The genre bonus I settled on (+3.0 points) is large enough that it overrides almost every other signal — a genre match beats a mood match, and a near-perfect numerical fit from a different genre. That is a bias baked into the design, not the data, and it shows up immediately when you test an edge case like a metal fan whose catalog has only one metal song. The system does not fail gracefully; it just fills the remaining slots with whatever numbers happen to be closest. Seeing that behavior helped me understand why real recommenders rely on so many more signals than a hand-tuned rule.

I also found that the way results are *presented* shapes how intelligent the system seems. Printing a full score breakdown — genre match, mood match, each numerical gap — makes the output feel reasoned and trustworthy even though the underlying math is simple subtraction. That gap between what an algorithm actually does and what a user believes it understands is where a lot of AI fairness problems live. If the explanation sounds confident, users tend to trust the output without questioning the assumptions behind the weights.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

