
from ._version import __version__
from .core.jejudo import Jejudo


def setup(bot):
    bot.add_cog(Jejudo(bot))