import discord
from discord.ext import commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tickets", description="List all active tickets")
    async def tickets(self, ctx):
        # Get all channels that start with 'ticket-'
        ticket_channels = [channel for channel in ctx.guild.channels if channel.name.startswith('ticket-')]
        
        if not ticket_channels:
            await ctx.send("There are no active tickets.")
            return

        embed = discord.Embed(
            title="Active Tickets",
            description=f"Found {len(ticket_channels)} active tickets",
            color=discord.Color.blue()
        )

        for channel in ticket_channels:
            # Get the ticket creator from the channel name
            creator_name = channel.name.replace('ticket-', '')
            creator = discord.utils.get(ctx.guild.members, name=creator_name)
            
            if creator:
                embed.add_field(
                    name=f"Ticket: {channel.name}",
                    value=f"Created by: {creator.mention}\nChannel: {channel.mention}",
                    inline=False
                )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Tickets(bot)) 