# Reflection: Comparing User Profile Outputs

---

## Pair 1 — HIGH_ENERGY_POP vs. CHILL_LOFI

These two profiles are opposites in almost every way, and the results show that clearly.

The HIGH_ENERGY_POP listener gets *Gym Hero*, *Sunrise City*, and *Concrete Jungle Anthem* — all fast, punchy, very danceable tracks. The CHILL_LOFI listener gets *Midnight Coding*, *Library Rain*, and *Focus Flow* — all slow, quiet, acoustic lofi songs. There is zero overlap in the top 5.

This makes complete sense: one profile has an energy target of 0.90 and a tempo of 128 BPM, the other has 0.40 and 80 BPM. Those two numbers pull the system in completely opposite directions, so it ends up surfacing completely different songs from the catalog.

What it shows about the scoring: when two profiles are this different, the recommender works well. The numbers do a good job of separating "workout playlist" from "study session playlist."

---

## Pair 2 — HIGH_ENERGY_POP vs. DEEP_INTENSE_ROCK

This pair is more interesting because the two profiles share some things (both want high energy, both dislike acoustic), but they differ on mood and valence.

The HIGH_ENERGY_POP profile targets a bright, positive sound (valence 0.85) and an "energetic" mood. DEEP_INTENSE_ROCK targets a darker, more serious sound (valence 0.35) and an "intense" mood. That single difference — positive vs. dark — completely changes what shows up.

Both profiles rank *Gym Hero* highly, but for different reasons:
- For pop: it's a genre match and its numbers are nearly perfect.
- For rock: it matches the "intense" mood, earning +2.0 bonus points.

This is the core quirk of the system. *Gym Hero* is described here as a pop song about the gym — upbeat, produced, basically the opposite of a gritty rock track. But the recommender sees "intense mood" and hands it to both the pop fan and the rock fan. A human DJ would never put the same song on a happy-pop playlist and a deep-rock playlist, but the algorithm does.

**Why does Gym Hero keep showing up for people who just want "Happy Pop"?**

Imagine you are trying to find a restaurant that your friend will like, and all you know is that they like Italian food and fast service. You look through a list of restaurants and score them: +3 points if it's Italian, +2 if it has fast service, and then subtract points for anything that doesn't match their other preferences (price, distance, noise level).

*Gym Hero* is basically a restaurant that is Italian (+3 points) and has a very short wait time (great energy and tempo scores). It is noisy and expensive (the mood is wrong), but those minor deductions are so small compared to the +3 Italian bonus that it still wins. Your friend gets recommended a loud, expensive Italian place when they asked for a quiet, cheap one — just because the genre and numbers matched.

The recommender cannot tell that "intense" pop feels completely different from "energetic" pop. It just sees numbers that are close and gives the song a high score.

---

## Pair 3 — CHILL_LOFI vs. DEEP_INTENSE_ROCK

These two profiles are very different in energy and tempo, but they share one thing: neither one has a large catalog to draw from. There are three lofi songs and only one rock song in the entire dataset.

CHILL_LOFI benefits from this: the three lofi songs sweep the top three spots with scores of 4.91, 4.89, and 2.99. After that, the system picks *Spacewalk Thoughts* (ambient, chill) at #4 — a reasonable neighbor because it shares the "chill" mood. The only odd pick is *Dusty Highway* (country) at #5. A country song for a lofi listener sounds wrong, but its tempo (84 BPM) and energy (0.52) are close enough to the lofi targets that it sneaks in.

DEEP_INTENSE_ROCK is much worse off: there is only one rock song (*Storm Runner*), and after that the system is essentially guessing. It picks *Gym Hero* for its "intense" mood, *Iron Cathedral* for its high energy, *Night Drive Loop* for its dark tempo, and *Last Call Blues* because its danceability score (0.45) happens to be a perfect numerical match for the rock profile — even though a slow blues song sounds nothing like a rock record.

The comparison shows that the recommender is only as good as the variety in the catalog. When a genre has three songs, the top results look smart. When a genre has one song, the rest of the list is basically random.

---

## The Bigger Picture

Across all three pairs, the same pattern appears: the system rewards genre and mood matches heavily and then fills in the gaps with numerical closeness. When the catalog is deep in a genre, that strategy works well. When it is shallow, the system makes recommendations that feel off to any real listener.

The biggest takeaway is that a recommender system does not understand music — it only understands numbers. Two songs can have identical energy, tempo, valence, and danceability but sound completely different to a human ear. The numbers are a useful shortcut, but they are not the same as taste.
