from sqlalchemy import Column, Integer, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class Profile(Base):
    __tablename__ = "profile"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    name = Column(VARCHAR(30), nullable=False)
    bio = Column(VARCHAR(250))
    image_path = Column(VARCHAR(150))

    user = relationship("User", backref=backref("profiles", order_by=user_id))
