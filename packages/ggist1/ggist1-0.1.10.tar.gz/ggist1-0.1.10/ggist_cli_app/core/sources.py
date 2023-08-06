from typing import Sequence
from ggist_cli_app.utils.fs import exists, file_read_lines, file_write_lines
from ggist_cli_app.utils import git
from ggist_cli_app.core.source import Source
from ggist_cli_app.core.aliases import Aliases

class Sources:

    def __init__(self, context: 'Context'):
        self.context = context
        self.sources_file = context.sources_file
        self.sources = self.load_sources(self.sources_file, context)

    def remove_source(self, source: Source):
        self.sources.remove(source)
        self.save()

    def add_source(self, source: Source):
        self.sources.add(source)
        self.save()


    def save(self):
        self.save_sources(self.sources_file, self.sources)
        # update aliases file
        Aliases.recreate_aliases(self.context.aliases_file, self.sources)

    @staticmethod
    def load_sources(sources_file, context):
        return set(map(lambda s: Source(s, context), file_read_lines(sources_file)))

    @staticmethod
    def save_sources(sources_file, sources: Sequence[Source]):
        file_write_lines(sources_file, tuple(map(str, sources)))