import requests
from datacollector.app import create_app, db
from datacollector.models import Season, Game, Team, Player, Record

app = create_app()

def fetch_game_logs(player_id, season, game_type):
    url = f"https://api-web.nhle.com/v1/player/{player_id}/game-log/{season}/{game_type}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching game logs: {e}")
        return
    
    game_logs = response.json()['gameLog']
    for game in game_logs:
        game_log = NHLGameLog(
            player_id=player_id,
            game_id=game['gameId'],
            goals=game['goals'],
            assists=game['assists'],
            points=game['points'],
            team_name=game['commonName'],
            team_abbreviation=game['teamAbbrev'],
            opponent_name=game['opponentCommonName'],
            game_date=game['gameDate'],
            plus_minus=game['plusMinus'],
            penalty_minutes=game['pim'],
            shots=game['shots'],
            powerplay_goals=game['powerPlayGoals'],
            powerplay_points=game['powerPlayPoints'],
            shorthanded_goals=game['shorthandedGoals'],
            shorthanded_points=game['shorthandedPoints'],
            time_on_ice=game['toi'],
            shifts=game['shifts'],
            ot_goals=game['otGoals']
        )
        db.session.merge(game_log)
    db.session.commit()

def fetch_player_season(player_id):
    url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player stats: {e}")
        return
    
    player_stats = response.json()['featuredStats']
    player_stat = NHLPlayerStats(
        id = int(str(player_stats['season']) + str(player_id)),
        player_id=player_id,
        goals=player_stats['regularSeason']['subSeason']['goals'],
        assists=player_stats['regularSeason']['subSeason']['assists'],
        points=player_stats['regularSeason']['subSeason']['points'],
        pp_goals=player_stats['regularSeason']['subSeason']['powerPlayGoals'],
        pp_points=player_stats['regularSeason']['subSeason']['powerPlayPoints'],
        sh_goals=player_stats['regularSeason']['subSeason']['shorthandedGoals'],
        sh_points=player_stats['regularSeason']['subSeason']['shorthandedPoints'],
        gw_goals=player_stats['regularSeason']['subSeason']['gameWinningGoals'],
        shots=player_stats['regularSeason']['subSeason']['shots'],
        games_played=player_stats['regularSeason']['subSeason']['gamesPlayed'],
        pim=player_stats['regularSeason']['subSeason']['pim']
    )
    db.session.merge(player_stat)
    db.session.commit()

def fetch_game_schedule(date):
    url = f"https://api-web.nhle.com/v1/schedule/fetch_game_schedule/{date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching game schedule: {e}")
        return
    
    game_schedule = response.json()
    schedule = NHLGameSchedule(
        date=date,
        data=game_schedule
    )
    db.session.merge(schedule)
    db.session.commit()

def fetch_teams_and_records():
    url = "https://api-web.nhle.com/v1/standings/now"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching teams: {e}")
        return
    
    for item in response.json()['standings']:
        team = Team(
            id=item['teamAbbrev']['default'],
            name=item['teamName']['default']
        )
        db.session.merge(team)
        record = Record(
            id=str(item['seasonId']) + str(item['teamAbbrev']['default']),
            team_id=item['teamAbbrev']['default'],
            wins=item['wins'],
            losses=item['losses'],
            ot_losses=item['otLosses'],
            so_losses=item['shootoutLosses'],
            goals_for=item['goalFor'],
            goals_against=item['goalAgainst']
        )
        db.session.merge(record)
    db.session.commit()

    
    

if __name__ == '__main__':
    with app.app_context():
        fetch_teams_and_records()
