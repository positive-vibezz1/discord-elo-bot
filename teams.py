class Team:
    def __init__(self, name, captain, player_IDs):
        self.name = name
        self.captain = captain
        self.player_IDs = player_IDs
        #self.members = members
        
    def fetch_players(self):
        # You might need to modify this depending on your use case
        return [self.captain] + [self.captain.guild.get_member(player_id) for player_id in self.player_IDs]

    def get_member_ids(self):
        return [member.id for member in self.members]

    def get_team_info(self):
        return f"Team: {self.name}\nCaptain: {self.captain.display_name}\nPlayers: {', '.join([player.display_name for player in self.members])}"

    def add_player(self, new_player):
        if new_player.id not in self.get_member_ids():
            self.members.append(new_player)
            self.player_IDs.append(new_player.id)
            return True
        else:
            return False

    def remove_player(self, player):
        if player.id in self.get_member_ids() and player.id != self.captain.id:
            self.members.remove(player)
            self.player_IDs.remove(player.id)
            return True
        else:
            return False