from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    DateTime
)

from .meta import Base


class Entry(Base):
    """Model our journal entries."""
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(DateTime)
