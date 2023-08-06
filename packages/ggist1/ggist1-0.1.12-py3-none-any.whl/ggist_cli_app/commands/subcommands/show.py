import click
from ggist_cli_app.context import click_pass_context
from ggist_cli_app.core.sources import Sources
from ggist_cli_app.utils.fs import file_write_lines
from ggist_cli_app.commands.groups import show

@show.command()
@click_pass_context
def sources(context):
    """
    Show sources
    """
    sources = Sources.load_sources(context.sources_file, context)

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
