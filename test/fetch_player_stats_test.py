import unittest
from unittest.mock import patch
import datacollector.datacollector as datacollector

class TestFetchPlayerStats(unittest.TestCase):

    def test_fetch_player_stats(self):
        app = datacollector.create_app()

        with app.app_context():
            response, status_code = datacollector.fetch_players_stats(8475786)

        assert status_code == 200
        assert response['firstName']['default'] == 'Zach'
        assert response['lastName']['default'] == 'Hyman'
        assert response['sweaterNumber'] == 18

if __name__ == '__main__':
    unittest.main()