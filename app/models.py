from sqlalchemy import Column, Integer, LargeBinary

from .database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    game = Column(LargeBinary)
