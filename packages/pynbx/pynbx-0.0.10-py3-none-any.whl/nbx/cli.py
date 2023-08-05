import os
from pathlib import Path

import typer
import html2text
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.console import Console
from rich.markdown import Markdown

from nbx import nbx, util, config, tui


TUI_MENU_COMMANDS = ["nbx", "nbx add", "nbx edit <index>",
                     "nbx search <query>", "nbx insight"]

cli = typer.Typer()
console = Console()


#######################################################################################
# Insight CLI

insight_cli = typer.Typer()


@insight_cli.command("add")
def add_insight():
    """
    Learn something from the note base
    """
    task = Prompt.ask("Choose a task type", choices=["Analyze a Note"], default="Analyze a Note")
    console.print(f"Not Yet Implemented: {task}")


cli.add_typer(insight_cli, name="insight")

#######################################################################################
# Config CLI

config_cli = typer.Typer()


@config_cli.callback(invoke_without_command=True)
def config_main(ctx: typer.Context):
    """
    Configure NBX
    """
    # only run without a command specified
    if ctx.invoked_subcommand is not None:
        return

    nbx_config = config.load_config()
    notes_dir = nbx_config["notes_dir"]
    serach_method = nbx_config["search_method"]
    config_subcommands = [
        "nbx config search", "nbx config storage",
        "nbx config openai", "nbx config pinecone"
    ]
    subtitle = tui.get_panel_subtitle(config_subcommands)
    content = f"""
[bold cyan]Notes Repo:[/bold cyan] [yellow]{str(notes_dir)}[/yellow]
[bold cyan]Search Method:[/bold cyan] [yellow]{serach_method}[/yellow]
    """
    dashboard = Panel(
        content.strip(), title="NBX Configuration", subtitle=subtitle
    )
    console.print(dashboard)


@config_cli.command("storage")
def config_storage():
    """
    Configure NBX's storage
    """
    notes_dir = Prompt.ask("Enter repo path", default=os.fspath(config.DEFAULT_NOTES_DIR)).strip()
    notes_dir = Path(notes_dir)
    notes_dir.mkdir(parents=True, exist_ok=True)
    config.set_notes_dir(notes_dir)


@config_cli.command("search")
def config_search_method():
    """
    Configure search method
    """
    from nbx.search import SEARCH_OPTIONS
    nbx_config = config.load_config()
    method = Prompt.ask(
        "Enter your preferred search method",
        choices=SEARCH_OPTIONS, default=nbx_config["search_method"]
    ).strip()
    config.set_search_method(method)
    nbx.index_all_notes(background=True)


@config_cli.command("openai")
def config_openai():
    """
    Configure OpenAI API token
    """
    token = Prompt.ask("Enter your OpenAI API token").strip()
    verify_resp = util.verify_openai_token(token)
    if verify_resp != "OK":
        console.print(verify_resp)
        return
    config.set_openai_token(token)


@config_cli.command("pinecone")
def config_pincone():
    """
    Configure Pincone API token
    """
    token = Prompt.ask("Enter your Pinecone API token").strip()
    verify_resp = util.verify_pinecone_token(token)
    if verify_resp != "OK":
        console.print(verify_resp)
        return
    config.set_pinecone_token(token)


cli.add_typer(config_cli, name="config")

#######################################################################################
# Alias CLI

alias_cli = typer.Typer()


@alias_cli.command("del")
def alias_del():
    """
    Delete a NBX note alias
    """
    all_alias = nbx.get_alias_headlines()
    alias = Prompt.ask("Enter alias").strip()
    if alias not in all_alias:
        console.print("[Warning]: Alias doesn't exist")
    headline = all_alias[alias]
    prompt = f"Removing alias [yellow]{alias}[/yellow] from [bold cyan]{headline}[/bold cyan]"
    if not Confirm.ask(prompt):
        return
    nbx.delete_alias(alias)


@alias_cli.command("add")
def alias_add():
    """
    Add a NBX note alias
    """
    notes = nbx.get_all_notes()
    all_alias = nbx.get_alias_headlines()
    index = IntPrompt.ask("Enter note index")
    if len(notes) <= index or index < 0:
        console.print("[Warning]: Note doesn't exist")
        return
    note = notes[index]
    headline = note.get_headline()
    headline = tui.format_headline(headline)
    if not Confirm.ask(f"Creating alias for note: [bold cyan]{headline}[/bold cyan]"):
        return
    alias = Prompt.ask("Enter alias").strip()
    if alias in all_alias:
        headline = all_alias[alias]
        console.print(f"[Warning]: Alias already exist with note: {headline}")
        return
    prompt = f"Aliasing note [bold cyan]{headline}[/bold cyan] with [yellow]{alias}[/yellow]"
    if not Confirm.ask(prompt):
        return
    nbx.create_alias(note, alias)


@alias_cli.callback(invoke_without_command=True)
def alias_main(ctx: typer.Context):
    """
    Manage NBX's note alias
    """
    # only run without a command specified
    if ctx.invoked_subcommand is not None:
        return
    config_subcommands = [
        "nbx alias add", "nbx alias del"
    ]
    subtitle = tui.get_panel_subtitle(config_subcommands)
    alias_headlines = nbx.get_alias_headlines()
    if len(alias_headlines) == 0:
        content = "No alias defined"
    else:
        content = """[bold cyan]Note Alias:[/bold cyan]\n"""
        for alias in alias_headlines:
            headline = alias_headlines[alias]
            content += f"[yellow]{alias}[/yellow]: {headline}\n"
    dashboard = Panel(
        content.strip(), title="NBX Note Alias", subtitle=subtitle
    )
    console.print(dashboard)


