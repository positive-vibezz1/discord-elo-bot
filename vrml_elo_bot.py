import discord
import asyncio
from ranking_class import ranking_command
from create_team import CreateTeam
from substitute import Substitute
import tracemalloc
tracemalloc.start()
import sqlite3
from discord.ext import commands




tracemalloc.start()
# Initialize SQLite connection and cursor
conn = sqlite3.connect('elo_ratings.db')
cursor = conn.cursor()

team_ratings = {'test1': 600, 'test2': 600}
registered_users = set()

# Intents determine what events your bot will receive information about
intents = discord.Intents.default()
intents.message_content = True  # Add more if needed

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)


#this is our class handling stuff
team_commands = CreateTeam(bot, team_ratings, registered_users)
ranking_cmd = ranking_command(bot, team_ratings, team_commands)

#command channels
ranking_and_teams_channel = 1181350917975584818

#class initation 
substitute_handler = Substitute(team_ratings, registered_users, bot)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command(name='submit_scores')
async def submit_scores(ctx):
    # Call methods of your ranking_command /instance
    await ranking_cmd.score_submit(ranking_cmd, ctx)


@bot.command(name='create_team')
async def team_registration(ctx):
    await team_commands.team_registration(ctx)


@bot.command(name='register_sub')
async def register_substitute(ctx):
    await substitute_handler.register_substitute(ctx)
    await ctx.send("You have been registered as a substitute.")

@commands.command(name='test')
async def test(self, ctx):
    if not self.registered_subs:
        await ctx.send("No substitutes are currently registered.")
        return

    subs_list = "\n".join(f"Discord ID: {sub[0]}, MMR: {sub[1]}" for sub in self.registered_subs)
    await ctx.send(f"Registered Substitutes:\n{subs_list}")

      
async def get_user_input(ctx, prompt):
    await ctx.send(prompt)
    #await ctx.send(score)
    response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=90)
    return response.content

        
bot.run('BOT TOKEN')
