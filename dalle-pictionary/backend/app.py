from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import Response, FileResponse
from pydantic import BaseModel
import base64
from numpy.random import randint
from .sentence_transformer import SentenceTransformer

sentence_transformer = SentenceTransformer()

class Image(BaseModel):
	id: str
	description: str
	base64: str

class SentenceSimilarityQuery(BaseModel):
	ground_truth: str
	guess: str

def base64_encode_image(path: Path) -> str:
	with open(path, "rb") as image_file:
		encoded_image_string = base64.b64encode(image_file.read())
	return encoded_image_string


def get_backend(image_base_path: Path) -> FastAPI:
	BASE_DIR = image_base_path
	text = [
		"A dinosaur hunting down an ice cream truck",
		"A high tech solarpunk utopia in the Amazon rainforest"
	]
	img_path = [
		"dinosaur_ice_cream.png",
		"rainforest_utopia.png"
	]
	num_images = len(text)

	app = FastAPI()

	@app.get("/")
	def root() -> str:
		return "App is up and ready to receive requests."

	@app.get("/image/file", response_class=FileResponse)
	def get_image_as_file() -> str:
		index = randint(0, num_images)
		return BASE_DIR+img_path[index]

	@app.get("/image/json", response_model=Image)
	def get_image_as_json() -> Image:
		index = randint(0, num_images)
		return Image(
			id=img_path[index],
			description=text[index],
			base64=base64_encode_image(Path(BASE_DIR+img_path[index]))
		)

	@app.post("/predict")
	def predict_sentence_similarity(description_pair: SentenceSimilarityQuery) -> float:
		result = sentence_transformer.sentence_similarity(
			source=description_pair.ground_truth,
			query=description_pair.guess
		)
		return {"similarity": result.item()}

	return app

backend = get_backend("./data/img/")
