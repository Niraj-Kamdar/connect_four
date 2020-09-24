from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def index():
    """ Index page of the website """
    index_path = Path("app") / "static" / "index.html"
    with index_path.open("r") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)


@app.post("/start/", responses={200: {"description": "Game is Ready!"}}, response_model=schemas.GameBase)
def start_game(db: Session = Depends(get_db)):
    """ Creates new game instance """
    return crud.create_game(db=db)


@app.delete("/game/{game_id}", responses={200: {"description": "Game aborted successfully!"}},
            response_model=schemas.Message)
def stop_game(game_id: int, db: Session = Depends(get_db)):
    """ Stops game with given game_id """
    crud.delete_game_by_id(db, game_id)
    return {"message": f"Game: {game_id} aborted successfully!"}


@app.get("/game/{game_id}", response_model=schemas.GameState)
def read_game_state(game_id: int, db: Session = Depends(get_db)):
    """
    Returns information of current game:
    - **id**: ID of the current game
    - **board**: board state of the current game
    - **turn**: Yellow or Red
    """
    db_game = crud.get_game_by_id(db=db, id=game_id)
    if db_game:
        return crud.get_game_state(db_game)
    else:
        raise HTTPException(status_code=400, detail=f"Game: {game_id} is invalid!")


@app.put("/game/{game_id}", responses={
    406: {"description": "Move is invalid!", "model": schemas.MessageGameState},
    200: {"description": "Move registered successfully!", "model": schemas.MessageGameState},
})
def make_move(game_id: int, column: int, db: Session = Depends(get_db)):
    """ Make move if it is valid """
    db_game = crud.get_game_by_id(db=db, id=game_id)
    if not db_game:
        raise HTTPException(status_code=400, detail=f"Game: {game_id} is invalid!")

    game = crud.load_game(db_game)
    try:
        winner = game.play(column)
    except ValueError:
        return JSONResponse(
            status_code=406,
            content={"message": f"Move: {column} is invalid!", **crud.get_game_state(db_game)},
        )
    if winner:
        crud.delete_game_by_id(db, game_id)
        return JSONResponse(
            status_code=200,
            content={"message": f"Player {winner} wins!", "id": game_id, "board": game.matrix.tolist(),
                     "turn": game.turn.value},
        )
    else:
        crud.update_game(db, db_game, game)
        return JSONResponse(
            status_code=200,
            content={"message": f"Move: {column} is registered successfully!", **crud.get_game_state(db_game)},
        )
