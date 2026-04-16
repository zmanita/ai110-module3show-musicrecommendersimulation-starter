from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str       # e.g. "lofi"
    favorite_mood: str        # e.g. "chill"
    target_energy: float      # 0.0–1.0
    target_tempo_bpm: float   # beats per minute
    target_valence: float     # 0.0–1.0 (musical positiveness)
    target_danceability: float  # 0.0–1.0
    likes_acoustic: bool      # True → prefers acoustic over electronic


# --- Scoring constants ---
# Genre is awarded the most points because it is the broadest taste signal.
# Mood gets slightly fewer points — it matters, but two songs in the same genre
# can differ wildly in mood and still feel right to a listener.
GENRE_BONUS = 3.0    # points added for an exact genre match
MOOD_BONUS  = 2.0    # points added for an exact mood match

# Tempo is in BPM (roughly 60–260), while every other numerical feature sits
# on a 0–1 scale.  Dividing the BPM gap by TEMPO_MAX_RANGE brings it onto the
# same 0–1 scale so it contributes a comparable penalty to the other features.
TEMPO_MAX_RANGE = 200.0


def score_song(user_prefs, song) -> Tuple[float, List[str]]:
    """
    Calculate a recommendation score for a song based on user preferences.
    
    Compares a song's attributes (genre, mood, energy, tempo, valence, danceability)
    against user preferences, applying bonuses for exact matches on categorical features
    and penalties based on distance from target numerical features.
    
    Args:
        user_prefs: User preference object (dict or dataclass) containing favorite_genre,
                   favorite_mood, target_energy, target_tempo_bpm, target_valence,
                   and target_danceability.
        song: Song object (dict or dataclass) containing genre, mood, energy, tempo_bpm,
              valence, and danceability attributes.
    
    Returns:
        Tuple[float, List[str]]: A tuple containing the calculated score (higher is better)
                                 and a list of reason strings explaining score components.
    """

    def get(obj, key):
        """Return obj[key] for dicts or getattr(obj, key) for dataclasses."""
        return obj[key] if isinstance(obj, dict) else getattr(obj, key)

    score = 0.0
    reasons: List[str] = []

    # --- Binary feature bonuses ---
    if get(song, "genre").lower() == get(user_prefs, "favorite_genre").lower():
        score += GENRE_BONUS
        reasons.append(f"genre match (+{GENRE_BONUS})")
    if get(song, "mood").lower() == get(user_prefs, "favorite_mood").lower():
        score += MOOD_BONUS
        reasons.append(f"mood match (+{MOOD_BONUS})")

    # --- Numerical feature penalties (distance from user's targets) ---
    energy_penalty = abs(get(song, "energy") - get(user_prefs, "target_energy"))
    score -= energy_penalty
    reasons.append(f"energy distance −{energy_penalty:.2f}")

    tempo_penalty = abs(get(song, "tempo_bpm") - get(user_prefs, "target_tempo_bpm")) / TEMPO_MAX_RANGE
    score -= tempo_penalty
    reasons.append(f"tempo distance −{tempo_penalty:.2f}")

    valence_penalty = abs(get(song, "valence") - get(user_prefs, "target_valence"))
    score -= valence_penalty
    reasons.append(f"valence distance −{valence_penalty:.2f}")

    dance_penalty = abs(get(song, "danceability") - get(user_prefs, "target_danceability"))
    score -= dance_penalty
    reasons.append(f"danceability distance −{dance_penalty:.2f}")

    return score, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(self.songs, key=lambda s: score_song(user, s)[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(user, song)
        return f"'{song.title}' recommended because: {'; '.join(reasons)}."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)

    return [
        (song, sc, "; ".join(reasons))
        for song, sc, reasons in scored[:k]
    ]
