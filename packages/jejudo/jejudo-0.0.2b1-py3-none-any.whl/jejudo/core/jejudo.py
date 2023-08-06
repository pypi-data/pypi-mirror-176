import discord 
from discord.ext import commands
import sys
import typing
import pkg_resources
from ..core.work import math as natural_size



# ==============================================================================

try:
    import psutil
except ImportError:
    psutil = None

try:
    from importlib.metadata import distribution, packages_distributions
except ImportError:
    from importlib_metadata import distribution, packages_distributions  # type: ignore

# ==============================================================================





class Dropdown(discord.ui.Select):
    def __init__(self, bot_: discord.Bot, requester):
        # For example, you can use self.bot to retrieve a user or perform other functions in the callback.
        # Alternatively you can use Interaction.client, so you don't need to pass the bot instance.
        self.bot = bot_
        self.requester = requester
        # Set the options that will be presented inside the dropdown:
        options = [
            discord.SelectOption(
                label="jejudo page", description="View the Jeju Island main page.", emoji="🟥"
            ),
            discord.SelectOption(
                label="protected_access page", description="The page related to the intent.", emoji="🟩"
            )
        ]

        # The placeholder is what will be shown when no option is selected.
        # The min and max values indicate we can only pick one of the three options.
        # The options parameter, contents shown above, define the dropdown options.
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
                f"> the, jejudo ` v{pkg_resources.get_distribution('jishaku').version} `, py-cord ` v{pkg_resources.get_distribution('py-cord').version} `".replace("\n", ""),
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

            await interaction.response.edit_message(
                content="\n".join(jejudo)
            )
        if self.values[0] == "protected_access page":
            jejudo = [
                f"> the, jejudo ` v{pkg_resources.get_distribution('jishaku').version} `, py-cord ` v{pkg_resources.get_distribution('py-cord').version} `".replace("\n", ""),
                f"ㄴ • Python ` {sys.version}`".replace("\n", ""),
                f"ㄴ • platform `{sys.platform}`".replace("\n", "")
            ]
            # pylint: disable=protected-access
            if self.bot._connection.max_messages:  # type: ignore
                message_cache = f"Message cache capped at {self.bot._connection.max_messages}"  # type: ignore
            else:
                message_cache = "Message cache is disabled"

            if discord.version_info >= (1, 5, 0):
                remarks = {
                    True: 'enabled',
                    False: 'disabled',
                    None: 'unknown'
                }

                *group, last = (
                    f"{intent.replace('_', ' ')} intent is {remarks.get(getattr(self.bot.intents, intent, None))}"
                    for intent in
                    ('presences', 'members', 'message_content')
                )

                jejudo.append(f"\n{message_cache},\n{', '.join(group)}, and {last}.")
            else:
                guild_subscriptions = f"guild subscriptions are {'enabled' if self.bot._connection.guild_subscriptions else 'disabled'}"  # type: ignore

                jejudo.append(f"\n{message_cache}\n{guild_subscriptions}.\n")

            # pylint: enable=protected-access

            # Show websocket latency in milliseconds
            jejudo.append(f"\n\nAverage websocket latency: {round(self.bot.latency * 1000, 2)}ms")

            await interaction.response.edit_message(
                content="\n".join(jejudo)
            )

class DropdownView(discord.ui.View):
    def __init__(self, bot_: discord.Bot, requester):
        self.bot = bot_
        self.requester = requester
        super().__init__()

        # Adds the dropdown to our View object
        self.add_item(Dropdown(self.bot, self.requester))

class Jejudos():
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command("jejudo",aliases=["jeju","jdo"],invoke_without_command=True, ignore_extra=False)
    @commands.is_owner()
    async def jejudo(self, ctx: commands.Context):


        jejudo = [
            f"> the, jejudo ` v{pkg_resources.get_distribution('jishaku').version} `, py-cord ` v{pkg_resources.get_distribution('py-cord').version} `".replace("\n", ""),
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
        await ctx.send("\n".join(jejudo), view=view)




