from collections import Counter


def get_statistics(songs):
    stats = {}

    stats["failed_songs"] = len(songs)

    artists = [song.get("artist", "Unknown") for song in songs]
    albums = [song.get("album", "Unknown") for song in songs]
    reasons = [song.get("reason", "Unknown") for song in songs]

    stats["unique_artists"] = len(set(artists))
    stats["unique_albums"] = len(set(albums))

    stats["reason_counts"] = Counter(reasons)

    if artists:
        stats["most_failed_artist"] = Counter(artists).most_common(1)[0]
    else:
        stats["most_failed_artist"] = ("None", 0)

    if albums:
        stats["most_failed_album"] = Counter(albums).most_common(1)[0]
    else:
        stats["most_failed_album"] = ("None", 0)

    return stats