from updating_elo import Update_rating
import discord
import asyncio
from discord.ext import commands
from substitute import Substitute


class ranking_command:

    def __init__(self, bot, team_ratings, create_team_instance):
        self.bot = bot
        self.team_ratings = team_ratings
        self.create_team_instance = create_team_instance
        registered_users = set()
        substitute_handler = Substitute(team_ratings, registered_users, bot)
    
    ranking_and_teams_channel = 1181350917975584818

    @commands.command(name='submit_scores')
    async def score_submit(self, ctx):
        if ctx.channel.id == self.ranking_and_teams_channel:
            await ctx.send("Updating Elo...")

            team_home, rating_home = await self.get_team_and_rating(ctx, "home")
            team_away, rating_away = await self.get_team_and_rating(ctx, "away")

            # Check if both teams exist
            if team_home is None or team_away is None:
                await ctx.send("Score submission canceled due to invalid team names.")
                return

            # Check if the author is the captain of either team
            if not (self.create_team_instance.is_captain(ctx.author) and (ctx.author in team_home.members or ctx.author in team_away.members)):
                await ctx.send("You are not the captain of either team. Score submission canceled.")
                return

            # Prompt the home team captain to submit scores
            await ctx.send(f"{team_home.mention}, please submit scores for your team.")
            scores_home = await self.collect_scores(ctx, team_home, team_away)

            # Mention the opposing team's captain to submit scores
            await ctx.send(f"{team_away.captain.mention}, your opposing team ({team_home.mention}) has submitted scores. Please submit scores for your team.")

            # Prompt the away team captain to submit scores
            scores_away = await self.collect_scores(ctx, team_away, team_home)

            # Check if both teams submitted matching scores
            if scores_home == scores_away:
                await self.process_scores(ctx, team_home, team_away, rating_home, rating_away, scores_home)
            else:
                await ctx.send("Scores provided by both teams do not match. Please make sure both teams submit the same scores.")

    async def get_team_and_rating(self, ctx, team_type):
        team_name = await self.get_user_input(ctx, f"Enter {team_type} team:")
        rating = self.team_ratings.get(team_name, 600)  # Default rating to 600 if not found

        if team_name not in self.team_ratings:
            print(f"Debug: Team '{team_name}' not found in team_ratings.")
            await ctx.send(f"Team '{team_name}' not found in team database. Using default rating.")
            return None, None  # Return None for team and rating

        team_instance = self.create_team_instance.teams.get(team_name)
        if team_instance is None:
            print(f"Debug: Team instance for '{team_name}' not found.")
            await ctx.send(f"Team '{team_name}' instance not found. Score submission canceled.")
            return None, None

        return team_instance, rating
    
    async def collect_scores(self, ctx, team1, team2):
        games_scores = []
        for game_number in range(1, 4):
            try:
                scores_input = await self.get_user_input(ctx, f"Enter scores for Game {game_number} (separated by comma) between {team1} and {team2}:")
                scores_input_stripped = scores_input.strip()
                print(f"Debug: scores_input received for Game {game_number}: {scores_input}")
                score_team1, score_team2 = map(int, scores_input_stripped.split(','))

                # Append the scores to the list
                games_scores.append((score_team1, score_team2))

            except ValueError:
                await ctx.send(f"Invalid input for Game {game_number}. Please enter scores in the format 'team1,team2'.")

        return games_scores

    async def process_scores(self, ctx, team_home, team_away, rating_home, rating_away, games_scores):
        team_home_wins = 0
        team_away_wins = 0
        substitute_needed = True

        for game_number, (score_home, score_away) in enumerate(games_scores, start=1):
            if score_home > score_away:
                team_home_wins += 1
            elif score_home < score_away:
                team_away_wins += 1

        # Determine the overall winner
        if team_home_wins > team_away_wins:
            won = 1
        elif team_home_wins < team_away_wins:
            won = 0
        else:
            won = .5 #its a tie

        weight = 20
        updating_elo = Update_rating(rating_home, rating_away, won, weight)

        game_outcome_weight = updating_elo.expected_outcome()

        new_rating_teams = updating_elo.update_elo_rating()

        self.team_ratings[team_home.name] = new_rating_teams[0]
        self.team_ratings[team_away.name] = new_rating_teams[1]

        print(f"expected outcome is: {game_outcome_weight}")
        print(f"New Rating for {team_home}: {new_rating_teams[0]}")
        print(f"New Rating for {team_away}: {new_rating_teams[1]}")

        await ctx.send(f"New Rating for {team_home}: {new_rating_teams[0]}")
        await ctx.send(f"New Rating for {team_away}: {new_rating_teams[1]}")
        
        if substitute_needed:
            await ctx.send("yas there a substitue? (yes/no)")
            substitute_played = await self.get_user_input(ctx, "Enter 'yes' or 'no':")

            if substitute_played.lower() == 'yes':
                await self.process_substitute(ctx, team_home, rating_home, won)
                # Add similar logic for the away team if needed
            else:
                await ctx.send("No substitute played in this match.")
    
    async def process_substitute(self, ctx, team, team_rating, won):
        # Prompt the user for substitute information
        substitute_needed = True

        if substitute_needed:
            await ctx.send("It seems there was a substitute player. Please provide the following details:")
            # Prompt for substitute details, such as Discord ID, username, etc.
            substitute_id = await self.get_user_input(ctx, "Enter the Discord ID of the substitute:")
            substitute_username = await self.get_user_input(ctx, "Enter the Discord username of the substitute:")

            # Check if the substitute is registered
            if not self.substitute_handler.is_registered_substitute(substitute_id):
                await ctx.send("The provided Discord ID is not registered as a substitute. Processing canceled.")
                return

            # Check MMR range
            substitute_mmr = self.substitute_handler.get_substitute_mmr(substitute_id)
            if not self.substitute_handler.check_mmr_range(substitute_mmr, team_rating):
                await ctx.send("Substitute's MMR is not within the allowed range. Processing canceled.")
                return

            # Update substitute's MMR based on the match outcome
            won = 1 if won else 0
            substitute_rating = self.substitute_handler.update_substitute_mmr(substitute_id, won)

            await ctx.send(f"Updated MMR for substitute with Discord ID {substitute_id}: {substitute_rating}")
    
    async def get_user_input(self, ctx, prompt):
        await ctx.send(prompt)
        try:
            response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=90)
            return response.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Command canceled.")
            return None
