from db.base_class import Base
from sqlalchemy import String, Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Posts(Base):
    id = Column(Integer, primary_key=True, index=True)
    img_url = Column(String, unique=True, nullable=False)
    img_url_type = Column(String, nullable=False)
    caption = Column(String, nullable=False)
    timestamp = Column(DateTime)
    creator_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='posts')