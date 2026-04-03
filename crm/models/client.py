from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

class Client(Base):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String)
    company_name = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
        )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
        )
    sales_contact_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))

    contracts = relationship('Contract', back_populates='client')
    sales_contact = relationship('User', back_populates='clients')

    def __repr__(self):
        return f'Client {self.id}'
