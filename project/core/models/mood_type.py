from sqlalchemy import Column, Integer, VARCHAR

from project.core.models import Base


class Mood_type(Base):
    __tablename__ = "mood_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(16), nullable=False)
