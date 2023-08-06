import click
from ggist_cli_app.context import click_pass_context
from ggist_cli_app.core.aliases import recreate_aliases
from ggist_cli_app.core.source import Source
from ggist_cli_app.utils.fs import file_write_lines

@click.command()
@click.argument('source')
@click_pass_context
def add(context, source: str):
    """
    Simple command that says hello
    """
    source = Source(source, context)

    sources = Source.load_sources(context.sources_file, context)

    sources.add(source)

    file_write_lines(context.sources_file, tuple(map(str, sources)))

    # update aliases file
    recreate_aliases(context.aliases_file, sources)



@click.command()
@click.argument('source')
@click_pass_context
def remove(context, source: str):
    """
    Simple command that says hello
    """
    source = Source(source, context)

    sources = Source.load_sources(context.sources_file, context)
    sources.remove(source)

    file_write_lines(context.sources_file, tuple(map(str, sources)))

    # update aliases file
    recreate_aliases(context.aliases_file, sources)


@click.command()
@click_pass_context
def refresh(context):
    sources = Source.load_sources(context.sources_file, context)
    # update aliases file
    recreate_aliases(context.aliases_file, sources)