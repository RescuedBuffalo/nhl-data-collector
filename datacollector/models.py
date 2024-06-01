from . import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    records = db.relationship('Record', backref='team', lazy=True)
    players = db.relationship('Player', backref='team', lazy=True)
    home_games = db.relationship('Game', foreign_keys='Game.home_id', backref='home_team', lazy=True)
    away_games = db.relationship('Game', foreign_keys='Game.away_id', backref='away_team', lazy=True)

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    seasons = db.relationship('Season', backref='player', lazy=True)

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    home_goals = db.Column(db.Integer, nullable=False)
    away_goals = db.Column(db.Integer, nullable=False)
    winner = db.Column(db.String(100), nullable=False)

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    wins = db.Column(db.Integer, nullable=False)
    losses = db.Column(db.Integer, nullable=False)
    ot_losses = db.Column(db.Integer, nullable=False)
    so_losses = db.Column(db.Integer, nullable=False)
    goals_for = db.Column(db.Integer, nullable=False)
    goals_against = db.Column(db.Integer, nullable=False)

class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    goals = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    pp_goals = db.Column(db.Integer, nullable=False)
    pp_points = db.Column(db.Integer, nullable=False)
    sh_goals = db.Column(db.Integer, nullable=False)
    sh_points = db.Column(db.Integer, nullable=False)
    gw_goals = db.Column(db.Integer, nullable=False)
    blocks = db.Column(db.Integer, nullable=False)
    hits = db.Column(db.Integer, nullable=False)
