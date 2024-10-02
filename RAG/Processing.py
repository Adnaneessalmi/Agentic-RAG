import nltk
import random
import re

class Processing:
    def __init__(self, pdf_data):
        # Initialize the Processing class with the provided PDF data.
        self.pdf_data = pdf_data
    def clean_text(self, text):
        # Remove non-printable characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Replace non-ASCII characters with a space
        # Replace backspace characters with an empty string
        text = text.replace('\x08', '')
        # Optionally, you could replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        return text

    def chunking(self, slice_size: int):
        # Chunk the text of each page into sentences and then into smaller chunks, adding them to the page's dictionary.
        print("############## PROCESSING ####################")
        new_pdf_data = []
        for page in self.pdf_data:
            # Tokenize the text into sentences
            cleaned_text = self.clean_text(page["text"])
            sentences = nltk.sent_tokenize(cleaned_text)
            
            # Discard empty sentences
            non_empty_sentences = [s for s in sentences if s.strip()]

            # Split non-empty sentences into chunks of size slice_size
            step = 384
            max_len = 200
            for i in range(0, len(non_empty_sentences), slice_size):
                chunk = " ".join(non_empty_sentences[i:i + slice_size])
               
                num_tokens = len(chunk.split())

                if num_tokens <= max_len:
                    if chunk.strip():  # Ensure the chunk is not empty
                        page_chunk = page.copy()
                        page_chunk["chunks"] = chunk
                        new_pdf_data.append(page_chunk)
                    step = slice_size
                else:
                    seek = True
                    len_count = 0
                    j = 1
                    while seek:
                        buffer = " ".join(non_empty_sentences[i:i + j])
                        
                        len_count = len(buffer.split())
                        
                        if len_count < max_len:
                            j += 1
                        else:
                            step = j
                            chunk = " ".join(non_empty_sentences[i:i + j-1])
                            if chunk.strip():  # Ensure the chunk is not empty
                                page_chunk = page.copy()
                                page_chunk["chunks"] = chunk
                                new_pdf_data.append(page_chunk)
                            seek = False
                            if j > 10:
                                print("infinite loop")
                
        self.pdf_data = new_pdf_data

        return self.pdf_data

    def display_random_sample(self, sample_size=5):
        # Display a random sample of the processed PDF data.
        random_sample = random.sample(self.pdf_data, min(sample_size, len(self.pdf_data)))
        for sample in random_sample:
            print(sample)
            print("############")
            print()
