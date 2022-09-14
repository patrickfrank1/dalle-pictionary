import base64
import requests
from typing import Tuple
from io import BytesIO

from PIL import Image
import pandas as pd

IP_ADDRESS = "http://127.0.0.1"
PORT = 8000
URL = f"{IP_ADDRESS}:{PORT}"

def decode_base64_to_image(base64_image: str) -> Image.Image:
	im = Image.open(BytesIO(base64.b64decode(base64_image)))
	return im

def get_image() -> Tuple[str, str, Image.Image]:
	response = requests.get(f"{URL}/image/json").json()
	base64_image = response["base64"]
	image = decode_base64_to_image(base64_image)
	return response["id"], response["description"], image

def get_leaderboard(image_id: int, k: int = 10) -> pd.DataFrame:
	data = requests.get(f"{URL}/leaderboard?image_id={image_id}&k={k}").json()
	df = pd.DataFrame.from_records(data, columns=["leaderboard_name", "similarity_score"])
	placeholder_df = pd.DataFrame({"leaderboard_name": k*["John Dough"], "similarity_score": [0.0 for _ in range(k)]})
	df = pd.concat([df,placeholder_df])
	df["similarity_score"] = df["similarity_score"].astype(float, copy=False).round(4)
	return df

def calculate_similarity_score(image_id, actual_description, guess_description, leaderboard_name="John Dough"):
	response = requests.post(
		f"{URL}/predict",
		json={
			"image_id": image_id,
			"leaderboard_name": leaderboard_name,
			"actual_description": actual_description,
			"guess_description": guess_description
		}
	).json()
	return response["similarity_score"]
