import logging
import discord
import asyncio

class Substitute:
    def __init__(self, team_ratings, registered_users, bot):
        """
        Initialize the Substitute class.

        Args:
            team_ratings: Dictionary containing team ratings.
            registered_users: Set of registered user IDs.
            bot: The Discord bot instance.
        """
        self.team_ratings = team_ratings
        self.registered_users = registered_users
        self.registered_subs = set()
        self.bot = bot

    async def register_substitute(self, ctx):
        """
        Register a user as a substitute.

        Args:
            ctx: The context of the command.
        """
        # Check if the user is already on a team
        if any(role.name in self.team_ratings for role in ctx.author.roles) or ctx.author.id in self.registered_users:
            await ctx.send("You're already on a team. You cannot register as a substitute.")
            return

        # Prompt the user for Discord ID
        await ctx.send("Enter your Discord ID:")
        substitute_id = await self.get_user_input(ctx)

        # Check if the user is in the registered users
        if substitute_id in self.registered_users:
            # Check if the user is already registered as a substitute
            if any(substitute_id == sub[0] for sub in self.registered_subs):
                await ctx.send("You are already registered as a substitute.")
                return

            # Register the user as a substitute with 700 MMR
            self.registered_subs.add((substitute_id, 700))
            await ctx.send("You have been registered as a substitute.")

            # Assign "substitute" role to the user
            substitute_role = discord.utils.get(ctx.guild.roles, name="substitute")
            substitute_user = self.bot.get_user(int(substitute_id))
            
            if substitute_user:
                # Add the "substitute" role to the user
                await substitute_user.add_roles(substitute_role)
                await ctx.send("You have been registered as a substitute and assigned the 'substitute' role.")
            else:
                await ctx.send("Failed to find the user with the provided Discord ID. Make sure the ID is correct.")

    async def is_registered_substitute(self, ctx):
        """
        Check if a user is a registered substitute.

        Args:
            ctx: The context of the command.

        Returns:
            True if the user is a registered substitute, False otherwise.
        """
        # Prompt the user for Discord ID to check registration
        await ctx.send("Enter your Discord ID:")
        substitute_id = await self.get_user_input(ctx)

        # Check if the substitute is a registered substitute
        return any(substitute_id == sub[0] for sub in self.registered_subs)
            
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
