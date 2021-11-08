from sqlalchemy import Column, Integer, ForeignKey, BIGINT
from sqlalchemy.orm import relationship, backref

from project.core.models import Base


class Kdt(Base):
    __tablename__ = "kdt"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    add_kdt = Column(BIGINT, nullable=False, server_default=0)
    donate_kdt = Column(BIGINT, nullable=False, server_default=0)
    reward_kdt = Column(BIGINT, nullable=False, server_default=0)

    user = relationship("User", backref=backref("kdt", order_by=user_id))
