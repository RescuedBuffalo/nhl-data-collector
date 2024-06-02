from flask import Blueprint, jsonify
from datacollector.models import Team, Player, Game, Record, Season

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Welcome to the Data Collection Server!"

@main.route('/fetch-nhl-goal-leaders', methods=['GET'])
def get_goal_leaders():
    goal_leaders = NHLGoalLeaders.query.all()
    return jsonify([leader.to_dict() for leader in goal_leaders]), 200

@main.route('/game-log/<player_id>/game-log/<season>/<game_type>', methods=['GET'])
def get_nhl_game_logs(player_id, season, game_type):
    game_logs = NHLGameLog.query.filter_by(player_id=player_id).all()
    return jsonify([log.to_dict() for log in game_logs]), 200

@main.route('/player/<player_id>', methods=['GET'])
def get_player_stats(player_id):
    player_stats = NHLPlayerStats.query.filter_by(player_id=player_id).first()
    return jsonify(player_stats.to_dict()), 200

@main.route('/fetch_game_schedule/<date>', methods=['GET'])
def get_game_schedule(date):
    game_schedule = NHLGameSchedule.query.filter_by(date=date).first()
    return jsonify(game_schedule.to_dict()), 200
