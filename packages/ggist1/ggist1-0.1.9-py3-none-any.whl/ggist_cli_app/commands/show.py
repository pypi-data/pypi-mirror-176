import click
from ggist_cli_app.context import click_pass_context
from ggist_cli_app.core.aliases import recreate_aliases
from ggist_cli_app.core.source import Source
from ggist_cli_app.utils.fs import file_write_lines

@click.group()
def show():
    pass

@show.command()
@click_pass_context
def sources(context):
    """
    Show sources
    """
    sources = Source.load_sources(context.sources_file, context)

    print('sources:')
    for source in sources:
        print(f' - {source}')



@show.command()
@click_pass_context
def aliases(context):
    """
    Show aliases
    """
    print('aliases:')
    with open(context.aliases_file, 'r') as fin:
        line = fin.read()
        print(line)
