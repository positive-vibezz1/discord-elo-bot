import discord
from discord.ext import commands
from calculated_expected_outcome import CalculateExpectedScore
from updating_elo import Update_rating
import sqlite3
import tkinter as tk
from tkinter import simpledialog

# Initialize SQLite connection and cursor
conn = sqlite3.connect('elo_ratings.db')
cursor = conn.cursor()

team_ratings = {'Silly_Willy': 800, 'Lunch_Room_Bandits': 600}
# Intents determine what events your bot will receive information about
intents = discord.Intents.default()
intents.message_content = True  # Add more if needed

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')  

@bot.command(name='game-report')
async def test(ctx):   
        await ctx.channel.send("Did you win or lose? Type `!won` or `!lost` then type in your team and opponent team.")

@bot.command(name='won')
async def win(ctx):
     if ctx.channel.id == 1180168660778745978:
        await ctx.send("Updating Elo...")
        
        root = tk.Tk()
        root.withdraw()
    
        team_home = simpledialog.askstring("Input", "Enter home team:")
        team_away = simpledialog.askstring("Input", "Enter away team:")
        try:
                won = int(simpledialog.askstring("Input", "Enter game outcome: 1 for win, 0 for loss"))
        except:
                simpledialog.askstring("use 1 for win and zero for a loss")

        rating_home = team_ratings[team_home]
        rating_away = team_ratings[team_away]
        
        weight = 20
        game_weight = Update_rating(rating_home, rating_away, won, weight)

        updating_elo = Update_rating(rating_home, rating_away, won, weight)

        game_outcome_weight = game_weight.expected_outcome()

        new_rating_teams = updating_elo.update_elo_rating()
        
        team_ratings[team_home] = new_rating_teams[0]
        team_ratings[team_away] = new_rating_teams[1]

        print(f"expected outcome is: {game_outcome_weight}")

        print(f"New Rating for teams: {new_rating_teams}")
        
        await ctx.send(f"New Rating for teams: {new_rating_teams}")

'''
@bot.command(name='lost')
async def lost(ctx):
     if ctx.channel.id == 1180168660778745978:
        response = 0
        await ctx.send("Updating Elo...")
    
        # Example usage:
        team_home = "Silly_Willy"
        team_away = "Lunch_Room_Bandits"

        rating_home = team_ratings[team_home]
        rating_away = team_ratings[team_away]
        
        won = response
        weight = 20
        game_weight = Update_rating(rating_home, rating_away, won, weight)

        updating_elo = Update_rating(rating_home, rating_away, won, weight)

        game_outcome_weight = game_weight.expected_outcome()

        new_rating_teams = updating_elo.update_elo_rating()
        
        team_ratings[team_home] = new_rating_teams[0]
        team_ratings[team_away] = new_rating_teams[1]

        print(f"expected outcome is: {game_outcome_weight}")

        print(f"New Rating for teams: {new_rating_teams}")
        
        await ctx.send(f"New Rating for teams: {new_rating_teams}")
'''        
        
bot.run('MTE4MDE2MjgwNzk3MTQ0Njc5NQ.G-l2wm.HlsSNYCFGTlxHIkq4Ye7XTzw_zi-l0JyAZP_q8')
