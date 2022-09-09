from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Image(Base):
	__tablename__ = "image"

	id = Column(Integer, primary_key=True, index=True)
	description = Column(String, index=True)
	base64= Column(String)


class Prediction(Base):
	__tablename__ = "prediction"

	id = Column(Integer, primary_key=True, index=True)
	guess_description = Column(String, index=True)
	similarity_score = Column(Float)

	image_id = Column(Integer, ForeignKey("image.id"))