import discord
import os
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.guild_only()
    async def sync(self, ctx: commands.Context) -> None:
        syncedL = await self.bot.tree.sync(guild=discord.Object(os.environ.get("GUILD_ID")))
        syncedG = await self.bot.tree.sync()
        await ctx.send(f"Synced {len(syncedG)} commands globally and {len(syncedL)} locally.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Owner(bot), guild=discord.Object(os.environ.get("GUILD_ID")))
