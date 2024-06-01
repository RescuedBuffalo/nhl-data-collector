import unittest
from unittest.mock import patch
from datacollector import datacollector

class TestFetchPlayerStats(unittest.TestCase):

    def test_fetch_player_stats(self):
        app = datacollector.create_app()

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                'id': 8475786,
                'firstName': {'default': 'Connor'},
                'lastName': {'default': 'McDavid'},
                'primaryNumber': '97',
                'birthDate': '1997-01-13',
                'currentAge': 26,
                'birthCity': 'Richmond Hill',
                'birthStateProvince': 'ON',
                'birthCountry': 'CAN',
                'goals': 10,
                'assists': 20,
                'points': 30,
                'gamesPlayed': 10,
                'plusMinus': 5,
                'penaltyMinutes': 10,
                'shotPct': 10.0,
                'gameWinningGoals': 2,
                'overTimeGoals': 1,
                'shortHandedGoals': 1,
                'shortHandedPoints': 2,
                'powerPlayGoals': 3,
                'powerPlayPoints': 5,
            }

        with app.app_context():
            response, status_code = datacollector.fetch_player_stats(8475786)

        assert status_code == 200
        assert response.json == {
            'player_name': 'Connor McDavid',
            'primary_number': '97',
            'birth_date': '1997-01-13',
            'current_age': 26,
            'birth_city': 'Richmond Hill',
            'birth_state_province': 'ON',
            'birth_country': 'CAN',
            'goals': 10,
            'assists': 20,
            'points': 30,
            'games_played': 10,
            'plus_minus': 5,
            'penalty_minutes': 10,
            'shot_pct': 10.0,
            'game_winning_goals': 2,
            'overtime_goals': 1,
            'shorthanded_goals': 1,
            'shorthanded_points': 2,
            'powerplay_goals': 3,
            'powerplay_points': 5,
        }

if __name__ == '__main__':
    unittest.main()