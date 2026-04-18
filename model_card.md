# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SongMatch 1.0**

---

## 2. Intended Use  

SongMatch 1.0 recommends songs from a small catalog based on a user's stated taste preferences.

- It generates a ranked top-5 list of songs for a single user profile at a time.
- It assumes the user knows their favorite genre, favorite mood, and rough numerical targets for energy, tempo, valence, and danceability.
- This is a classroom simulation — it is not meant for real-world deployment or real user data.

---

## 3. How the Model Works  

Every song starts with a score of zero. The system then adjusts that score in two ways.

First, it checks two yes-or-no questions: does the song's genre match the user's favorite genre? Does the song's mood match the user's favorite mood? A genre match adds 3 points; a mood match adds 2 points. These are the biggest boosts in the whole system.

Second, it looks at four numbers — energy, tempo, valence (how positive the song sounds), and danceability. For each one, it measures how far the song is from the user's target and subtracts that gap from the score. A song that is far off on energy loses more points than a song that is close.

After every song is scored, the five with the highest totals are returned as recommendations.

No listening history, ratings, or other-user data is used. The system only compares a single profile against fixed song attributes.

---

## 4. Data  

The catalog contains **18 songs**.

Each song has 10 fields: a unique ID, title, artist, genre, mood, and five numerical audio features — energy (0–1), tempo in BPM, valence (0–1), danceability (0–1), and acousticness (0–1).

The catalog covers **15 genres**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, metal, r&b, folk, edm, country, and blues.

Represented moods include: happy, chill, intense, relaxed, moody, focused, peaceful, energetic, angry, romantic, melancholic, euphoric, nostalgic, and sad.

Key limits:
- Most genres have only 1 song (rock, metal, classical, folk, blues, country, jazz, edm, etc.).
- Only lofi has 3 songs; pop has 2.
- No user listening history, ratings, or demographic data is included.
- The dataset was not modified from the starter — no songs were added or removed.

---

## 5. Strengths  

The system works best when the catalog has several songs in the user's favorite genre. The CHILL_LOFI profile is the clearest example: three lofi songs exist, two of them also match the "chill" mood, and they dominate the top 3 slots with very clean scores.

The scoring is fully transparent. Every recommendation comes with a written explanation showing exactly which bonuses were earned and which penalties were applied. There are no black-box steps.

The genre + mood priority hierarchy makes intuitive sense: broad category first, then feel, then numbers. That ordering matches how most people describe their music taste.

---

## 6. Limitations and Bias 

The system over-prioritizes genre match because the genre bonus (+3.0 points) is so large relative to the numerical penalties that a song in the "right" genre will almost always outrank a better-fitting song from a different genre. For example, a lofi song with the wrong energy, tempo, valence, and danceability can still beat a perfectly matched indie-pop song simply because the user listed "lofi" as their favorite genre. This creates a genre filter bubble: users are rarely shown music outside their stated category, even when songs from other genres would actually suit their listening mood better. The problem is compounded for users whose favorite genre has very few songs in the catalog — a metal or classical fan gets at most one genre-bonus recommendation, and the rest of the top-5 list is filled by numerical proximity alone, which can pull in genres that feel completely unrelated. Real music apps address this by blending genre signals with listening history and diversity constraints, neither of which this system currently supports.

---

## 7. Evaluation  

I tested three user profiles against all 18 songs in the catalog and inspected the top-5 recommendations for each.

**Profiles tested:**

- **HIGH_ENERGY_POP** — wants pop, energetic mood, very high energy (0.90), fast tempo (128 BPM), very positive valence (0.85), and highly danceable tracks.
- **CHILL_LOFI** — wants lofi, chill mood, low energy (0.40), slow tempo (80 BPM), moderate positivity (0.60), some groove, and an acoustic sound.
- **DEEP_INTENSE_ROCK** — wants rock, intense mood, high energy (0.85), fast driving tempo (140 BPM), darker tone (valence 0.35), and is not focused on danceability.

**What I looked for:**

I checked whether the genre and mood of the top results actually matched the profile's stated preferences, and whether the numerical scores (energy, tempo, valence, danceability) were close to the targets.

**Results and surprises:**

