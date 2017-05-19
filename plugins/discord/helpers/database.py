import os

import discord
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class UserDB(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(250), unique=True)
    nickname = Column(String(250), unique=True)
    battletag = Column(String(250))
    diablo_char = Column(Integer)


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True)
    value = Column(String(250))


class Database:
    def __init__(self):
        self.engine = create_engine(os.environ.get("DISCORD_DB"))
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()

    def register_user(self, user: discord.user) -> str:
        if self.db.query(UserDB).filter(UserDB.user_id == user.id).count():
            return "Already registered"
        else:
            self.db.add(UserDB(user_id=user.id))
            self.db.commit()
            return "{0.mention} now registered, welcome!".format(user)

    def edit_nickname(self, user: discord.user, nickname: str) -> str:
        if not self.db.query(UserDB).filter(UserDB.user_id == user.id).count():
            return "You need to register first"
        else:
            self.db.query(UserDB).filter(UserDB.user_id == user.id).update({UserDB.nickname: nickname})
            self.db.commit()
            return "{1.mention} will now register under nickname {0}".format(nickname, user)

    def edit_diablo_char(self, user: discord.user, char: str) -> str:
        if not self.db.query(UserDB).filter(UserDB.user_id == user.id).count():
            return "You need to register first"
        else:
            self.db.query(UserDB).filter(UserDB.user_id == user.id).update({UserDB.diablo_char: char})
            self.db.commit()
            return "Diablo character {0} now registered to {1.mention}".format(char, user)

    def edit_battletag(self, user: discord.user, battletag: str) -> str:
        if not self.db.query(UserDB).filter(UserDB.user_id == user.id).count():
            return "You need to register first"
        else:
            self.db.query(UserDB).filter(UserDB.user_id == user.id).update({UserDB.battletag: battletag})
            self.db.commit()
            return "Battletag {0} now registered to {1.mention}".format(battletag, user)

    def get_nickname(self, user: discord.user):
        if not self.db.query(UserDB).filter(UserDB.user_id == user.id).count():
            return False
        else:
            return self.db.query(UserDB).filter(UserDB.user_id == user.id).one().nickname

    def get_battletag_by_nick(self, nickname: str):
        if not self.db.query(UserDB).filter(UserDB.nickname == nickname).count():
            return False
        else:
            return self.db.query(UserDB).filter(UserDB.nickname == nickname).one().battletag

    def get_battletag(self, user: discord.user):
        if not self.db.query(UserDB).filter(UserDB.user_id == user.id).count():
            return False
        else:
            return self.db.query(UserDB).filter(UserDB.user_id == user.id).one().battletag

    def get_diablo_char(self, user: discord.user):
        if not self.db.query(UserDB).filter(UserDB.user_id == user.id).count():
            return False
        else:
            return self.db.query(UserDB).filter(UserDB.user_id == user.id).one().diablo_char
