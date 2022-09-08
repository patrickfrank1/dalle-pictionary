import gradio as gr
import requests
import base64
from PIL import Image
from io import BytesIO

def decode_image(base64_image: str) -> str:
	im = Image.open(BytesIO(base64.b64decode(base64_image)))
	return im

def refresh_image():
	response = requests.get("http://127.0.0.1:8000/image/json/").json()
	base64_image = response["base64"]
	image = decode_image(base64_image)
	return response["id"], response["description"], image

def get_similarity(actual_description, description_guess):
	return int(actual_description == description_guess)

def get_frontend():
	with gr.Blocks() as demo:
		with gr.Row():
			with gr.Column():
				__, _, im = refresh_image()
				candidate_image = gr.Image(im ,type="pil", shape=(20,20))
			with gr.Column():
				id = gr.Textbox(label="Id", visible=False)
				actual_description = gr.Textbox(label="Actual description", visible=False)
				description_guess = gr.Textbox(label="Image description guess")
				similarity_score = gr.Number(label="Similarity score")
				new_image = gr.Button("Get new image")
				new_image.click(fn=refresh_image, inputs=None, outputs=[id, actual_description, candidate_image])
				submit = gr.Button("Submit")
				submit.click(fn=get_similarity, inputs=[actual_description, description_guess], outputs=similarity_score)
	demo.launch()
	return demo

frontend = get_frontend()
