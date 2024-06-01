import unittest
from unittest.mock import patch
from datacollector import datacollector

class TestFetchGameLog(unittest.TestCase):
    
    def test_fetch_game_log(self):
        app = datacollector.create_app()

        with app.app_context():
            response, status_code = datacollector.fetch_nhl_game_logs(8475786, 20222023, 2)

        assert status_code == 200
        assert response.json["2022021308"]['gameDate'] == "2023-04-13"
        assert response.json["2022021308"]["goals"] == 0



if __name__ == '__main__':
    unittest.main()