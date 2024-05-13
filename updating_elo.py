import math
import logging

class Update_rating:
    def __init__(self, rating_home, rating_away, won, weight):
        """
        Initialize the Update_rating class.

        Args:
            rating_home: Rating of the home team.
            rating_away: Rating of the away team.
            won: Boolean indicating if the home team won.
            weight: The weight for the Elo rating calculation.
        """
        self.rating_home = rating_home
        self.rating_away = rating_away
        self.won = won
        self.weight = weight

    def expected_outcome(self):
        """
        Calculate the expected outcome based on the ratings.

        Returns:
            The expected outcome as a float.
        """
        try:
            return 1 / (1 + 10**((self.rating_away - self.rating_home) / 400))
        except Exception as e:
            logging.error(f"An error occurred while calculating the expected outcome: {e}")
            return None

    def update_elo_rating(self):
        """
        Update the Elo ratings for both teams.

        Returns:
            A tuple containing the new ratings for the home and away teams.
        """
        try:
            expected_score = self.expected_outcome()
            if expected_score is None:
                raise ValueError("Expected score calculation failed.")

            rating_home_new = self.rating_home + self.weight * (self.won - expected_score)
            rating_home_new_rounded = math.floor(rating_home_new)

            rating_away_new = self.rating_away - self.weight * (self.won - expected_score)
            rating_away_new_rounded = math.floor(rating_away_new)

            return rating_home_new_rounded, rating_away_new_rounded
        except Exception as e:
            logging.error(f"An error occurred while updating Elo ratings: {e}")
            return None, None
