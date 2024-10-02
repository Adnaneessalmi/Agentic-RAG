import requests
from fpdf import FPDF

class LLMResponder:
    def __init__(self):
        self.ollama_host = ""
        self.context = []

    def update_context(self, query, response):
        """Update the context with a new query and response."""
        self.context.append({"query": query, "response": response})

    def get_context(self):
        """Retrieve the current context as a formatted string."""
        context_string = ""
        for entry in self.context:
            context_string += f"Query: {entry['query']}\nResponse: {entry['response']}\n"
        return context_string

    def generate_response(self, query, retrieved_answer):
        """Generate a response from the LLM using the current context and handle actions based on the returned code."""
        # Get the current context
        context = self.get_context()
        print("Retrieved answer: ", retrieved_answer)

        # Format the prompt with or without the context
        if context:
            prompt = (f"This is a Retrieval-Augmented Generation (RAG) system.\n"
                      f"Context:\n{context}\n"
                      f"New Query: {query}\n"
                      f"Retrieved Answer: {retrieved_answer}\n"
                      f"Generate a proper response to present to the user.\n"
                      f"Your response should start with one of the following numbers:\n"
                      f"0: if you judge that the question isn't related to the retrieved answer\n"
                      f"1: if the user wants the answer to be saved in a PDF\n"
                      f"2: if the user wants the answer to be saved in a text file\n"
                      f"3: no action.")
        else:
            prompt = (f"This is a Retrieval-Augmented Generation (RAG) system.\n"
                      f"New Query: {query}\n"
                      f"Retrieved Answer: {retrieved_answer}\n"
                      f"Generate a proper response to present to the user.\n"
                      f"Your response should start with one of the following numbers:\n"
                      f"0: if you judge that the question isn't related to the retrieved answer\n"
                      f"1: if the user wants the answer to be saved in a PDF\n"
                      f"2: if the user wants the answer to be saved in a text file\n"
                      f"3: no action.")

        # Debugging: Print prompt and size
        print("Sending prompt:", prompt)
        print("Prompt size:", len(prompt))

        # Send a POST request to the LLM
        headers = {'Content-Type': 'application/json', 'Connection': 'close'}
        response = requests.post(
            f"{self.ollama_host}/v1/completions",
            json={"model": "gemma2:2b", "prompt": prompt},
            headers=headers,
            verify=False  # Disabling SSL verification for debugging (remove for production)
        )

        # Check for successful response and handle accordingly
        if response.status_code == 200:
            completion_text = response.json()['choices'][0]['text'].strip()
            # Extract the action code and the actual response
            action_code = completion_text[0]
            actual_response = completion_text[1:].strip()

            # Debugging: Print the action code
            print("Action Code:", action_code)

            # Handle actions based on the action code
            if action_code == '0':
                print("The retrieved information may be out of context. Please refine your query.")
            elif action_code == '1':
                self.save_as_pdf(query, actual_response)
            elif action_code == '2':
                self.save_as_text(query, actual_response)
            elif action_code == '3':
                print("No action required.")

            # Update context with the generated response
            self.update_context(query, actual_response)

            return actual_response
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return f"Error: {response.status_code}, {response.text}"

    def save_as_pdf(self, query, response_text):
        """Save the response as a PDF document."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Query:", ln=True)
        pdf.multi_cell(0, 10, txt=query)
        pdf.cell(200, 10, txt="Response:", ln=True)
        pdf.multi_cell(0, 10, txt=response_text)
        
        pdf_filename = "response.pdf"
        pdf.output(pdf_filename)
        print(f"Response saved as PDF: {pdf_filename}")

    def save_as_text(self, query, response_text):
        """Save the response as a text file."""
        text_filename = "response.txt"
        with open(text_filename, 'w', encoding='utf-8') as file:
            file.write("Query:\n")
            file.write(query + "\n\n")
            file.write("Response:\n")
            file.write(response_text)
        print(f"Response saved as text file: {text_filename}")

    def format_to_html(self, response_text):
        """Format the given response text to HTML style using the LLM."""
        prompt = (f"Format the following text in HTML style for a well-presented response:\n"
                  f"Response: {response_text}\n"
                  f"Make sure the output includes HTML tags like <p>, <b>, <i>, etc., "
                  f"to ensure a visually appealing format.")

        # Debugging: Print prompt and size
        print("Formatting prompt:", prompt)
        print("Prompt size:", len(prompt))

        # Send a POST request to the LLM for formatting
        headers = {'Content-Type': 'application/json', 'Connection': 'close'}
        response = requests.post(
            f"{self.ollama_host}/v1/completions",
            json={"model": "gemma2:2b", "prompt": prompt},
            headers=headers,
            verify=False  # Disabling SSL verification for debugging (remove for production)
        )

        # Check for successful response and return the HTML formatted text
        if response.status_code == 200:
            formatted_html = response.json()['choices'][0]['text'].strip()
            return formatted_html
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return f"Error: {response.status_code}, {response.text}"

