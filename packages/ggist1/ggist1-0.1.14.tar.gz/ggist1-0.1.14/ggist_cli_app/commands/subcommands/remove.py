import click
from ggist_cli_app.context import click_pass_context
from ggist_cli_app.commands.groups import remove
from ggist_cli_app.core.source import Source



@remove.command(name="source")
@click.argument('source')
@click_pass_context
def remove_source(context, source: str):
    """
    remove a source
    """
    source = Source(source, context)
    context.sources.remove_source(source)
