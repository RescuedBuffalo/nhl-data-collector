import requests
import sqlite3
import pandas as pd
import datetime
import argparse
import time

def fetch_player_season(player_id, conn):
    url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player stats: {e}")
        return
    
    player_stats = response.json()['featuredStats']['regularSeason']['subSeason']
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO seasons (id, player_id, goals, assists, points, pp_goals, pp_points, sh_goals, sh_points, gw_goals, shots, games_played, pim)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        int(str(player_stats['season']) + str(player_id)),
        player_id,
        player_stats['goals'],
        player_stats['assists'],
        player_stats['points'],
        player_stats['powerPlayGoals'],
        player_stats['powerPlayPoints'],
        player_stats['shorthandedGoals'],
        player_stats['shorthandedPoints'],
        player_stats['gameWinningGoals'],
        player_stats['shots'],
        player_stats['gamesPlayed'],
        player_stats['pim']
    ))
    conn.commit()

def fetch_game_schedule(date, conn):
    url = f"https://api-web.nhle.com/v1/score/{date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching game schedule: {e}")
        return
    
    cursor = conn.cursor()
    for game in response.json()['games']:
        winner = game['homeTeam']['abbrev'] if game['homeTeam']['score'] > game['awayTeam']['score'] else game['awayTeam']['abbrev']
        cursor.execute('''
            INSERT OR REPLACE INTO games (id, date, season, game_type, home_id, away_id, home_goals, away_goals, winner)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            game['id'],
            game['gameDate'],
            game['season'],
            game['gameType'],
            game['homeTeam']['abbrev'],
            game['awayTeam']['abbrev'],
            game['homeTeam']['score'],
            game['awayTeam']['score'],
            winner
        ))
    conn.commit()

def fetch_teams_and_records(conn):
    url = "https://api-web.nhle.com/v1/standings/now"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching teams: {e}")
        return
    
    cursor = conn.cursor()
    for item in response.json()['standings']:
        cursor.execute('''
            INSERT OR REPLACE INTO teams (id, name) VALUES (?, ?)
        ''', (
            item['teamAbbrev']['default'],
            item['teamName']['default']
        ))
        cursor.execute('''
            INSERT OR REPLACE INTO records (id, team_id, wins, losses, ot_losses, so_losses, goals_for, goals_against)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            str(item['seasonId']) + str(item['teamAbbrev']['default']),
            item['teamAbbrev']['default'],
            item['wins'],
            item['losses'],
            item['otLosses'],
            item['shootoutLosses'],
            item['goalFor'],
            item['goalAgainst']
        ))
    conn.commit()

def fetch_roster_by_season(team_id, season, conn):
    url = f"https://api-web.nhle.com/v1/roster/{team_id}/{season}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching roster: {e}")
        return

    cursor = conn.cursor()
    for player in response.json()['forwards'] + response.json()['defensemen'] + response.json()['goalies']:
        cursor.execute('''
            INSERT OR REPLACE INTO players (id, first_name, last_name, team_id)
            VALUES (?, ?, ?, ?)
        ''', (
            player['id'],
            player['firstName']['default'],
            player['lastName']['default'],
            team_id
        ))
    conn.commit()

def backfill_games(start_date, conn):
    dates = pd.date_range(start=start_date, end=datetime.datetime.now().strftime('%Y-%m-%d'), freq='W-SUN').strftime('%Y-%m-%d')
    for date in dates:
        fetch_game_schedule(date, conn)
        time.sleep(60)

def backfill_seasons(conn):
    cursor = conn.cursor()
    # Select all player IDs from the players table
    cursor.execute('SELECT id FROM players')
    player_ids = cursor.fetchall()
    for player_id in player_ids:
        fetch_player_season(player_id[0], conn)
        time.sleep(60)

def backfill_rosters(conn):
    cursor = conn.cursor()
    # Select all team IDs from the teams table
    cursor.execute('SELECT id FROM teams')
    team_ids = cursor.fetchall()
    for team_id in team_ids:
        fetch_roster_by_season(team_id[0], 20232024, conn)
        time.sleep(60)

def backfill_teams(conn):
    fetch_teams_and_records(conn)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch NHL data and store in the database.')
    parser.add_argument('--date', type=str, help='The date to fetch the game schedule for, in YYYY-MM-DD format.')
    parser.add_argument('--player_id', type=int, help='The player ID to fetch the game logs and player stats for.')
    parser.add_argument('--season', type=str, help='The season to fetch the game logs for.')
    parser.add_argument('--game_type', type=str, help='The game type to fetch the game logs for.')
    parser.add_argument('--fetch_teams', action='store_true', help='Fetch teams and their records.')
    parser.add_argument('--fetch_roster', action='store_true', help='Fetch roster by season.')
    parser.add_argument('--backfill_games', type=str, help='Backfill the game schedule starting from the given date.')
    parser.add_argument('--backfill_seasons', action='store_true', help='Backfill player seasons.')
    parser.add_argument('--backfill_rosters', action='store_true', help='Backfill team rosters.')
    parser.add_argument('--backfill_teams', action='store_true', help='Backfill teams and their records.')

    args = parser.parse_args()

    conn = sqlite3.connect('../app/nhl_stats.db')

    if args.fetch_teams:
        fetch_teams_and_records(conn)
    if args.fetch_roster:
        team_ids = [team[0] for team in conn.execute('SELECT id FROM teams')]
        for team in team_ids:
            fetch_roster_by_season(team, 20232024, conn)
    if args.date:
        fetch_game_schedule(args.date, conn)
    if args.player_id:
        fetch_player_season(args.player_id, conn)
    if args.backfill_games:
        backfill_games(args.backfill, conn)
    if args.backfill_seasons:
        backfill_seasons(conn)
    if args.backfill_rosters:
        backfill_rosters(conn)
    if args.backfill_teams:
        backfill_teams(conn)
    
    conn.close()
