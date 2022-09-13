from typing import List
from sqlalchemy.orm import Session

from . import models, schemas

def get_image(db: Session, image_id: int) -> schemas.Image:
	return db.query(models.Image).filter(models.Image.id == image_id).first()

def get_number_of_images(db: Session) -> int:
	return db.query(models.Image).count()

def get_prediction(db: Session, prediction_id: int) -> schemas.Prediction:
	return db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()

def get_number_of_predictions(db: Session) -> int:
	return db.query(models.Prediction).count()

def get_sorted_predictions_by_image(db: Session, image_id: int) -> List[schemas.Prediction]:
	return (db.query(models.Prediction)
	.filter(models.Prediction.image_id == image_id)
	.order_by(models.Prediction.similarity_score.desc())
	.all())

def get_number_of_predictions_by_image(db: Session, image_id: int) -> int:
	return db.query(models.Prediction).filter(models.Prediction.image_id == image_id).count()

def get_top_predictions_by_image(db: Session, image_id: int, k: int) -> List[schemas.Prediction]:
	return (db.query(models.Prediction)
		.distinct() # only works for postgres
		.filter(models.Prediction.image_id == image_id)
		.order_by(models.Prediction.similarity_score.desc())
		.limit(k)
		.all())

def create_image(db: Session, image: schemas.ImageCreate) -> schemas.Image:
	db_image = models.Image(**image.dict())
	db.add(db_image)
	db.commit()
	db.refresh(db_image)
	return db_image

def create_prediction(db: Session, prediction: schemas.PredictionCreate) -> schemas.Prediction:
	db_prediction = models.Prediction(**prediction.dict())
	db.add(db_prediction)
	db.commit()
	db.refresh(db_prediction)
	return db_prediction
