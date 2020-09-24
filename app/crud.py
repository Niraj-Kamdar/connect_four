import pickle

from sqlalchemy.orm import Session

from . import models
from .game import Connect4


def load_game(db_game):
    return pickle.loads(db_game.game)


def get_game_by_id(db: Session, id: int):
    return db.query(models.Game).filter(models.Game.id == id).first()


def get_game_state(db_game: models.Game):
    game = load_game(db_game)
    return {"id": db_game.id, "board": game.matrix.tolist(), "turn": game.turn.value}


def update_game(db: Session, db_game: models.Game, game: Connect4):
    db_game.game = pickle.dumps(game)
    db.commit()
    db.refresh(db_game)
    return db_game


def delete_game_by_id(db: Session, id: int):
    db.query(models.Game).filter(models.Game.id == id).delete(synchronize_session="fetch")
    db.commit()


def create_game(db: Session):
    db_game = models.Game(game=pickle.dumps(Connect4()))
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game
