import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import io

# Load environment variables
load_dotenv()

# setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='p/', intents=intents, help_command=None)  # disable default help so our own gets perfectly displayed

# Collections for commands and tickets
bot.tickets = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    
    # playing thingy
    await bot.change_presence(activity=discord.Game(name="Made with ♥ by preach."))

    # Loading all cogs beeb beep boop im a robot
    cogs = [
        'commands.help',
        'commands.userinfo',
        'commands.serverinfo',
        'commands.clear',
        'commands.delete',
        'commands.setticketpanel',
        'commands.tickets',
        'commands.addstaff',
        'commands.admin'
    ]
    
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"Loaded {cog}")
        except Exception as e:
            print(f"Failed to load {cog}: {e}")
    
    # Sync commands w dc
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    try:
        # handling the very good looking ticket menu selection
        if interaction.type == discord.InteractionType.component:
            if interaction.data.get('custom_id') == 'ticket_menu':
                category = interaction.data['values'][0]
                user = interaction.user
                guild = interaction.guild

                # creating the ticketchannel naming it ticket-username of the ticket creator
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                    guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
                }

                ticket_channel = await guild.create_text_channel(
                    name=f'ticket-{user.name}',
                    overwrites=overwrites
                )

                embed = discord.Embed(
                    title='🎫 New Support Ticket',
                    description=f'Welcome {user.mention}!\nOur support team will be with you shortly.',
                    color=discord.Color.green()
                )
                embed.add_field(name='Category', value=f'📋 {category.capitalize()}', inline=True)
                embed.add_field(name='Created By', value=user.mention, inline=True)
                embed.add_field(name='Instructions', value='Please describe your issue in detail. A staff member will assist you soon.\nTo close this ticket, click the button below.', inline=False)
                embed.set_footer(text=f'Ticket ID: {ticket_channel.id} | Created at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | A log of this conversation will be saved.')

                close_button = discord.ui.Button(
                    custom_id='close_ticket',
                    label='Close Ticket',
                    style=discord.ButtonStyle.danger,
                    emoji='🔒'
                )

                view = discord.ui.View()
                view.add_item(close_button)

                await ticket_channel.send(embed=embed, view=view)
                await interaction.response.send_message(f'✅ Ticket created in {ticket_channel.mention}!', ephemeral=True)

            # Handle close button click
            elif interaction.data.get('custom_id') == 'close_ticket':
                channel = interaction.channel
                user = interaction.user
                member = await channel.guild.fetch_member(user.id)

                # Check permissions
                if not member.guild_permissions.manage_channels and channel.name != f'ticket-{user.name}':
                    await interaction.response.send_message('❌ You do not have permission to close this ticket.', ephemeral=True)
                    return

                # Create confirmation embed
                confirm_embed = discord.Embed(
                    title='🔒 Close Ticket',
                    description='Are you sure you want to close this ticket?\nThis action cannot be undone.',
                    color=discord.Color.orange()
                )
                confirm_embed.add_field(name='Ticket', value=channel.name, inline=True)
                confirm_embed.add_field(name='Closing By', value=user.mention, inline=True)
                confirm_embed.add_field(name='User ID', value=user.id, inline = True)
                confirm_embed.set_footer(text='Click the buttons below to confirm or cancel')

                confirm_button = discord.ui.Button(
                    custom_id='confirm_close',
                    label='Close Ticket',
                    style=discord.ButtonStyle.danger,
                    emoji='✅'
                )

                cancel_button = discord.ui.Button(
                    custom_id='cancel_close',
                    label='Cancel',
                    style=discord.ButtonStyle.secondary,
                    emoji='❌'
                )

                view = discord.ui.View()
                view.add_item(confirm_button)
                view.add_item(cancel_button)

                await interaction.response.send_message(embed=confirm_embed, view=view, ephemeral=True)

            # Handle confirmation
            elif interaction.data.get('custom_id') == 'confirm_close':
                await handle_ticket_close(interaction)

            # Handle closeall confirmation
            elif interaction.data.get('custom_id') == 'confirm_closeall':
                ticket_channels = [channel for channel in interaction.guild.channels if channel.name.startswith('ticket-')]
                
                closing_embed = discord.Embed(
                    title='🔒 Closing All Tickets',
                    description=f'Closing {len(ticket_channels)} tickets...',
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=closing_embed)

                for channel in ticket_channels:
                    try:
                        await handle_ticket_close(interaction, channel)
                    except Exception as e:
                        print(f'Error closing ticket {channel.name}: {e}')

                final_embed = discord.Embed(
                    title='✅ All Tickets Closed',
                    description=f'Successfully closed {len(ticket_channels)} tickets.',
                    color=discord.Color.green()
                )
                await interaction.channel.send(embed=final_embed)

            # Handle cancellation
            elif interaction.data.get('custom_id') in ['cancel_close', 'cancel_closeall']:
                cancel_embed = discord.Embed(
                    title='❌ Operation Cancelled',
                    description='The ticket will remain open.',
                    color=discord.Color.grey()
                )
                await interaction.message.edit(embed=cancel_embed, view=None)

    except Exception as e:
        print(f'Error handling interaction: {e}')
        if interaction.response.is_done():
            await interaction.followup.send('There was an error processing your request. Please try again.', ephemeral=True)
        else:
            await interaction.response.send_message('There was an error processing your request. Please try again.', ephemeral=True)

async def handle_ticket_close(interaction, channel=None):
    channel = channel or interaction.channel
    user = interaction.user

    try:
        # Create transcript
        messages = []
        async for message in channel.history(limit=None, oldest_first=True):
            messages.append(f'[{message.created_at.strftime("%Y-%m-%d %H:%M:%S")}] {message.author} ({message.author.id}): {message.content}')

        transcript = f'📝 Ticket Transcript: {channel.name}\n'
        transcript += f'Ticket ID: {channel.id}\n'
        transcript += f'Closed by: {user}\n'
        transcript += f'Closed at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'
        transcript += '💬 Messages:\n' + '\n'.join(messages)

        # Find or create log channel
        logs_channel = discord.utils.get(channel.guild.channels, name='ticket-logs')
        if not logs_channel:
            logs_channel = await channel.guild.create_text_channel(
                name='ticket-logs',
                overwrites={
                    channel.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    channel.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
                }
            )

        # Send log
        log_embed = discord.Embed(
            title='🔒 Ticket Closed',
            description=f'Ticket `{channel.name}` has been closed',
            color=discord.Color.red()
        )
        log_embed.add_field(name='📋 Ticket', value=channel.name, inline=True)
        log_embed.add_field(name='👤 Closed By', value=user.mention, inline=True)
        log_embed.add_field(name='⏰ Closed At', value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        log_embed.set_footer(text=f'Ticket ID: {channel.id}')

        # Send notification to the channel before closing
        close_notification = discord.Embed(
            title='🔒 Ticket Closing',
            description='This ticket is now being closed.\nA transcript will be saved.',
            color=discord.Color.orange()
        )
        await channel.send(embed=close_notification)

        # Wait a moment for the message to be visible
        await asyncio.sleep(2)

        # Send transcript and log
        await logs_channel.send(
            embed=log_embed,
            file=discord.File(
                io.StringIO(transcript),
                filename=f'{channel.name}-transcript.txt'
            )
        )

        # Delete the channel
        await channel.delete()

    except Exception as e:
        print(f'Error during ticket closure: {e}')
        raise e

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN')) 