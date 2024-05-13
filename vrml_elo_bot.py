import discord
import asyncio
import logging
from ranking_class import RankingCommand
from create_team import CreateTeam
from substitute import Substitute
import tracemalloc
import sqlite3
from discord.ext import commands

# Start tracking memory allocations
tracemalloc.start()

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize SQLite connection and cursor
try:
    conn = sqlite3.connect('elo_ratings.db')
    cursor = conn.cursor()
    logging.info("Connected to SQLite database successfully.")
except sqlite3.Error as e:
    logging.error(f"Failed to connect to SQLite database: {e}")

# Global variables for team ratings and registered users
team_ratings = {'test1': 600, 'test2': 600}
registered_users = set()

# Intents determine what events your bot will receive information about
intents = discord.Intents.default()
intents.message_content = True  # Add more if needed

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

# Initialize class instances for handling commands
team_commands = CreateTeam(bot, team_ratings, registered_users)
ranking_cmd = RankingCommand(bot, team_ratings, team_commands)
substitute_handler = Substitute(team_ratings, registered_users, bot)

@bot.event
async def on_ready():
    """
    Event handler for when the bot is ready.
    """
    logging.info(f'Logged in as {bot.user.name}')

@bot.command(name='submit_scores')
async def submit_scores(ctx):
    """
    Command to submit scores.
    """
    await ranking_cmd.score_submit(ctx)

@bot.command(name='create_team')
async def team_registration(ctx):
    """
    Command to create a team.
    """
    await team_commands.team_registration(ctx)

@bot.command(name='register_sub')
async def register_substitute(ctx):
    """
    Command to register a substitute.
    """
    await substitute_handler.register_substitute(ctx)
    await ctx.send("You have been registered as a substitute.")

@commands.command(name='test')
async def test(ctx):
    """
    Command to test the registration of substitutes.
    """
    if not substitute_handler.registered_subs:
        await ctx.send("No substitutes are currently registered.")
        return

    subs_list = "\n".join(f"Discord ID: {sub[0]}, MMR: {sub[1]}" for sub in substitute_handler.registered_subs)
    await ctx.send(f"Registered Substitutes:\n{subs_list}")

async def get_user_input(ctx, prompt):
    """
    Get input from the user.

    Args:
        ctx: The context of the command.
        prompt: The prompt message to display.

    Returns:
        The user's input as a string.
    """
    await ctx.send(prompt)
    try:
        response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=90)
        return response.content
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Command canceled.")
        return None

# Run the bot with the provided bot token
bot.run('BOT TOKEN')
