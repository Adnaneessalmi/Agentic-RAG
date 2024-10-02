from django.shortcuts import render
from django.http import HttpResponse
import os
import sys

# Correctly configure the RAG directory path
RAG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'RAG')
sys.path.append(RAG_DIR)

# Import the Main class from the RAG system
from Main import Main

# Initialize the RAG system
main_instance = Main()

def overview(request):
    return HttpResponse('This is the overview page of the RAG system.')

def chat(request):
    response = None
    query = None
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            # Get the response from the RAG system
            response = main_instance.get_response_for_query(query)
    
    return render(request, 'RAGapp/chat.html', {'query': query, 'response': response})
