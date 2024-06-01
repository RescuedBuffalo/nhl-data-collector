# pytest to test the fetch_goal_leaders function in the data_collection_server
import unittest
from unittest.mock import patch
import datacollector.datacollector as datacollector

class TestFetchGoalLeaders(unittest.TestCase):
        
    def fetch_game_schedule(self):
        app = datacollector.create_app()
        app.config['TESTING'] = True
            
        with app.app_context():
            response, status_code = datacollector.fetch_game_schedule('2022-09-23')
        
        assert status_code == 200
        assert response.json['nextStartDate']  == '2022-09-30'
        assert response.json['gameWeek'][0]['numberOfGames'] == 0
        assert response.json['gameWeek'][1]['numberOfGames'] == 4

if __name__ == '__main__':
    unittest.main()
