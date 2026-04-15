from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from crm.models.base import Base

class Contract(Base):
    __tablename__= 'contract'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='RESTRICT'), nullable=False)
    total_amount = Column(Integer)
    remaining_amount = Column(Integer)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    signed = Column(Boolean, default=False, nullable=False)

    client = relationship('Client', back_populates='contracts')
    event = relationship('Event', back_populates='contract', uselist=False)

    def __repr__(self):
        return f'Contract {self.id}'
