import gradio as gr
import requests
import base64

def decode_image(base64_image: str) -> str:
	imgdata = base64.b64decode(base64_image)
	filename = 'received_image.png'  # I assume you have a way of picking unique filenames
	with open(filename, 'wb') as f:
		f.write(imgdata)
	return filename, f

def greet(name):
	image_file = get_image()
	return "Hello " + name + "!"

def get_image():
	response = requests.get("http://127.0.0.1:8000/image/json/")
	base64_image = response.json()["base64"]
	image_file, _ = decode_image(base64_image)
	image_description = response.json()["description"]
	return image_file, image_description

def get_frontend():
	with gr.Blocks() as demo:
		with gr.Row():
			with gr.Column():
				img = gr.Image(get_image(), type="filepath", shape=(20,20))
			with gr.Column():
				actual_description = gr.Textbox(label="Actual image description", visible=False)
				description_guess = gr.Textbox(label="Image description guess")
				similarity_score = gr.Textbox(label="Similarity score")
				new_image = gr.Button("Get new image")
				new_image.click(fn=get_image, inputs=None, outputs=[img, actual_description])
				submit = gr.Button("Submit")
				submit.click(fn=greet, inputs=description_guess, outputs=similarity_score)
	demo.launch()
	return demo

frontend = get_frontend()
