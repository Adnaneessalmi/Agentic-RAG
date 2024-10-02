from Documents import Documents
from Processing import Processing
from Embedding import Embedding
from Retriever import Retriever
from LLM import LLMResponder


class Main:
    def __init__(self):
        # Initialize the Documents class
        self.documents_instance = Documents()

        # Check if the PDFs have changed
        if self.documents_instance.detect_change():
            # Load and process the PDF data
            self.pdf_data = self.load_and_process_pdfs()
            
            # Generate embeddings for the processed data
            self.embedding_instance = Embedding(self.pdf_data)
            print(self.pdf_data[0].keys())
            self.pdf_data = self.embedding_instance.generate_embeddings()
        else:
            # Load the stored embeddings
            self.embedding_instance = Embedding(None)  # No need to pass pdf_data here
            self.pdf_data = self.embedding_instance.load_stored()

        # Initialize the LLM responder
        self.responder = LLMResponder()

    def load_and_process_pdfs(self):
        # Load the PDF data
        pdf_data = self.documents_instance.load_magic()

        # Process the data (e.g., chunking sentences)
        processor = Processing(pdf_data)
        processed_pdf_data = processor.chunking(slice_size=7)  # Adjust slice_size as needed

        return processed_pdf_data

    def perform_search(self, query):
        # Instantiate the Retriever class
        retriever = Retriever(self.pdf_data)

        # Generate an embedding for the query
        query_embedding = self.embedding_instance.embed_query(query)

        # Perform the search and return the results
        return retriever.search(query_embedding, top_k=1)

    def get_response_for_query(self, query):
        # Perform the search
        search_result = self.perform_search(query)
        
        # Retrieve the relevant chunk
        retrieved_chunk = self.pdf_data[search_result[1][0]]["chunks"]
        
        # Generate a response using the LLM
        final_answer = self.responder.generate_response(query, retrieved_chunk)
        
        return final_answer
