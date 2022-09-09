import unittest
import numpy as np
import torch
from ..sentence_transformer import SentenceTransformer

class TestSentenceTransformer(unittest.TestCase):
	def setUp(self):
		self.sentence_transformer = SentenceTransformer()
		self.sentences = [
			"That is a happy person",
			"That is a very happy person"
		]

	def test_embedding_size(self):
		assert self.sentence_transformer.embed_sentences(self.sentences[0]).shape == torch.Size([1,384])
		assert self.sentence_transformer.embed_sentences(self.sentences).shape == torch.Size([2,384])

	def test_similarity_score(self):
		assert np.allclose(
			self.sentence_transformer.sentence_similarity(*self.sentences).numpy(),
			np.array([0.9429]),
			atol=1e-4
		)
		query = "That is a happy dog"
		assert np.allclose(
			self.sentence_transformer.sentence_similarity(self.sentences[0], query).numpy(),
			np.array([0.695]),
			atol=1e-3
		)
	
if __name__ == '__main__':
	unittest.main()