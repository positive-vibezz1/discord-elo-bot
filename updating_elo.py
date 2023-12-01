import math

class Update_rating:
    def __init__(self, rating_home, rating_away, won, weight):
        self.rating_home = rating_home
        self.rating_away = rating_away
        self.won = won
        self.weight = weight

    #this is the expected outcome of who is to win  the game, ie it allows us to adjust how much points are won and lost based on who has a higher rating    
    def expected_outcome(self):
        return 1 / (1 + 10**((self.rating_away - self.rating_home) / 400))
        
    #this function gives us the final updated rating of the teams      
    def update_elo_rating(self):
        expected_score = self.expected_outcome()
        rating_home_new = self.rating_home + self.weight * (self.won - expected_score)
        rating_home_new_rounded = math.floor(rating_home_new)
        rating_away_new = self.rating_away - self.weight * (self.won - expected_score)
        rating_home_away_rounded = math.floor(rating_away_new)
        return rating_home_new_rounded, rating_home_away_rounded





