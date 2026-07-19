import subprocess
import questionary
import json

from modules.failed import get_failed_songs
from modules.config import config
from pathlib import Path
from collections import Counter
from rich.console import Console
console = Console()
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)


def retry_menu():
    return questionary.select(
        "Retry Failed Songs",
        choices=[
            "Retry All Failed Songs",
            "Retry One Song",
            "Retry by Artist",
            "Retry by Reason",
            "Back",
        ],
    ).ask()


def select_failed_song():
    songs = get_failed_songs()

    if not songs:
        return None

    song_map = {}
    choices = []

    for song in songs:
        display = f"{song['name']} — {song['artist']}"
        song_map[display] = song
        choices.append(display)

    choices.append("Back")

    selected = questionary.select(
        "Select a failed song",
        choices=choices,
    ).ask()

    if selected == "Back":
        return None

    return song_map[selected]




def select_artist():
    songs = get_failed_songs()

    if not songs:
        return None

    artist_counts = Counter(song["artist"] for song in songs)

    artist_map = {}
    choices = []

    for artist, count in sorted(artist_counts.items()):
        display = f"{artist} ({count})"
        artist_map[display] = artist
        choices.append(display)

    choices.append("Back")

    selected = questionary.select(
        "Select an artist",
        choices=choices,
    ).ask()

    if selected == "Back":
        return None

    return artist_map[selected]

def select_reason():
    songs = get_failed_songs()

    if not songs:
        return None

    reason_counts = Counter(song["reason"] for song in songs)

    reason_map = {}
    choices = []

    for reason, count in sorted(reason_counts.items()):
        display = f"{reason} ({count})"
        reason_map[display] = reason
        choices.append(display)

    choices.append("Back")

    selected = questionary.select(
        "Select a reason",
        choices=choices,
    ).ask()

    if selected == "Back":
        return None

    return reason_map[selected]

def remove_failed_song(song_id):
    path = Path(config["failed_songs_path"])

    if not path.exists():
        return

    with path.open("r", encoding="utf-8") as f:
        songs = json.load(f)

    songs = [song for song in songs if song["id"] != song_id]

    with path.open("w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)

def retry_song(song, verbose=True):
    if verbose:
        console.print(
            f"\n[cyan]Retrying:[/cyan] {song['name']} - {song['artist']}"
        )

    try:
        result = subprocess.run(
            [
                config["amdl_path"],
                song["url"],
            ],
            cwd=Path(config["amdl_path"]).parent,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode == 0:
            remove_failed_song(song["id"])

            if verbose:
                console.print("[bold green]✓ Success[/bold green]")

            return True

        if verbose:
            console.print(
                f"[bold red]✗ Failed (Exit Code {result.returncode})[/bold red]"
            )

        return False

    except Exception as e:
        if verbose:
            console.print(f"[bold red]{e}[/bold red]")

        return False

def retry_songs(songs, title="Retry Summary"):
    success = 0
    failed = 0

    console.clear()
    console.rule(f"[bold green]{title}")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:

        task = progress.add_task(
            "Retrying Songs",
            total=len(songs),
        )

        for song in songs:

            progress.update(
                task,
                description=f"{song['artist']} - {song['name']}"
            )

            if retry_song(song, verbose=False):
                success += 1
            else:
                failed += 1

            progress.advance(task)

    console.rule("[bold green]Retry Summary")

    console.print(f"Total Songs : {len(songs)}")
    console.print(f"[green]Succeeded : {success}[/green]")
    console.print(f"[red]Failed    : {failed}[/red]")

    input("\nPress Enter to continue...")

def handle_retry():
    option = retry_menu()

    if option == "Back":
        return

    elif option == "Retry All Failed Songs":

        songs = get_failed_songs()

        if not songs:
            console.print("[yellow]No failed songs found.[/yellow]")
            input("\nPress Enter to continue...")
            return

        retry_songs(songs)

    elif option == "Retry One Song":
        song = select_failed_song()

        if song is None:
            return

        console.clear()

        console.print()
        console.rule("[bold green]Selected Song")
        console.print()

        console.print(f"Name   : {song['name']}")
        console.print(f"Artist : {song['artist']}")
        console.print(f"Album  : {song['album']}")
        console.print(f"Reason : {song['reason']}")
        console.print(f"ID     : {song['id']}")
        retry_song(song)
        input("\nPress Enter to continue...")
        
    elif option == "Retry by Artist":

        artist = select_artist()

        if artist is None:
            return

        songs = [
            song
            for song in get_failed_songs()
            if song["artist"] == artist
        ]

        retry_songs(songs, title=artist)

    elif option == "Retry by Reason":

        reason = select_reason()

        if reason is None:
            return

        songs = [
            song
            for song in get_failed_songs()
            if song["reason"] == reason
        ]

        retry_songs(songs, title=reason)