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

team_ratings = {'test1': 600, 'test2': 600}
# Intents determine what events your bot will receive information about
intents = discord.Intents.default()
intents.message_content = True  # Add more if needed

# Create a bot instance with a command prefix
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
      

@bot.command(name='test')
async def score_submit(ctx):
    if ctx.channel.id == 1180168660778745978:
        await ctx.send("Updating Elo...")
        
        root = tk.Tk()
        root.withdraw()
        
        #try:
                #team_home = simpledialog.askstring("Input", "Enter home team:")
        try:
            team_home = simpledialog.askstring("Input", "Enter home team:")
            rating_home = team_ratings[team_home]
            
        except KeyError:
            await ctx.send(f"Team '{team_home}' not found in team data base.")
            return
        
        try:
            team_away = simpledialog.askstring("Input", "Enter away team:")
            rating_away = team_ratings[team_away]
        
        except KeyError:
            await ctx.send(f"Team '{team_away}' not found in team data base.")
            return
    
        try:
            scores_input = simpledialog.askstring("Input", "Enter game scores (separated by comma):")
            score_home, score_away = map(int, scores_input.split(','))
            
        except ValueError:
            await ctx.send("Invalid input. Please enter scores in the format 'home,away'.")
            return
    
        if score_home > score_away:
            won = 1
            
        elif score_home < score_away:
            won = 0

        else:
            won = .5
            
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
        
        await ctx.send(f"New Rating for { team_home}: {new_rating_teams[0]}")
        await ctx.send(f"New Rating for { team_away}: {new_rating_teams[1]}")
     
@bot.command(name='register_team')
async def team_registration(ctx):
    if ctx.channel.id == 1180168660778745978:
        guild = ctx.guild        
        await ctx.send("Adding team to data base...")
        
        root = tk.Tk()
        root.withdraw()
        initial_rating = 600
        
        try:
            team_name = simpledialog.askstring("Input", "Enter team name:")
            
            team_ratings[team_name] = initial_rating
            
            await ctx.send(f"Team '{team_name}' has been successfully registered to the EAML, and roles have been given.")
            
        except ValueError:
            await ctx.send("Invalid input. Please enter a valid team name and initial rating.")
            
        try:
            players = simpledialog.askstring("Input", "Enter yours players discord id (separated by comma):")
            player_ID = list(map(int, players.split(',')))
            
        except ValueError:
            await ctx.send("Invalid input. Please enter scores in the format 'home,away'.")
            return

        existing_role = discord.utils.get(guild.roles, name=team_name)
        
        if existing_role:
            await ctx.send(f"Role '{team_name}' already exists.")
            return

        
        for player_id in player_ID:
            player = guild.get_member(player_id)
            if player:
               await player.add_roles(new_role)
            else:
                await ctx.send(f"Player with ID {player_ID} not found.")
                
        # Create the role
        new_role = await guild.create_role(name=team_name)
        await ctx.author.add_roles(new_role)     
        
          
bot.run('MTE4MDE2MjgwNzk3MTQ0Njc5NQ.G37B7z.QOYaJiRjXTzkdVV5U5eMp1QGMrkV9rYHLy0BWI')
