import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ... existing code ...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chatbot',  # Add the chatbot app
]

# ... existing code ...

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# ... rest of the settings ... 