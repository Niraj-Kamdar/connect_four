from typing import List

from pydantic import BaseModel


class GameBase(BaseModel):
    id: int

    class Config:
        orm_mode = True


class GameState(GameBase):
    board: List[List[str]]
    turn: str


class Message(BaseModel):
    message: str


class MessageGameState(Message, GameState):
    pass
