# -*- coding: utf-8 -*-

"""Top-level package for CLI App"""

import click

from . import commands



@click.group()
def cli():
    pass


# Add commands
cli.add_command(commands.sources.add)
cli.add_command(commands.sources.remove)
cli.add_command(commands.sources.refresh)
cli.add_command(commands.terminal.apply)
cli.add_command(commands.show.show)

cli()
