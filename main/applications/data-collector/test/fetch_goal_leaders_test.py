# pytest to test the fetch_goal_leaders function in the data_collection_server

import pytest
import requests
from flask_testing import TestCase
from unittest.mock import patch
from applications.data_collection_server.main.flask_app import data_collection_app

class TestFetchGoalLeaders(TestCase):

    def create_app(self):
        data_collection_app.app.config['TESTING'] = True
        return data_collection_app.app
        
    def test_fetch_goal_leaders(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                'goals': [
                    {
                        'id': 1,
                        'firstName': {'default': 'Connor'},
                        'lastName': {'default': 'McDavid'},
                        'position': 'C',
                        'teamName': {'default': 'Oilers'},
                        'value': 10
                    },
                    {
                        'id': 2,
                        'firstName': {'default': 'Leon'},
                        'lastName': {'default': 'Draisaitl'},
                        'position': 'LW',
                        'teamName': {'default': 'Oilers'},
                        'value': 9
                    }
                ]
            }
            
            response, status_code = data_collection_app.fetch_goal_leaders()
            
            assert status_code == 200
            assert response.json == {
                '1' : {'player_name': 'Connor McDavid', 'position': 'C', 'team': 'Oilers', 'goals': 10},
                '2' : {'player_name': 'Leon Draisaitl', 'position': 'LW', 'team': 'Oilers', 'goals': 9}
            }     

if __name__ == '__main__':
    pytest.main()
