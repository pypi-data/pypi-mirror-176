import click
from ggist_cli_app.context import click_pass_context


@click.command()
@click_pass_context
def apply(context):
    # apply it in bashrc with 
    # cd /workspaces/ggist/ && eval "$(python -m ggist_cli_app apply)"

    # apply aliases
    with open(context.aliases_file, 'r') as fin:
        line = fin.read()
        print(line)

    # apply scripts
    print(f'export PATH=$PATH:{context.scripts_dir}')