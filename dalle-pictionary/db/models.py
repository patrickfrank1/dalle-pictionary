from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Image(Base):
	__tablename__ = "image"

	id = Column(Integer, primary_key=True, index=True)
	description = Column(String, index=True)
	base64= Column(String)


class Prediction(Base):
	__tablename__ = "prediction"

	id = Column(Integer, primary_key=True, index=True)
	leaderboard_name = Column(String)
	guess_description = Column(String)
	similarity_score = Column(Float)

	image_id = Column(Integer, ForeignKey("image.id"))