cli.add_typer(alias_cli, name="alias")

#######################################################################################
# Main CLI


@cli.command("add")
def add(message: str = typer.Option("", "--message", "-m", help="Message to add")):
    """
    Add a new note
    """
    if message == "":
        from nbx import app
        app.add_note()
        return

    nbx.create_note(f"<p>{message}</p>")
    nbx.index_all_notes(background=True)


@cli.command("edit")
def edit(index: str):
    """
    Edit the note with <index>
    """
    note = nbx.get_note(index)

    if note is None:
        console.print("[Warning]: Note doesn't exist")
        return

    from nbx import app
    app.edit_note(note)


@cli.command("search")
def search(
    query: str,
    edit_index: int = typer.Option(
        -1, "--edit", "-e", help="edit the search result with the index"
    ),
    peek_index: int = typer.Option(
        -1, "--peek", "-p", help="peek the serach result with the index"
    )
):
    """
    Search notes with query
    """
    all_notes = nbx.get_all_notes()
    if len(all_notes) == 0:
        console.print("[Warning]: No note exist")
        return

    records, notes = nbx.search_notes(all_notes, query)

    if len(records) > 0:
        if edit_index >= 0 and edit_index < len(notes):
            from nbx import app
            app.edit_note(notes[edit_index])
            return
        if peek_index >= 0 and peek_index < len(notes):
            from nbx import app
            app.edit_note(notes[peek_index], read_only=True)
            return
        panel_content = tui.get_panel_records(records, notes)
    else:
        panel_content = "No matching"

    dashboard = Panel(panel_content, subtitle=tui.get_panel_subtitle(TUI_MENU_COMMANDS))
    console.print(dashboard)


@cli.command("archive")
def archive(index: str):
    """
    Archive the note with <index>
    """
    note = nbx.get_note(index)

    if note is None:
        console.print("[Warning]: Note doesn't exist")
        return

    headline = note.get_headline()
    headline = tui.format_headline(headline)
    confirmed = Confirm.ask(headline)
    if confirmed:
        note.archive()
        nbx.index_all_notes(background=True)


@cli.command("index")
def index():
    """
    Index (retrain) the note base
    """
    all_notes = nbx.get_all_notes()
    console.print("Indexing the note base...")
    nbx.index_notes(all_notes)
    console.print("Done")


@cli.command("log")
def log():
    """
    Show the log of changes in nbx
    """
    logs = ["log1", "log2"]
    log_content = tui.get_log_content(logs)
    panel_subtitle = tui.get_panel_subtitle(TUI_MENU_COMMANDS)
    log_panel = Panel(log_content, title="NBX Logs",
                      subtitle=panel_subtitle)
    console.print(log_panel)


@cli.command("peek")
def peek(
    index: str = typer.Argument(..., help="index of the note"),
    gui: bool = typer.Option(
        False, "--gui", "-g", help="open the note with GUI in browser"
    ),
):
    """
    Peek a note by <index>
    """
    note = nbx.get_note(index)

    if note is None:
        console.print("[Warning]: Note doesn't exist")
        return

    if gui:
        from nbx import app
        app.edit_note(note, read_only=True)
    else:
        markdown_text = html2text.html2text(note.html, bodywidth=0)
        md = Markdown(markdown_text)
        console.print(md)


@cli.command("status")
def status():
    """
    Status of the nbx note base
    """
    console.print("NBX status")


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    gui: bool = typer.Option(
        False, "--gui", "-g", help="open the note with GUI in browser"
    )
):
    """
    Default behavior
    """
    # only run without a command specified
    if ctx.invoked_subcommand is not None:
        return

    notes = nbx.get_all_notes()

    if gui:
        pass
    else:
        # fake saved queries
        panel_title = tui.get_panel_title()
        panel_subtitle = tui.get_panel_subtitle(TUI_MENU_COMMANDS)
        panel_content = tui.get_panel_notes(notes)
        panel = Panel(panel_content, title=panel_title, subtitle=panel_subtitle)
        console.print(panel)

    # if gui:
    #     from nbx import app
    #     # extract only title string
    #     note_titles = [note_title[0] for note_title in note_titles]
    #     note_infos = [
    #         {"filename": file, "title": title} for file, title in zip(note_files, note_titles)
    #     ]
    #     app.list_notes(note_infos)
    # else:
    #     # fake saved queries
    #     saved_queries = ["NBX-TODO", "Micro-SAAS", "GPT3"]

    #     # format data into rich dashboard desired format
    #     panel_title = tui.get_panel_title(saved_queries)
    #     panel_subtitle = tui.get_panel_subtitle(TUI_MENU_COMMANDS)
    #     panel_content = tui.get_panel_content(note_titles, note_tags)
    #     dashboard = Panel(panel_content, title=panel_title, subtitle=panel_subtitle)
    #     console.print(dashboard)
