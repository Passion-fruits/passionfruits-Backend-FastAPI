from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class Follow(Base):
    __tablename__ = "follow"

    follower = Column(Integer, ForeignKey("user.id"), primary_key=True)
    following = Column(Integer, ForeignKey("user.id"), primary_key=True)

    followers = relationship("User", backref=backref("follower_user"), foreign_keys=[follower])
    followings = relationship("User", backref=backref("following_user"), foreign_keys=[following])
