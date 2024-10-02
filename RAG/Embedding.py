import torch
from sentence_transformers import SentenceTransformer

class Embedding:
    def __init__(self, pdf_data, save_path="C:\\Users\\pc\\Desktop\\project1\\prj1\\RAG\\embeddings.pt"):
        self.pdf_data = pdf_data
        self.save_path = save_path

        # Determine the device: CUDA if available, otherwise CPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        # Initialize the embedding model with the selected device
        self.embedding_model = SentenceTransformer(model_name_or_path="all-mpnet-base-v2", device=device)

    def generate_embeddings(self):
        print("############## EMBEDDING ####################")

        for i, chunk_data in enumerate(self.pdf_data):
            # Generate embeddings for each chunk of text
            chunks = chunk_data.get('chunks', [])
            chunk_embeddings = self.embedding_model.encode(chunks, convert_to_tensor=True)

            # Store the embeddings in the chunk_data dictionary
            chunk_data['embedding'] = chunk_embeddings

        # Save all embeddings as tensors to the specified save_path
        torch.save(self.pdf_data, self.save_path)
        print(f"Embeddings saved to {self.save_path}")

        # Return the updated pdf_data with embeddings
        return self.pdf_data

    def load_stored(self):
        print("Loading stored embeddings from file...")
        self.pdf_data = torch.load(self.save_path)
        
        return self.pdf_data

    def embed_query(self, query):
        # Generate an embedding for the query
        query_embedding = self.embedding_model.encode(query, convert_to_tensor=True)
        return query_embedding

