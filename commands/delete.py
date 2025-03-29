import discord
from discord.ext import commands

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="delete", description="Delete x amount of messages")
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, amount: int):
        if not ctx.guild.me.guild_permissions.manage_messages:
            await ctx.send("I don't have permission to manage messages!") # give the bot permissions lol
            return

        if amount < 1 or amount > 100:
            await ctx.send("Please specify a number between 1 and 100!")
            return

        try:
            await ctx.channel.purge(limit=amount + 1)  # +1 to also delete the command message
            await ctx.send(f"Deleted {amount} messages!", delete_after=5)
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete messages in this channel!")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(Delete(bot)) 