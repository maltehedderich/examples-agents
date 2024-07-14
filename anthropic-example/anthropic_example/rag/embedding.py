import logging

import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoModel, AutoTokenizer

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    def __init__(self, model_path: str = "Alibaba-NLP/gte-large-en-v1.5", dim: int = 1024):
        self.tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model: AutoModel = AutoModel.from_pretrained(model_path, trust_remote_code=True)
        self.dim: int = dim
        self.max_length: int = 8192

    def generate_embeddings(self, input_texts: list[str], normalize: bool = True) -> Tensor:
        logger.info(f"Generating embeddings for {len(input_texts)} texts")
        batch_dict = self.tokenizer(
            input_texts, max_length=self.max_length, padding=True, truncation=True, return_tensors="pt"
        )

        with torch.no_grad():
            outputs = self.model(**batch_dict)

        embeddings: Tensor = outputs.last_hidden_state[:, 0]

        if normalize:
            embeddings = F.normalize(embeddings, p=2, dim=1)

        return embeddings

    def calculate_similarity_scores(self, embeddings: Tensor) -> list[float]:
        scores: Tensor = embeddings[:1] @ embeddings[1:].T
        return scores.tolist()
