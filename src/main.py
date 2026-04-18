"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


HIGH_ENERGY_POP = {
    "favorite_genre": "pop",
    "favorite_mood": "energetic",
    "target_energy": 0.90,           # high-energy, hype listening
    "target_tempo_bpm": 128,         # fast dance tempo (bpm)
    "target_valence": 0.85,          # very positive, feel-good
    "target_danceability": 0.90,     # highly danceable
    "likes_acoustic": False,         # prefers electronic/produced sound
}

CHILL_LOFI = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,           # low-energy, calm listening
    "target_tempo_bpm": 80,          # slow-to-mid tempo (bpm)
    "target_valence": 0.60,          # moderately positive/uplifting
    "target_danceability": 0.60,     # some groove, not a party track
    "likes_acoustic": True,          # prefers acoustic over electronic
}

DEEP_INTENSE_ROCK = {
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.85,           # high-energy, aggressive listening
    "target_tempo_bpm": 140,         # fast, driving tempo (bpm)
    "target_valence": 0.35,          # darker, more serious tone
    "target_danceability": 0.45,     # not focused on danceability
    "likes_acoustic": False,         # prefers electric/distorted sound
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Switch between profiles to test different recommendations
    user_prefs = CHILL_LOFI

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"🎵 {song['title']}")
        print(f"   Artist: {song['artist']}")
        print(f"   Score: {score:.2f}/10")
        print(f"   Why: {explanation}")
        print("-" * 50)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
