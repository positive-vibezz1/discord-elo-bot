import logging

class Team:
    def __init__(self, name, captain, player_IDs):
        """
        Initialize the Team class.

        Args:
            name: The name of the team.
            captain: The captain of the team.
            player_IDs: List of player IDs.
        """
        self.name = name
        self.captain = captain
        self.player_IDs = player_IDs
        self.members = self.fetch_players()

    def fetch_players(self):
        """
        Fetch the players of the team.

        Returns:
            A list of players including the captain and other team members.
        """
        try:
            return [self.captain] + [self.captain.guild.get_member(player_id) for player_id in self.player_IDs]
        except Exception as e:
            logging.error(f"An error occurred while fetching players: {e}")
            return []

    def get_member_ids(self):
        """
        Get the IDs of all team members.

        Returns:
            A list of member IDs.
        """
        return [member.id for member in self.members]

    def get_team_info(self):
        """
        Get information about the team.

        Returns:
            A string containing the team's name, captain, and players.
        """
        return f"Team: {self.name}\nCaptain: {self.captain.display_name}\nPlayers: {', '.join([player.display_name for player in self.members])}"

    def add_player(self, new_player):
        """
        Add a new player to the team.

        Args:
            new_player: The new player to add.

        Returns:
            True if the player was added, False otherwise.
        """
        if new_player.id not in self.get_member_ids():
            self.members.append(new_player)
            self.player_IDs.append(new_player.id)
            return True
        else:
            return False

    def remove_player(self, player):
        """
        Remove a player from the team.

        Args:
            player: The player to remove.

        Returns:
            True if the player was removed, False otherwise.
        """
        if player.id in self.get_member_ids() and player.id != self.captain.id:
            self.members.remove(player)
            self.player_IDs.remove(player.id)
            return True
        else:
            return False
