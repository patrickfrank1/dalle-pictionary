
import base64
from pathlib import Path
from typing import Generator, List

from ..db import database, models


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


def filter_top_predictions(sorted_predictions: List[models.Prediction], k=5) -> List[models.Prediction]:
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