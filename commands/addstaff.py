import discord
from discord.ext import commands

class AddStaff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addstaff", description="Add a staff member to a ticket")
    async def addstaff(self, ctx, member: discord.Member):
        # check if the channel is a ticket using ticket-
        if not ctx.channel.name.startswith('ticket-'):
            await ctx.send("This command can only be used in ticket channels!")
            return

        # Check user permissions to chekc channels
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("You don't have permission to add staff members to tickets!")
            return

        try:
            # add user to the channel by using the user ID
            await ctx.channel.set_permissions(member,
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )

            embed = discord.Embed(
                title="Staff Member Added",
                description=f"{member.mention} has been added to the ticket by {ctx.author.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("I don't have permission to modify channel permissions!")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(AddStaff(bot)) 