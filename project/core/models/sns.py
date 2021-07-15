from sqlalchemy import Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class Sns(Base):
    __tablename__ = "sns"

    profile_user_id = Column(Integer, ForeignKey("profile.user_id"), primary_key=True)
    insta = Column(VARCHAR(150))
    facebook = Column(VARCHAR(150))
    soundcloud = Column(VARCHAR(150))
    youtube = Column(VARCHAR(150))

    profile = relationship("Profile", backref=backref("sns"))
