from sqlalchemy import Column, String, Integer

from database import Base

class Recipe(Base):
    __tablename__ = 'Recipe'
    id = Column(Integer, primary_key=True, index=True)
    title_of_dish = Column(String, index=True)
    description = Column(String, index=True)
    ingredients = Column(String, index=True)
    preparing_time_in_min = Column(Integer, index=True)
    view_count = Column(Integer, index=True)
