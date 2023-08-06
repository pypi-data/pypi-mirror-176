# -*- coding: utf-8 -*-

"""Top-level package for CLI App"""

import click

from . import commands



@click.group()
def cli():
    pass


# Add commands
cli.add_command(commands.groups.add)
cli.add_command(commands.groups.remove)
cli.add_command(commands.groups.show)
cli.add_command(commands.groups.play)
cli.add_command(commands.stubs.apply)
cli.add_command(commands.stubs.refresh)

cli()
