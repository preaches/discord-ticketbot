import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Show all available commands")
    @app_commands.describe(command="Specific command to get help for")
    async def help(self, ctx, command: str = None):
        if command:
            cmd = self.bot.get_command(command)
            if cmd:
                embed = discord.Embed(
                    title=f"Help: {cmd.name}",
                    description=cmd.description or "No description available",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Usage", value=f"`p/{cmd.name}`", inline=False)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(f"Command `{command}` not found.")
                return

        # general help
        embed = discord.Embed(
            title="Commands",
            description="Here are all available commands:",
            color=discord.Color.blue()
        )

        # General Commands
        embed.add_field(
            name="🛠️ General Commands",
            value="`p/help` - Shows this help message\n"
                  "`p/userinfo [@user]` - Shows user information\n"
                  "`p/serverinfo` - Shows server information",
            inline=False
        )

        # Moderation Commands
        embed.add_field(
            name="⚔️ Moderation Commands",
            value="`p/clear` - Clears all messages in a channel\n"
                  "`p/delete <number>` - Deletes specified number of messages",
            inline=False
        )

        # Ticket System
        embed.add_field(
            name="🎫 Ticket System",
            value="`p/tickets` - Lists all active tickets\n"
                  "`p/addstaff @user` - Adds a staff member to a ticket\n"
                  "`p/setticketpanel` - Creates the ticket creation panel",
            inline=False
        )

        # Admin Commands
        embed.add_field(
            name="👑 Admin Commands",
            value="`p/admin closeall` - Closes all active tickets\n"
                  "`p/admin stats` - Shows ticket statistics",
            inline=False
        )

        embed.set_footer(text="Bot made with ❤️ | Use p/ before each command")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
