
import pytest
import requests
from flask_testing import TestCase
from unittest.mock import patch
from applications.data_collection_server.main.flask_app import data_collection_app

class TestFetchGameLog(TestCase):

    def create_app(self):
        data_collection_app.app.config['TESTING'] = True
        return data_collection_app.app
    
    def test_fetch_game_log(self):
       response, status_code = data_collection_app.fetch_nhl_game_logs(8475786, 20222023, 2)
       assert status_code == 200
       assert response.json["2022021308"]['gameDate'] == "2023-04-13"
       assert response.json["2022021308"]["goals"] == 0


if __name__ == '__main__':
    pytest.main()