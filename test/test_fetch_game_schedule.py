# pytest to test the fetch_goal_leaders function in the data_collection_server
import unittest
import datacollector.app as datacollector

class TestFetchGameSchedule(unittest.TestCase):
        
    def test_fetch_game_schedule(self):
        app = datacollector.create_app()
        app.config['TESTING'] = True
            
        with app.app_context():
            response, status_code = datacollector.routes.get_game_schedule('2023-11-26')
        
        assert status_code == 200
        assert response.json['nextStartDate']  == '2023-11-26'
        assert response.json['gameWeek'][0]['numberOfGames'] == 0
        assert response.json['gameWeek'][1]['numberOfGames'] == 4

if __name__ == '__main__':
    unittest.main()
