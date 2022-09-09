from typing import Tuple
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

class SentenceTransformer:
	def __init__(self):
		self.tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
		self.model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
	
	def mean_pooling(self, model_output, attention_mask):
		token_embeddings = model_output[0]
		input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
		return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
	
	def embed_sentences(self, sentences):
		encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
		with torch.no_grad():
			model_output = self.model(**encoded_input)
			sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
			sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
		return sentence_embeddings

	def sentence_similarity(self, source, query):
		embeddings = self.embed_sentences([source, query])
		return torch.dot(embeddings[0], embeddings[1])
