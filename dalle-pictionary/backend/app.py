from pathlib import Path
from typing import Generator, List
from fastapi import FastAPI, Depends
import base64
from pydantic import BaseModel
from numpy.random import randint
from sqlalchemy.orm import Session
from .sentence_transformer import SentenceTransformer
from ..db import database, crud, schemas

def get_db() -> Generator:
	try:
		db = database.SessionLocal()
		yield db
	finally:
		db.close()

def base64_encode_image(path: Path) -> str:
	with open(path, "rb") as image_file:
		encoded_image_string = base64.b64encode(image_file.read())
	return encoded_image_string

def filter_top_predictions(sorted_predictions: List[schemas.Prediction], k=5) -> List[schemas.Prediction]:
	top_k_predictions = []
	for i, item in enumerate(sorted_predictions):
		if len(top_k_predictions) == k:
			break
		if i == 0:
			top_k_predictions.append(item)
			continue

		previous_item = sorted_predictions[i-1]
		
		if item.guess_description == previous_item.guess_description:
			continue
		else:
			top_k_predictions.append(item)

	return top_k_predictions

class SimilarityQuery(BaseModel):
	image_id: int
	actual_description: str
	guess_description:str
	leaderboard_name: str = "John Doe"

def get_backend(image_base_path: Path) -> FastAPI:
	
	app = FastAPI()

	@app.get("/")
	def root() -> str:
		return "App is up and ready to receive requests."

	@app.get("/image/json", response_model=schemas.Image)
	def get_image_as_json(db: Session = Depends(get_db)) -> schemas.Image:
		index = randint(0, NUM_IMAGES) + 1
		return crud.get_image(db, index)

	@app.post("/predict", response_model=schemas.Prediction)
	def predict_sentence_similarity(query: SimilarityQuery, db: Session = Depends(get_db)) -> float:
		result = sentence_transformer.sentence_similarity(
			source=query.actual_description,
			query=query.guess_description
		).item()
		prediction = schemas.PredictionCreate(
			image_id=query.image_id,
			leaderboard_name=query.leaderboard_name,
			guess_description=query.guess_description,
			similarity_score=result
		)
		return crud.create_prediction(db, prediction)

	@app.get("/leaderboard")
	def get_leaderboard(image_id: int, k: int = 5, db: Session = Depends(get_db)):
		sorted_predictions = crud.get_sorted_predictions_by_image(db, image_id)
		return filter_top_predictions(sorted_predictions, k=k)

	return app


sentence_transformer = SentenceTransformer()
NUM_IMAGES = crud.get_number_of_images(get_db().__next__())

backend = get_backend("./data/img/")
