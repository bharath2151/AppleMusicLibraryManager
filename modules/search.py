def search_failed_songs(songs, query):
    query = query.lower().strip()

    results = []

    for song in songs:
        if (
            query in song.get("name", "").lower()
            or query in song.get("artist", "").lower()
            or query in song.get("album", "").lower()
            or query in song.get("reason", "").lower()
        ):
            results.append(song)

    return results