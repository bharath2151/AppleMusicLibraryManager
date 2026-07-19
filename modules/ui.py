import questionary
from rich.console import Console
from rich.table import Table

console = Console()


def main_menu():
    return questionary.select(
        "Select an option:",
        choices=[
            "View Failed Songs",
            "Search Failed Songs",
            "Statistics",
            "Retry Failed Songs",
            "Exit",
        ],
    ).ask()


def show_failed_songs(songs):
    table = Table(title="Failed Songs")

    table.add_column("#", justify="right")
    table.add_column("Song")
    table.add_column("Artist")
    table.add_column("Album")
    table.add_column("Reason")

    for i, song in enumerate(songs, start=1):
        table.add_row(
            str(i),
            song.get("name", ""),
            song.get("artist", ""),
            song.get("album", ""),
            song.get("reason", ""),
        )

    console.print(table)


def search_prompt():
    return questionary.text(
        "Search:"
    ).ask()

def show_statistics(stats):
    table = Table(title="Library Statistics")

    table.add_column("Statistic", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Failed Songs", str(stats["failed_songs"]))
    table.add_row("Unique Artists", str(stats["unique_artists"]))
    table.add_row("Unique Albums", str(stats["unique_albums"]))

    artist, artist_count = stats["most_failed_artist"]
    album, album_count = stats["most_failed_album"]

    table.add_row(
        "Most Failed Artist",
        f"{artist} ({artist_count})"
    )

    table.add_row(
        "Most Failed Album",
        f"{album} ({album_count})"
    )

    console.print(table)

    if stats["reason_counts"]:
        reason_table = Table(title="Failure Reasons")

        reason_table.add_column("Reason", style="yellow")
        reason_table.add_column("Count", justify="right")

        for reason, count in stats["reason_counts"].items():
            reason_table.add_row(reason, str(count))

        console.print(reason_table)