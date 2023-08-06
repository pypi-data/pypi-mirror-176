import click
from ..groups import add
from ggist_cli_app.context import click_pass_context
from ggist_cli_app.core.source import Source
from ggist_cli_app.utils.fs import file_write_lines
import inquirer
from rich.console import Console


@add.command()
@click.argument('source')
@click_pass_context
def source(context, source: str):
    """
    add a source
    """
    console = Console()

    source_label = source
    source = Source(source_label, context)
    console.print(f'''Source '{source_label}' contains:
    - {len(source.aliases)} aliases
    ''')
    questions = [
        inquirer.Confirm("sure", message="Continue?", default=True),
    ]

    answers = inquirer.prompt(questions)

    if answers['sure']:        
        context.sources.add_source(source)
        console.print(f"[bold green]Source '{source}' added")
        console.print(f"open a new terminal session and you can use:")
        for alias in source.aliases[:10]:
            console.print(f'-{alias}')

        if len(source.aliases) > 10:
            console.print('...\n(partial)')
        console.print('[blue] to see the full list run `ggist show aliases`')
    else:
        console.print("[bold red]Skipped. you answered 'NO'")