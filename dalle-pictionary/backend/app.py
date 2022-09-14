from typing import List
from numpy.random import randint
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends

from .utils import get_db, filter_top_predictions
from .sentence_transformer import SentenceTransformer
from ..db import database, crud, schemas, models

SENTENCE_TRANSFORMER = SentenceTransformer()
NUM_IMAGES = crud.get_number_of_images(get_db().__next__())

"""
FastAPI implementation
"""
app = FastAPI()

@app.get("/")
def root() -> str:
	return "App is up and ready to receive requests."

@app.get("/image/json", response_model=schemas.Image)
def get_image_as_json(db: Session = Depends(get_db)) -> models.Image:
	index = randint(0, NUM_IMAGES) + 1
	return crud.get_image(db, index)

@app.post("/predict", response_model=schemas.Prediction)
def predict_sentence_similarity(query: schemas.SimilarityQuery, db: Session = Depends(get_db)) -> float:
	result = SENTENCE_TRANSFORMER.sentence_similarity(
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

@app.get("/leaderboard", response_model=List[schemas.Prediction])
def get_leaderboard(image_id: int, k: int = 5, db: Session = Depends(get_db)) -> List[models.Prediction]:
	sorted_predictions = crud.get_sorted_predictions_by_image(db, image_id)
	return filter_top_predictions(sorted_predictions, k=k)
