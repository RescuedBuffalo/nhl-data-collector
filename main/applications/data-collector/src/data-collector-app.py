from flask import Flask, jsonify, redirect, url_for, render_template
import requests, json, sqlite3, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Basic home route
@app.route('/')
def home():
    return "Welcome to the Data Collection Server!"

@app.route('/fetch-nhl-goal-leaders', methods=['GET'])
def fetch_goal_leaders():
    url = 'https://api-web.nhle.com/v1/skater-stats-leaders/current'

    try:
        response = requests.get(url, params={'categories': 'goals', 'limit': 10})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    if response.status_code == 200:
        data = response.json()
        
        # Create a json object to be returned to the client
        player_data = {}

        for player in data['goals']:
            player_id = player['id']
            player_name = f"{player['firstName']['default']} {player['lastName']['default']}"
            position = player['position']
            team = player['teamName']['default']
            goals = player['value']
            player_data[str(player_id)] = {'player_name': player_name, 'position': position, 'team': team, 'goals': goals}

        return jsonify(player_data), 200
    
    else:
        return {}, 500
    

@app.route('/game-log/<player_id>/game-log/<season>/<game_type>', methods=['GET'])
def fetch_nhl_game_logs(player_id, season, game_type):
    url = "https://api-web.nhle.com/v1/player/"
    try:
        response = requests.get(url + f"{player_id}/game-log/{season}/{game_type}")
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    if response.status_code == 200:
        game_data = {}
        for game in response.json()['gameLog']:
            data = {}
            game_id = str(game['gameId'])
            data['goals'] = game['goals']
            data['assists'] = game['assists']
            data['points'] = game['points']
            data['teamName'] = game['commonName']
            data['teamAbbreviation'] = game['teamAbbrev']
            data['opponentName'] = game['opponentCommonName']   
            data['gameDate'] = game['gameDate']        
            data['plusMinus'] = game['plusMinus']
            data['penaltyMinutes'] = game['pim']
            data['shots'] = game['shots']
            data['powerplayGoals'] = game['powerPlayGoals']
            data['powerplayPoints'] = game['powerPlayPoints']
            data['shorthandedGoals'] = game['shorthandedGoals']
            data['shorthandedPoints'] = game['shorthandedPoints']
            data['timeOnIce'] = game['toi']
            data['shifts'] = game['shifts']
            data['otGoals'] = game['otGoals']
            game_data[game_id] = data

        return jsonify(game_data), 200
    
    else:
        return {}, 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
