from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
import json
import logging
from .services import ChatbotService

logger = logging.getLogger(__name__)

def chat_view(request):
    """Render the chat interface"""
    return render(request, 'chatbot/chat.html')

@method_decorator(csrf_exempt, name='dispatch')
@permission_classes([AllowAny])
class ChatbotView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({
                    'error': 'Message is required'
                }, status=400)
            
            logger.info(f"Processing message: {user_message}")
            chatbot = ChatbotService()
            response = chatbot.process_message(user_message)
            logger.info(f"Got response: {response}")
            
            return JsonResponse({
                'response': response
            })
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request", exc_info=True)
            return JsonResponse({
                'error': 'Invalid JSON'
            }, status=400)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': str(e)
            }, status=500) 