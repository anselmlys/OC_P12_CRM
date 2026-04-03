from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from base import Base

class Event(Base):
    __tablename__= 'event'

    id = Column(Integer, primary_key=True)
    contract_id = Column(
        Integer,
        ForeignKey('contract.id', ondelete='CASCADE'),
        nullable=False,
        unique=True
    )
    start_date = Column(Date)
    end_date = Column(Date)
    support_contact_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='SET NULL')
    )
    location = Column(String)
    number_of_attendees = Column(Integer)
    notes = Column(Text)

    contract = relationship('Contract', back_populates='event')
    support_contact = relationship('User', back_populates='events')

    def __repr__(self):
        return f'Event {self.id}'
