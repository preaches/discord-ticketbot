import discord
from discord.ext import commands
from datetime import datetime

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", description="Show information about a user")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        roles = [role.mention for role in member.roles[1:]]  # Exclude @everyone
        roles_str = ", ".join(roles) if roles else "None"
        
        embed = discord.Embed(
            title=f"User Information - {member.name}",
            color=member.color
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Roles", value=roles_str, inline=False)
        
        if member.premium_since:
            embed.add_field(name="Nitro Since", value=member.premium_since.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfo(bot)) 