from . import stubs, groups

from .subcommands import add, play, show, remove # we need to load this code for click register commands

__all__ = ['groups', 'stubs']