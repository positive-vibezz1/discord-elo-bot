import discord
from teams import Team

class CreateTeam:
    def __init__(self, bot, team_ratings, registered_users):
        self.bot = bot
        self.team_ratings = team_ratings
        self.registered_users = registered_users
        self.teams = {}
        
        
    ranking_and_teams_channel = 1181350917975584818
      
    async def get_team_and_rating(self, ctx, team_type):
        team_name = await self.get_user_input(ctx, f"Enter {team_type} team:")
        rating = self.team_ratings.get(team_name, 600)  # Default rating to 600 if not found

        team_instance = self.create_team_instance.teams.get(team_name)
        if team_instance is None:
            print(f"Debug: Team instance for '{team_name}' not found.")
            await ctx.send(f"Team '{team_name}' instance not found. Score submission canceled.")
            return None, None

        return team_instance, rating
        
    async def get_user_input(self, ctx, prompt):
        await ctx.send(prompt)
        response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=90)
        return response.content
    
    def is_captain(self, user):
        for role in user.roles:
            if role.name in self.team_ratings:
                return True
        return False
        
    async def team_registration(self, ctx):

        # Check if the command is being used in the correct channel
        if ctx.channel.id != self.ranking_and_teams_channel:
            await ctx.send("Please use this command in the correct channel.")
            return

        guild = ctx.guild
        captain_role = discord.utils.get(guild.roles, name="captain")

        # Check if user is already on a team
        if any(role.name in self.team_ratings for role in ctx.author.roles) or ctx.author.id in self.registered_users:
            await ctx.send("You're already on a team.")
            return

        await ctx.send("Let's create your team...")

        initial_rating = 600

        try:
            # Get user input for the team name
            team_name = await self.get_user_input(ctx, "Enter team name:")
            self.team_ratings[team_name] = initial_rating

        except ValueError:
            await ctx.send("Invalid input. Please enter a valid team name and initial rating.")
            return

        try:
            # Get user input for the captain's ID
            captain_id = await self.get_user_input(ctx, "Enter captain ID:")
            captain_id = int(captain_id.strip())

            member = await guild.fetch_member(captain_id)

            if member:
                await member.add_roles(captain_role)
            else:
                await ctx.send(f"User with ID {captain_id} not found.")
                return

        except ValueError:
            await ctx.send("Invalid input. Please enter a valid user ID.")
            return

        try:
            # Get user input for player IDs
            players = await self.get_user_input(ctx, "Enter player IDs (separated by comma):")
            player_IDs = list(map(int, players.split(',')))

        except ValueError:
            await ctx.send("Invalid input. Please enter valid user IDs.")
            return

        # Create a new Team instance
        new_team = Team(team_name, ctx.author, player_IDs)  # Assuming Team takes team_name, captain, player_IDs as parameters

        # Add the team to the dictionary
        self.teams[team_name] = new_team

        # Check if any player is already on a team or registered
        for player_id in player_IDs:
            player = await guild.fetch_member(player_id)

            if any(role.name in self.team_ratings for role in player.roles) or player.id in self.registered_users:
                await ctx.send(f"Player with ID {player_id} is already on a team or registered to another team.")
                return

        existing_role = discord.utils.get(guild.roles, name=team_name)

        if existing_role:
            await ctx.send(f"Role '{team_name}' already exists.")
            return

        new_role = await guild.create_role(name=team_name)

        # Add the captain to the new role
        await ctx.author.add_roles(new_role)
        # Add the captain to the set of registered users
        self.registered_users.add(ctx.author.id)

        for player_id in player_IDs:
            player = await guild.fetch_member(player_id)

            if player:
                # Add each player to the new role
                await player.add_roles(new_role)
                # Add the player to the set of registered users
                self.registered_users.add(player.id)
            else:
                await ctx.send(f"Player with ID {player_id} not found.")

        await ctx.send(f"Team '{team_name}' has been successfully registered to the EAML, players have joined teams, and roles have been given.")
