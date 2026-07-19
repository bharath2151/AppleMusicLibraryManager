from rich.console import Console
from rich.panel import Panel

from modules.stats import get_statistics
from modules.search import search_failed_songs
from modules.retry import handle_retry

from modules.ui import (
    main_menu,
    search_prompt,
    show_failed_songs,
    show_statistics,
)
from modules.utils import clear_screen, pause
from modules.failed import (
    failed_count,
    get_failed_songs,
)

console = Console()

def run():
    while True:

        clear_screen()

        console.print(
            Panel.fit(
                "[bold cyan]Apple Music Library Manager[/bold cyan]\n"
                "[green]Version 0.1[/green]",
                title="AMLM",
            )
        )

        console.print(f"[bold red]Failed Songs:[/bold red] {failed_count()}")

        choice = main_menu()

        if choice == "View Failed Songs":
            clear_screen()
            show_failed_songs(get_failed_songs())
            pause()

        elif choice == "Search Failed Songs":
            clear_screen()

            query = search_prompt()

            results = search_failed_songs(
                get_failed_songs(),
                query,
            )

            show_failed_songs(results)

            pause()

        elif choice == "Retry Failed Songs":
            clear_screen()
            handle_retry()

        elif choice == "Exit":
            clear_screen()
            console.print("[green]Thank you for using Apple Music Library Manager![/green]")
            break