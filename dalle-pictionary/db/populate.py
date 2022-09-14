from pathlib import Path
import base64

from . import crud, schemas

IMAGE_PATH = "./data/img/"

def base64_encode_image(path: Path) -> str:
	with open(path, "rb") as image_file:
		encoded_image_string = base64.b64encode(image_file.read())
	return encoded_image_string

def insert_images(db) -> None:
	text = [
		"A dinosaur hunting down an ice cream truck",
		"A high tech solarpunk utopia in the Amazon rainforest"
	]
	img_fname = [
		"dinosaur_ice_cream.png",
		"rainforest_utopia.png"
	]
	
	for i in range(len(text)):
		crud.create_image(db, schemas.ImageCreate(
			description=text[i],
			base64=base64_encode_image(IMAGE_PATH+img_fname[i])
		))
