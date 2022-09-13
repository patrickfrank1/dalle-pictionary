from pydoc import resolve
import gradio as gr
import requests
import base64
from PIL import Image
from io import BytesIO
import pandas as pd

def decode_image(base64_image: str) -> str:
	im = Image.open(BytesIO(base64.b64decode(base64_image)))
	return im

def refresh_image():
	response = requests.get("http://127.0.0.1:8000/image/json/").json()
	image_id = response["id"]
	base64_image = response["base64"]
	image = decode_image(base64_image)
	leaderboard = get_leaderboard(image_id, k=10)
	return image_id, response["description"], image, None, None, None, leaderboard

def get_similarity(image_id, actual_description, guess_description, leaderboard_name="John Dough"):
	response = requests.post(
		"http://127.0.0.1:8000/predict",
		json={
			"image_id": image_id,
			"leaderboard_name": leaderboard_name,
			"actual_description": actual_description,
			"guess_description": guess_description
		}
	).json()
	leaderboard = get_leaderboard(image_id, k=10)
	return response["similarity_score"], leaderboard

def get_leaderboard(image_id: int, k: int = 10) -> pd.DataFrame:
	data = requests.get(f"http://127.0.0.1:8000/leaderboard?image_id={image_id}&k={k}").json()
	df = pd.DataFrame.from_records(data, columns=["leaderboard_name", "similarity_score"])
	placeholder_df = pd.DataFrame({"leaderboard_name": k*["John Dough"], "similarity_score": k*[0.0]})
	df = pd.concat([df,placeholder_df])
	df["similarity_score"] = df["similarity_score"].round(4)
	return df

def get_frontend():
	initial_id, initial_description, initial_image, _, _, _, initial_leaderboard = refresh_image()
	with gr.Blocks() as demo:
		with gr.Row():
			introduction = gr.Markdown("""
				# Reverse pictionary

				An AI generated picture is presented to you on the left hand 
				side. Your task is to guess, which query was used to generate that 
				image. Your submission will be scored against the true image and
				the query similarity, as measured by another AI model is returned.

				The pictures were generated by either DALL-E or by the Stable 
				Diffusion model. The text similarity is measured a sentence 
				transformer model from the Huggingface hub "sentence-transformers/all-MiniLM-L6-v2"
			""")
		with gr.Row():
			with gr.Column(scale=1):
				candidate_image = gr.Image(initial_image ,type="pil", shape=(20,20))
			with gr.Column(scale=1):
				leaderboard = gr.Dataframe(value=initial_leaderboard, row_count=(10,'fixed'), max_rows=10)
			with gr.Column(scale=1):
				id = gr.Textbox(value=initial_id, label="Id", visible=False)
				actual_description = gr.Textbox(value=initial_description, label="Actual description", visible=False)
				leaderboard_name = gr.Textbox(label="Name on Leaderboard", placeholder="John Dough")
				description_guess = gr.Textbox(label="Image description guess", lines=2)
				similarity_score = gr.Number(label="Similarity score")
				submit = gr.Button("Submit")
				submit.click(fn=get_similarity, inputs=[id, actual_description, description_guess, leaderboard_name], outputs=[similarity_score, leaderboard])
				new_image = gr.Button("Get new image")
				new_image.click(fn=refresh_image, inputs=None, outputs=[id, actual_description, candidate_image, description_guess, leaderboard_name, similarity_score, leaderboard])
	demo.launch()
	return demo

frontend = get_frontend()