CHILL_LOFI behaved almost exactly as expected: the top three were all lofi songs (*Midnight Coding*, *Library Rain*, *Focus Flow*), and *Midnight Coding* and *Library Rain* also matched the "chill" mood, giving them a combined genre + mood bonus that pushed their scores above 4.8. The only odd entry was *Dusty Highway* (country) slipping in at #5 — it landed there not because it sounds like lofi, but because its tempo (84 BPM) and energy (0.52) were numerically close enough to the lofi targets after the three actual lofi songs ran out.

HIGH_ENERGY_POP returned a more surprising result: *Gym Hero* ranked **first** (score 2.85), beating *Sunrise City* (score 2.75), which is the song that actually has a "happy" mood. *Gym Hero* is a high-intensity pop track, not a happy-pop track, but its energy (0.93), tempo (132 BPM), and danceability (0.88) are nearly perfect numerical matches for the profile. The genre bonus (+3.0) did the rest. The system has no way to penalize a mood mismatch — it only adds points for a match — so an "intense" gym banger outranks a "happy" pop song because the numbers are tighter.

DEEP_INTENSE_ROCK exposed the catalog's biggest weakness: there is only one rock song (*Storm Runner*), and it scored 4.54. After that, the system had to fall back on pure number-matching. *Gym Hero* ranked second (score 1.03) because its "intense" mood earned +2.0, even though the song is a pop track with a bright, positive valence (0.77) that is nothing like what a rock listener would want. The remaining slots were filled by *Iron Cathedral* (metal), *Night Drive Loop* (synthwave), and *Last Call Blues* (blues) — a mix that represents the system finding the "least bad" options when the catalog does not have enough rock songs.

**Simple comparisons run:**

Switching profiles manually and re-running the simulation confirmed that changes in `target_energy` and `target_valence` had the biggest effect on which songs appeared in the lower half of the top 5. The genre bonus was large enough that the top 1–2 slots were almost always genre matches when one existed.

---

## 8. Future Work  

**1. Expand the catalog.** Eighteen songs is too small. Genres like rock, metal, and classical each have one song, which means the system cannot recover gracefully when a user's genre preference is underrepresented. A larger catalog (hundreds of songs, balanced across genres) would make the numerical scoring far more meaningful.

**2. Add a diversity rule.** The current system can return all 3 lofi songs in the top 3 slots with no variety. A simple cap — say, no more than 2 songs from the same genre in a top-5 list — would push the system to surface something the user might not have expected, which is often how people discover new music.

**3. Weight the features differently per user.** Right now every user is scored the same way. A user who cares a lot about tempo but not about danceability has no way to express that. Letting users set custom weights for each feature (or learning those weights from feedback) would make recommendations much more personal.

---

## 9. Personal Reflection  

My biggest learning moment was designing the scoring function. That single formula controls everything the system does, and getting it right was harder than I expected. I used AI tools throughout the project — for writing code, running through test cases, and especially for thinking through the scoring logic. The first scoring function the AI suggested worked, but it was overcomplicated: it used normalization steps and weighted sums that were difficult to reason about and made it hard to explain why any one song ranked where it did. I had to push back, simplify, and rebuild it around a principle I could actually defend — big flat bonuses for genre and mood, then small continuous penalties for numerical distance. That iteration taught me that the AI is a strong collaborator for generating options, but the judgment call about *which* option is right still has to come from the engineer.

What surprised me most was how human the output felt even though the algorithm is just arithmetic. When the system prints "genre match (+3.0), mood match (+2.0), energy gap −0.18 …" for a recommended song, it reads like the system actually *understands* your taste — but it is only doing a handful of additions and subtractions. The explanation format does a lot of work: seeing a ranked list with justifications makes a simple formula feel intelligent in a way that a plain score number never would. That gap between what the algorithm actually computes and what a user perceives it as doing seems important for understanding how real recommenders build trust (and how they can mislead).

If I extended this project, the first thing I would do is expand the dataset. Eighteen songs is too limiting — most genres have only one representative, so the numerical scoring has almost nothing to work with once the genre bonus is spent. A larger, more balanced catalog would let me test whether the scoring function holds up at scale or whether the weights need to be rethought entirely.
