import logging
import asyncio
from discord.ext import commands
from substitute import Substitute


class RankingCommand:
    def __init__(self, bot, team_ratings, create_team_instance):
        """
        Initialize the RankingCommand class.

        Args:
            bot: The Discord bot instance.
            team_ratings: Dictionary containing team ratings.
            create_team_instance: Instance of CreateTeam class.
        """
        self.bot = bot
        self.team_ratings = team_ratings
        self.create_team_instance = create_team_instance
        self.registered_users = set()
        self.substitute_handler = Substitute(team_ratings, self.registered_users, bot)
        self.ranking_and_teams_channel = 1181350917975584818

    @commands.command(name='submit_scores')
    async def score_submit(self, ctx):
        """
        Command to submit scores and update Elo ratings.

        Args:
            ctx: The context of the command.
        """
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
            
            if scores_home is None or scores_away is None:
                await ctx.send("Score submission canceled due to timeout or error.")
                return

            # Process and update the Elo ratings
            updater = UpdateRating(self.team_ratings, team_home, team_away, scores_home, scores_away)
            await updater.process(ctx)
            await ctx.send("Elo ratings updated successfully.")
        else:
            await ctx.send("Please use this command in the correct channel.")

    async def collect_scores(self, ctx, team_home, team_away):
        """
        Collect scores from the teams.

        Args:
            ctx: The context of the command.
            team_home: The home team instance.
            team_away: The away team instance.

        Returns:
            A list of scores submitted by the teams.
        """
        try:
            await ctx.send(f"{team_home.mention} captain, please submit your scores for {team_away.mention}.")
            scores_home = await self.get_user_input(ctx, "Enter your scores (comma-separated):")
            scores_home = list(map(int, scores_home.split(',')))
            return scores_home
        except ValueError:
            await ctx.send("Invalid input. Please enter valid scores.")
            return None
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Command canceled.")
            return None
        except Exception as e:
            logging.error(f"An error occurred while collecting scores: {e}")
            await ctx.send("An error occurred while collecting scores. Please try again.")
            return None

    async def process_substitute(self, ctx, team, team_rating, won):
        """
        Process the substitute information.

        Args:
            ctx: The context of the command.
            team: The team instance.
            team_rating: The rating of the team.
            won: Boolean indicating if the team won.
        """
        substitute_needed = True

        if substitute_needed:
            await ctx.send("It seems there was a substitute player. Please provide the following details:")
            substitute_id = await self.get_user_input(ctx, "Enter the Discord ID of the substitute:")
            substitute_username = await self.get_user_input(ctx, "Enter the Discord username of the substitute:")

            if not self.substitute_handler.is_registered_substitute(substitute_id):
                await ctx.send("The provided Discord ID is not registered as a substitute. Processing canceled.")
                return

            substitute_mmr = self.substitute_handler.get_substitute_mmr(substitute_id)
            if not self.substitute_handler.check_mmr_range(substitute_mmr, team_rating):
                await ctx.send("Substitute's MMR is not within the allowed range. Processing canceled.")
                return

            won = 1 if won else 0
            substitute_rating = self.substitute_handler.update_substitute_mmr(substitute_id, won)

            await ctx.send(f"Updated MMR for substitute with Discord ID {substitute_id}: {substitute_rating}")

    async def get_user_input(self, ctx, prompt):
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
            response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=90)
            return response.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond. Command canceled.")
            return None
