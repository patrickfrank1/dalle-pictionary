from typing import List
from transformers import AutoTokenizer, AutoModel
import torch as pt
import torch.nn.functional as F

class SentenceTransformer:
	def __init__(self):
		self.hf_model_id = 'sentence-transformers/all-MiniLM-L6-v2'
		self.tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(self.hf_model_id)
		self.model: AutoModel = AutoModel.from_pretrained(self.hf_model_id)
	
	def mean_pooling(self, model_output: pt.Tensor, attention_mask: pt.Tensor):
		token_embeddings = model_output[0]
		input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
		return pt.sum(token_embeddings * input_mask_expanded, 1) / pt.clamp(input_mask_expanded.sum(1), min=1e-9)
	
	def embed_sentences(self, sentences: List[str]) -> pt.Tensor:
		encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
		with pt.no_grad():
			model_output = self.model(**encoded_input)
			sentence_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
			sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
		return sentence_embeddings

	def sentence_similarity(self, source: str, query: str) -> pt.Tensor:
		embeddings = self.embed_sentences([source, query])
		return pt.dot(embeddings[0], embeddings[1])
