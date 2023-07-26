"""
Here are defined SQL Alchemy (ORM) models.
They are also used from Alembic (Migration Tool).
"""
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from sqlalchemy import (
    Column, Unicode,
    Integer, String,
    ForeignKey, Boolean
    )


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), nullable=False, unique=True)
    password = Column(String, nullable=False)

    movies = relationship("Movies", back_populates="user")
    likes = relationship("Likes", back_populates="user")


class Movies(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', 
                                         ondelete='CASCADE'),
                     nullable=False)
    title = Column(Unicode(100), nullable=False, unique=True)
    description = Column(Unicode(500), nullable=False)
    date = Column(TIMESTAMP(timezone=True),
                  server_default=text('NOW()'), nullable=False)
    user = relationship("Users", back_populates="movies",
                        cascade="all, delete")
    opinions = relationship("Opinions", 
                            back_populates="opinions",
                            cascade="all, delete")
    likes = Column(Integer, server_default="0")
    hates = Column(Integer, server_default="0")
    

class Opinions(Base):
    """
    A row in this table can be interpreted as
    user with id x likes (if opinion = 1) movie with id y
    or she hates it (if opinion = 0). 
    If a user/movie pair is not in the database, it means
    a user has not expressed her opinion for the movie.
    """
    __tablename__ = 'opinions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', 
                                         ondelete='CASCADE'),
                     nullable=False) 
    movie_id = Column(Integer, ForeignKey('movies.id', 
                                         ondelete='CASCADE'),
                     nullable=False) 
    
    opinion = Column(Boolean, 
                     nullable=False,
                     comment="Likes = 1, Hates = 0")
