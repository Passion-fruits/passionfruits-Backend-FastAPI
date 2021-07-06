from sqlalchemy import Column, Integer, VARCHAR

from project.core.models import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(100), nullable=False)
