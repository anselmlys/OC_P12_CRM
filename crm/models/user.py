from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from crm.models.base import Base
from crm.models.client import Client
from crm.models.contract import Contract
from crm.models.event import Event


# employee_number to add later on

class User(Base):
    __tablename__= 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(
        Enum('sales', 'support', 'management', name='user_roles'),
        nullable=False
    )
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

    clients = relationship('Client', back_populates='sales_contact')
    events = relationship('Event', back_populates='support_contact')

    def __repr__(self):
        return f'User {self.id}'
