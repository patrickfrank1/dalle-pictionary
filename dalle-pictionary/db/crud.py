from sqlalchemy.orm import Session

from . import models, schemas

def get_image(db: Session, image_id: int) -> models.Image:
	return db.query(models.Image).filter(models.Image.id == image_id).first()

def get_number_of_images(db: Session) -> int:
	return db.query(models.Image).count()

def get_prediction(db: Session, prediction_id: int):
	return db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()


def get_predictions_by_image(db: Session, image_id: int):
	return db.query(models.Prediction).filter(models.Prediction.image_id == image_id).all()


def create_image(db: Session, image: schemas.ImageCreate):
	db_image = models.Image(**image.dict())
	db.add(db_image)
	db.commit()
	db.refresh(db_image)
	return db_image


def create_prediction(db: Session, prediction: schemas.PredictionCreate):
	db_prediction = models.Prediction(**prediction.dict())
	db.add(db_prediction)
	db.commit()
	db.refresh(db_prediction)
	return db_prediction