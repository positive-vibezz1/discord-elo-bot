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
        games_scores = []
        
        #try:
                #team_home = simpledialog.askstring("Input", "Enter home team:")
        try:
            team_home = await get_user_input(ctx, "Enter home team:")
            rating_home = team_ratings.get(team_home)
            
        except KeyError:
            await ctx.send(f"Team '{team_home}' not found in team data base.")
            return
        
        try:
            team_away = await get_user_input(ctx, "Enter away team:")
            rating_away = team_ratings.get(team_away)
        
        except KeyError:
            await ctx.send(f"Team '{team_away}' not found in team data base.")
            return

        

        for game_number in range(1, 4):
            try:
                scores_input = await get_user_input(ctx, f"Enter scores for Game {game_number} (separated by comma):")
                scores_input_stripped = scores_input.strip()
                print(f"Debug: scores_input received for Game {game_number}: {scores_input}")
                score_home, score_away = map(int, scores_input_stripped.split(','))

                # Append the scores to the list
                games_scores.append((score_home, score_away))

            except ValueError:
                await ctx.send(f"Invalid input for Game {game_number}. Please enter scores in the format 'home,away'.")
                return

        

        # Example usage in your existing code    
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
        
        return games_scores
     
@bot.command(name='create_team')
async def team_registration(ctx):
    if ctx.channel.id == 1180168660778745978:
        guild = ctx.guild        
        await ctx.send("lets create your team...")
        
        root = tk.Tk()
        root.withdraw()
        initial_rating = 600
        
        try:
            team_name = await get_user_input(ctx, "Enter team name:")
            
            team_ratings[team_name] = initial_rating
            
            
            
        except ValueError:
            await ctx.send("Invalid input. Please enter a valid team name and initial rating.")
            
        try:
            players = await get_user_input(ctx, "Enter yours players discord id (separated by comma):")
            player_ID = list(map(int, players.split(',')))
            
        except ValueError:
            await ctx.send("Invalid input. Please enter scores in the format 'home,away'.")
            return

        existing_role = discord.utils.get(guild.roles, name=team_name)
        
        if existing_role:
            await ctx.send(f"Role '{team_name}' already exists.")
            return

        # Create the role
        new_role = await guild.create_role(name=team_name) 
        
        #add players to team       
        for player_id in player_ID:
            player = await guild.fetch_member(player_id)
            if player:
               await player.add_roles(new_role)
            else:
                await ctx.send(f"Player with ID {player_id} not found.")
                

        await ctx.author.add_roles(new_role)
        await ctx.send(f"Team '{team_name}' has been successfully registered to the EAML, and roles have been given.")    
        
async def get_user_input(ctx, prompt):
    await ctx.send(prompt)
    #await ctx.send(score)
    response = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
    return response.content



          
bot.run('BOT TOKEN')
