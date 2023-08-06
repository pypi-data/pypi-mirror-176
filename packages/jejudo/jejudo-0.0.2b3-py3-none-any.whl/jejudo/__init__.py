
from ._version import __version__
from .core.jejudo import Jejudos
import inspect
import typing

from discord.ext import commands


__all__ = (
    "jejudo"
)

async def async_setup(bot: commands.Bot):
    """
    The async setup function defining the jishaku.cog and jishaku extensions.
    """

    await bot.add_cog(Jejudos(bot=bot))  # type: ignore


def setup(bot: commands.Bot):  # pylint: disable=inconsistent-return-statements
    """
    The setup function defining the jishaku.cog and jishaku extensions.
    """

    if inspect.iscoroutinefunction(bot.add_cog):
        return async_setup(bot)

    bot.add_cog(Jejudos(bot=bot))