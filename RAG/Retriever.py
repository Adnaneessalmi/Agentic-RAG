import torch
from sentence_transformers import util
import numpy as np

class Retriever:
    def __init__(self, pdf_data):
        # Convert the embeddings from the pdf_data to a NumPy array first
        embeddings_np = np.array([chunk['embedding'].cpu().numpy() for chunk in pdf_data])

        # Convert the NumPy array to a tensor and move to GPU
        self.embeddings = torch.tensor(embeddings_np, dtype=torch.float32).to("cuda")

    def search(self, embedded_query, top_k=3):
        print("############## RETRIEVER ####################")
        
        # Calculate dot product scores between the query and document embeddings
        dot_scores = util.dot_score(embedded_query, self.embeddings)[0]

        # Get top-k results
        scores, indices = torch.topk(dot_scores, k=top_k)

        return scores, indices
