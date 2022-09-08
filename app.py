from fastapi import FastAPI
from fastapi.responses import FileResponse


text = [
	"A dinosaur hunting down an ice cream truck",
	"A high tech solarpunk utopia in the Amazon rainforest"
]
BASE_DIR = "./data/img/"
img_path = [
	"dinosaur_ice_cream.png",
	"rainforest_utopia.png"
]

app = FastAPI()

@app.get("/")
def root() -> str:
	return "App is up and ready to receive requests."

@app.get("/image", response_class=FileResponse)
def get_image() -> str:
	return BASE_DIR + img_path[1]
