from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .agent import NewsAgent
import os
from dotenv import load_dotenv
load_dotenv()  # For local development

agent = NewsAgent()

def home(request):
    return render(request, 'index.html')

@csrf_exempt  # Temporarily disable CSRF for testing
def chat_api(request):
    if request.method == 'POST':
        try:
            query = request.POST.get('query', '').strip()
            if not query:
                return JsonResponse({'error': 'Query is required'}, status=400)
            
            response = agent.generate_response(query)
            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)