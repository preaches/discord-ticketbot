import discord
from discord import app_commands
from discord.ext import commands

class SetTicketPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setticketpanel", description="Set up the ticket panel with dropdown menu")
    @commands.has_permissions(administrator=True)
    async def setticketpanel_prefix(self, ctx):
        await self.create_ticket_panel(ctx)

    @app_commands.command(name="setticketpanel", description="Set up the ticket panel with dropdown menu")
    @app_commands.default_permissions(administrator=True)
    async def setticketpanel_slash(self, interaction: discord.Interaction):
        await self.create_ticket_panel(interaction)

    async def create_ticket_panel(self, ctx_or_interaction):
        is_interaction = isinstance(ctx_or_interaction, discord.Interaction)
        
        embed = discord.Embed(
            title='🎫 Ticket Bot',
            description='To create a ticket, select a category from the dropdown menu below.\nOur support team will assist you as soon as possible.',
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name='📋 Available Categories',
            value='**🔧 Technical Support**\n' +
                  'For technical issues, bugs, or errors\n\n' +
                  '**❓ General Support**\n' +
                  'For general questions and assistance\n\n' +
                  '**💰 Billing Support**\n' +
                  'For payment and subscription issues\n\n' +
                  '**📝 Other**\n' +
                  'For any other inquiries',
            inline=False
        )
        
        embed.set_footer(text='Select a category below to create a ticket')

        select = discord.ui.Select(
            custom_id='ticket_menu',
            placeholder='Select ticket category',
            options=[
                discord.SelectOption(
                    label='Technical Support',
                    description='For technical issues, bugs, or errors',
                    value='technical',
                    emoji='🔧'
                ),
                discord.SelectOption(
                    label='General Support',
                    description='For general questions and assistance',
                    value='general',
                    emoji='❓'
                ),
                discord.SelectOption(
                    label='Billing Support',
                    description='For payment and subscription issues',
                    value='billing',
                    emoji='💰'
                ),
                discord.SelectOption(
                    label='Other',
                    description='For any other inquiries',
                    value='other',
                    emoji='📝'
                )
            ]
        )

        view = discord.ui.View(timeout=None)
        view.add_item(select)

        if is_interaction:
            await ctx_or_interaction.response.send_message('✅ Ticket panel has been set up!', ephemeral=True)
            await ctx_or_interaction.channel.send(embed=embed, view=view)
        else:
            await ctx_or_interaction.send('✅ Ticket panel has been set up!')
            await ctx_or_interaction.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(SetTicketPanel(bot)) 