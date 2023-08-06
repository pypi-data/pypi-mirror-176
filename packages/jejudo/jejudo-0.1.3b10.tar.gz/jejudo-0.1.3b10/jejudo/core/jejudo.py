import discord 
from discord.ext import commands
import sys
import typing
import pkg_resources
from ..core.work.types import ContextA
from ..core.codeblocks import Codeblock, codeblock_converter
import traceback
import math
import typing
from jejudo.shell import ShellReader
from jejudo.exception_handling import ReplResponseReactor
from jejudo.flags import Flags
from jejudo.paginators import PaginatorInterface, WrappedPaginator





# ==============================================================================

try:
    import psutil
except ImportError:
    psutil = None

try:
    from importlib.metadata import distribution, packages_distributions
except ImportError:
    from importlib_metadata import distribution, packages_distributions

# ==============================================================================





def natural_size(size_in_bytes: int) -> str:
    """
    Converts a number of bytes to an appropriately-scaled unit
    E.g.:
        1024 -> 1.00 KiB
        12345678 -> 11.77 MiB
    """
    units = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

    power = int(math.log(max(abs(size_in_bytes), 1), 1024))

    return f"{size_in_bytes / (1024 ** power):.2f} {units[power]}"


def natural_time(time_in_seconds: float) -> str:
    """
    Converts a time in seconds to a 6-padded scaled unit
    E.g.:
        1.5000 ->   1.50  s
        0.1000 -> 100.00 ms
        0.0001 -> 100.00 us
    """
    units = (
        ('mi', 60),
        (' s', 1),
        ('ms', 1e-3),
        ('\N{GREEK SMALL LETTER MU}s', 1e-6),
    )

    absolute = abs(time_in_seconds)

    for label, size in units:
        if absolute > size:
            return f"{time_in_seconds / size:6.2f} {label}"

    return f"{time_in_seconds / 1e-9:6.2f} ns"


def mean_stddev(collection: typing.Collection[float]) -> typing.Tuple[float, float]:
    """
    Takes a collection of floats and returns (mean, stddev) as a tuple.
    """

    average = sum(collection) / len(collection)

    if len(collection) > 1:
        stddev = math.sqrt(sum(math.pow(reading - average, 2) for reading in collection) / (len(collection) - 1))
    else:
        stddev = 0.0

    return (average, stddev)


def format_stddev(collection: typing.Collection[float]) -> str:
    """
    Takes a collection of floats and produces a mean (+ stddev, if multiple values exist) string.
    """
    if len(collection) > 1:
        average, stddev = mean_stddev(collection)

        return f"{natural_time(average)} \N{PLUS-MINUS SIGN} {natural_time(stddev)}"

    return natural_time(sum(collection) / len(collection))


