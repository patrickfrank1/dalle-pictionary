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
	image_id: int
	leaderboard_name: str
	guess_description: str
	similarity_score: str
	


class PredictionCreate(PredictionBase):
	pass


class Prediction(PredictionBase):
	id: int

	class Config:
		orm_mode = True