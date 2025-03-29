# Discord Ticket Bot (it isnt perfect...a lot of stuff still needs to be fixed!!!)

A Discord bot that creates a ticket system with a dropdown menu for different support categories.

## Features

- Create tickets through a dropdown menu
- Multiple ticket categories (General, Technical, Billing, Other)
- Ticket transcripts
- Automatic log channel creation
- Permission-based ticket management
- Confirmation system for ticket closure

## Setup

1. Install Python 3.8 or higher
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

- `/setticketpanel` - Set up the ticket panel with dropdown menu (Admin only)

## Usage

1. Use `/setticketpanel` in the channel where you want the ticket panel to appear
2. Users can create tickets by selecting a category from the dropdown menu
3. Tickets will be created in the server's default category
4. Users can close their own tickets or admins can close any ticket
5. When a ticket is closed, a transcript will be sent to the ticket-logs channel

## Permissions Required

The bot needs the following permissions:
- Manage Channels
- Send Messages
- Embed Links
- Attach Files
- Read Message History
- View Channels
- Manage Messages

## Notes

- The bot will automatically create a 'ticket-logs' channel if it doesn't exist
- Only administrators can use the `/setticketpanel` command
- Users can only close their own tickets unless they have admin permissions 
