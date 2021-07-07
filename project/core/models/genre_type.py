from sqlalchemy import Column, Integer, VARCHAR

from project.core.models import Base


class Genre_type(Base):
    __tablename__ = "genre_type"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(12), nullable=False)
