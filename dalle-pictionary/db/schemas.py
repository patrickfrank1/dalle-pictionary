from pydantic import BaseModel


class ImageBase(BaseModel):
	description: str
	base64: str


class ImageCreate(ImageBase):
	pass


class Image(ImageBase):
	id: int

	class Config:
		orm_mode = True


class PredictionBase(BaseModel):
	guess_description: str
	similarity_score: str
	image_id: int


class PredictionCreate(PredictionBase):
	pass


class Prediction(PredictionBase):
	id: int

	class Config:
		orm_mode = True