class Dropdown(discord.ui.Select):
    def __init__(self, bot_: discord.Bot, requester):
        self.bot = bot_
        self.requester = requester
        options = [
            discord.SelectOption(
                label="jejudo page", description="View the Jeju Island main page.", emoji="🟥"
            ),
            discord.SelectOption(
                label="protected_access page", description="The page related to the intent.", emoji="🟩"
            )
        ]

        super().__init__(
            placeholder="jejudo !! Click here to open the menu!",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.requester:
            return await interaction.response.send_message("❌ jejudo is the commands owner !!", ephemeral=True)

        if self.values[0] == "jejudo page":

            jejudo = [
                f"> the, jejudo ` v{pkg_resources.get_distribution('jejudo').version} `, py-cord ` v{pkg_resources.get_distribution('py-cord').version} `".replace("\n", ""),
                f"ㄴ • Python ` {sys.version}`".replace("\n", ""),
                f"ㄴ • platform `{sys.platform}`".replace("\n", "")
            ]
            
            if psutil:
                try:
                    proc = psutil.Process()

                    with proc.oneshot():
                        try:
                            mem = proc.memory_full_info()
                            jejudo.append(f"\n • {natural_size(mem.rss)} memory , {natural_size(mem.vms)} memory , {natural_size(mem.uss)} memory")
                        except psutil.AccessDenied:
                            pass

                        try:
                            name = proc.name()
                            pid = proc.pid
                            thread_count = proc.num_threads()

                            jejudo.append(f"ㄴ • PID {pid} (`{name}`) == {thread_count} thread(s)")
                        except psutil.AccessDenied:
                            pass

                        jejudo.append("")
                except psutil.AccessDenied:
                    jejudo.append(
                        "ㄴ • psutil is installed, but this process does not have high enough access rights "
                    )
                    jejudo.append("")

            cache_summary = f"` 🌐 {len(self.bot.guilds)} ` guild(s) ㅣ ` 🤴 {len(self.bot.users)} ` user(s)"

            if isinstance(self.bot, discord.AutoShardedClient):
                if len(self.bot.shards) > 20:
                    jejudo.append(
                        f"This bot is auto shards (` {len(self.bot.shards)} ` shards of ` {self.bot.shard_count} `)"
                        f"\n{cache_summary}."
                    )
                else:
                    shard_ids = ', '.join(str(i) for i in self.bot.shards.keys())
                    jejudo.append(
                        f"This bot is auto shards (Shards ` {shard_ids} ` of ` {self.bot.shard_count} `)"
                        f"\n{cache_summary}."
                    )
            elif self.bot.shard_count:
                jejudo.append(
                    f"This bot is manually sharded (Shard ` {self.bot.shard_id} ` of ` {self.bot.shard_count} `)"
                    f"\n{cache_summary}."
                )
            else:
                jejudo.append(f"This bot is not sharded\n{cache_summary}.")

            jejudo.append(f"\n\nAverage websocket latency: {round(self.bot.latency * 1000, 2)}ms")

            await interaction.response.edit_message(
                content="\n".join(jejudo)
            )
        if self.values[0] == "protected_access page":
            jejudo = [
                f"> the, jejudo ` v{pkg_resources.get_distribution('jejudo').version} `, py-cord ` v{pkg_resources.get_distribution('py-cord').version} `".replace("\n", ""),
                f"ㄴ • Python ` {sys.version}`".replace("\n", ""),
                f"ㄴ • platform `{sys.platform}`".replace("\n", "")
            ]

            if self.bot._connection.max_messages:
                message_cache = f"Message cache capped at {self.bot._connection.max_messages}"
            else:
                message_cache = "Message cache is disabled"

            if discord.version_info >= (1, 5, 0):
                remarks = {
                    True: 'enabled',
                    False: 'disabled',
                    None: 'unknown'
                }

                *group, last = (
                    f"{intent.replace('_', ' ')} intent is {remarks.get(getattr(self.bot.intents, intent, None))}\n"
                    for intent in
                    ('presences', 'members', 'message_content')
                )

                jejudo.append(f"\n{message_cache}\n{''.join(group)}\n{last}")
            else:
                guild_subscriptions = f"guild subscriptions are {'enabled' if self.bot._connection.guild_subscriptions else 'disabled'}"  # type: ignore

                jejudo.append(f"\n{message_cache}\n{guild_subscriptions}")
            jejudo.append(f"Average websocket latency: {round(self.bot.latency * 1000, 2)}ms")

            await interaction.response.edit_message(
                content="\n".join(jejudo)
            )

class DropdownView(discord.ui.View):
    def __init__(self, bot_: discord.Bot, requester):
        self.bot = bot_
        self.requester = requester
        super().__init__()
        self.add_item(Dropdown(self.bot, self.requester))

class Jejudos(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot


    @commands.group("jejudo",aliases=["jeju","jdo"],invoke_without_command=True)
    @commands.is_owner()
    async def jejudo_jsk(self, ctx: ContextA):
        try:

            jejudo = [
                f"> the, jejudo ` v{pkg_resources.get_distribution('jejudo').version} `, py-cord ` v{pkg_resources.get_distribution('py-cord').version} `".replace("\n", ""),
                f"ㄴ • Python ` {sys.version}`".replace("\n", ""),
                f"ㄴ • platform `{sys.platform}`".replace("\n", "")
            ]
            
            if psutil:
                try:
                    proc = psutil.Process()

                    with proc.oneshot():
                        try:
                            mem = proc.memory_full_info()
                            jejudo.append(f"\n • {natural_size(mem.rss)} memory , {natural_size(mem.vms)} memory , {natural_size(mem.uss)} memory")
                        except psutil.AccessDenied:
                            pass

                        try:
                            name = proc.name()
                            pid = proc.pid
                            thread_count = proc.num_threads()

                            jejudo.append(f"ㄴ • PID {pid} (`{name}`) == {thread_count} thread(s)")
                        except psutil.AccessDenied:
                            pass

                        jejudo.append("")  # blank line
                except psutil.AccessDenied:
                    jejudo.append(
                        "ㄴ • psutil is installed, but this process does not have high enough access rights "
                    )
                    jejudo.append("")  # blank line

            cache_summary = f"` 🌐 {len(self.bot.guilds)} ` guild(s) ㅣ ` 🤴 {len(self.bot.users)} ` user(s)"

            # Show shard settings to summary
            if isinstance(self.bot, discord.AutoShardedClient):
                if len(self.bot.shards) > 20:
                    jejudo.append(
                        f"This bot is auto shards (` {len(self.bot.shards)} ` shards of ` {self.bot.shard_count} `)"
                        f"\n{cache_summary}."
                    )
                else:
                    shard_ids = ', '.join(str(i) for i in self.bot.shards.keys())
                    jejudo.append(
                        f"This bot is auto shards (Shards ` {shard_ids} ` of ` {self.bot.shard_count} `)"
                        f"\n{cache_summary}."
                    )
            elif self.bot.shard_count:
                jejudo.append(
                    f"This bot is manually sharded (Shard ` {self.bot.shard_id} ` of ` {self.bot.shard_count} `)"
                    f"\n{cache_summary}."
                )
            else:
                jejudo.append(f"This bot is not sharded\n{cache_summary}.")
            jejudo.append(f"\n\nAverage websocket latency: {round(self.bot.latency * 1000, 2)}ms")

            view = DropdownView(self.bot, ctx.author)
            await ctx.reply("\n".join(jejudo), view=view)
        except:
            print(traceback.format_exc())




    @jejudo_jsk.command(name="shell", aliases=["bash", "sh", "powershell", "ps1", "ps", "cmd", "terminal"])
    async def jejudo_shell(self, ctx: ContextA, *, argument: codeblock_converter=None):
        """
        Run a shell command
        """
        if not argument:
            await ctx.send("Usage: `jejudo shell <argument>`")
            return
        if typing.TYPE_CHECKING:
            argument: Codeblock = argument  # type: ignore

        try:
            async with ReplResponseReactor(ctx.message):
                with ShellReader(argument.content, escape_ansi=not Flags.use_ansi(ctx)) as reader:
                    prefix = "```" + reader.highlight

                    paginator = WrappedPaginator(prefix=prefix, max_size=1975)
                    paginator.add_line(f"{reader.ps1} {argument.content}\n")

                    interface = PaginatorInterface(ctx.bot, paginator, owner=ctx.author)
                    self.bot.loop.create_task(interface.send_to(ctx))

                    async for line in reader:
                        if interface.closed:
                            return
                        await interface.add_line(line)

                await interface.add_line(f"\n[status] Return code {reader.close_code}")
        except:
            print(traceback.format_exc())