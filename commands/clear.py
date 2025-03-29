import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", description="Clear all messages in a channel")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx):
        if not ctx.guild.me.guild_permissions.manage_messages:
            await ctx.send("I don't have permission to manage messages!")
            return

        try:
            await ctx.channel.purge()
            await ctx.send("All messages have been cleared!", delete_after=5)
        except discord.Forbidden:
            await ctx.send("I don't have permission to clear messages in this channel!")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(Clear(bot)) 