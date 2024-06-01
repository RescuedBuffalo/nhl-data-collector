# pytest to test the fetch_goal_leaders function in the data_collection_server
import unittest
from unittest.mock import patch
import datacollector

class TestFetchGoalLeaders(unittest.TestCase):
        
    def test_fetch_goal_leaders(self):
        app = datacollector.create_app()

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
            
            with app.app_context():
                response, status_code = datacollector.fetch_goal_leaders()
            
            assert status_code == 200
            assert response.json == {
                '1' : {'player_name': 'Connor McDavid', 'position': 'C', 'team': 'Oilers', 'goals': 10},
                '2' : {'player_name': 'Leon Draisaitl', 'position': 'LW', 'team': 'Oilers', 'goals': 9}
            }     

if __name__ == '__main__':
    unittest.main()
