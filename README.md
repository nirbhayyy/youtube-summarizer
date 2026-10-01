\# YouTube AI Summarizer



An AI-powered YouTube video summarization web application built with Django. 

The application extracts transcripts from YouTube videos and uses generative AI 

to generate concise summaries in multiple languages.



\## Features



\- 🎥 YouTube video transcript extraction

\- 🤖 AI-powered video summarization

\- 🌐 English and Hindi summaries

\- 📊 Summary information and video metadata

\- 🔐 User registration and authentication

\- 👤 User dashboard

\- 💾 Summary history

\- 📱 Responsive web interface

\- 🔌 REST API architecture



\## Tech Stack



\### Backend

\- Python

\- Django

\- Django REST Framework



\### AI / NLP

\- Google Gemini API

\- Groq API

\- NLTK



\### YouTube

\- YouTube Transcript API

\- YouTube Data API



\### Database

\- SQLite (local development)



\### Frontend

\- HTML

\- CSS

\- JavaScript



\## Project Architecture



```text

User

&#x20; │

&#x20; ▼

Django Web Application

&#x20; │

&#x20; ├── Authentication

&#x20; │

&#x20; ├── YouTube Service

&#x20; │       │

&#x20; │       ▼

&#x20; │   YouTube Transcript API

&#x20; │

&#x20; ├── AI Summarization

&#x20; │       │

&#x20; │       ├── Google Gemini

&#x20; │       └── Groq

&#x20; │

&#x20; └── Database

&#x20;         │

&#x20;         ▼

&#x20;     Summary History

youtubeMain/
│
├── manage.py
│
├── summerier/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── prompts.py
│   ├── sentiment.py
│   ├── serializers.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   └── youtube_service.py
│
└── youtubeMain/
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py