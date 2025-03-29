import discord
from discord.ext import commands
from datetime import datetime

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="admin", description="Admin commands for ticket management")
    @commands.has_permissions(administrator=True)
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please specify a subcommand: closeall, stats")

    @admin.command(name="closeall", description="Close all active tickets")
    async def closeall(self, ctx):
        # Get all ticket channels
        ticket_channels = [channel for channel in ctx.guild.channels if channel.name.startswith('ticket-')]
        
        if not ticket_channels:
            await ctx.send("There are no active tickets to close.")
            return

        # Create confirmation embed
        confirm_embed = discord.Embed(
            title="Confirm Close All Tickets",
            description=f"Are you sure you want to close {len(ticket_channels)} tickets? This action cannot be undone.",
            color=discord.Color.red()
        )
        confirm_embed.add_field(name="Tickets to Close", value="\n".join([channel.mention for channel in ticket_channels]), inline=False)

        confirm_button = discord.ui.Button(
            custom_id='confirm_closeall',
            label='Confirm Close All',
            style=discord.ButtonStyle.danger,
            emoji='✅'
        )

        cancel_button = discord.ui.Button(
            custom_id='cancel_closeall',
            label='Cancel',
            style=discord.ButtonStyle.secondary,
            emoji='❌'
        )

        view = discord.ui.View()
        view.add_item(confirm_button)
        view.add_item(cancel_button)

        await ctx.send(embed=confirm_embed, view=view)

    @admin.command(name="stats", description="Show ticket statistics")
    async def stats(self, ctx):
        # Get all ticket channels
        ticket_channels = [channel for channel in ctx.guild.channels if channel.name.startswith('ticket-')]

        # Create stats embed
        embed = discord.Embed(
            title="Ticket Statistics",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Total Active Tickets", value=len(ticket_channels), inline=True)
        
        # Add timestamp
        embed.set_footer(text=f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Admin(bot)) 