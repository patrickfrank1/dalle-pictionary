from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root() -> str:
	return "App is up and ready to receive requests."

