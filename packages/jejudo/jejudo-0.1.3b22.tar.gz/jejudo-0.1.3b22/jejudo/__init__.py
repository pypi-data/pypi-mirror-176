
from ._version import __version__
from .core.jejudo import Jejudos


def setup(bot):
    bot.add_cog(Jejudos(bot))