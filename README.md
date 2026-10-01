# 🎥 YouTube AI Summarizer

> **AI-powered YouTube video summarization using Django REST Framework and Generative AI.**

YouTube AI Summarizer is a web application that extracts transcripts from YouTube videos and uses Generative AI to generate concise, easy-to-read summaries.

The application supports **English and Hindi summaries**, user authentication, summary history, PDF export, and a REST API.

---

## ✨ Features

- 🎥 **YouTube Transcript Extraction**
  - Extract transcripts directly from YouTube videos.
  - Supports videos with available captions/transcripts.

- 🤖 **AI-Powered Summarization**
  - Uses Generative AI to convert long transcripts into concise summaries.
  - Supports multiple AI providers such as **Google Gemini** and **Groq**.

- 🌐 **Multi-Language Summaries**
  - Generate summaries in:
    - 🇬🇧 English
    - 🇮🇳 Hindi

- 📺 **YouTube Video Information**
  - Fetch basic information about YouTube videos using the YouTube Data API.

- 👤 **User Authentication**
  - User registration
  - Login/logout
  - Authenticated user sessions

- 📊 **User Dashboard**
  - View saved summaries
  - Access summary history
  - Manage previously generated summaries

- 📝 **Summary History**
  - Save generated summaries.
  - View previously generated summaries.

- 🗑️ **Delete Summaries**
  - Remove unwanted summaries from history.

- 📄 **PDF Export**
  - Export generated summaries as PDF files.

- 🔌 **Django REST API**
  - RESTful backend architecture for handling application functionality.

---

## 🧠 How It Works

```text
                YouTube URL
                     │
                     ▼
             Extract Video ID
                     │
                     ▼
          Fetch YouTube Transcript
                     │
                     ▼
              Text Processing
                     │
                     ▼
             Generative AI Model
                     │
                     ▼
              Generate Summary
                     │
              ┌──────┴──────┐
              ▼             ▼
          Display         Save
          Summary        Summary
                            │
                            ▼
                       PDF Export
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Backend | Python, Django |
| API | Django REST Framework |
| AI / LLM | Google Gemini, Groq |
| NLP | NLTK |
| YouTube | YouTube Transcript API, YouTube Data API |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite |
| PDF Generation | ReportLab |
| Environment Management | Python `venv`, `.env` |

---

## 📂 Project Structure

```text
youtube-summarizer/
│
├── youtubeMain/
│   │
│   ├── manage.py
│   │
│   ├── summerier/
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── prompts.py
│   │   ├── serializers.py
│   │   ├── sentiment.py
│   │   ├── urls.py
│   │   ├── utils.py
│   │   ├── views.py
│   │   └── youtube_service.py
│   │
│   └── youtubeMain/
│       ├── settings.py
│       ├── urls.py
│       ├── asgi.py
│       └── wsgi.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/nirbhayyy/youtube-summarizer.git
```

Navigate into the project:

```bash
cd youtube-summarizer
```

> Replace the repository URL with your actual GitHub repository URL if the repository name is different.

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

You can use `.env.example` as a reference.

Example:

```env
API_KEY2=your-gemini-api-key
```

If your application uses additional services, add their API keys to the `.env` file as required.

### ⚠️ Important

**Never commit your `.env` file or API keys to GitHub.**

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
db.sqlite3
```

---

## ▶️ Run the Application

Navigate to the Django project:

```bash
cd youtubeMain
```

Apply database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

---

## 🔌 API

The backend is built using **Django REST Framework**, allowing the summarization functionality to be accessed through API endpoints.

The API handles operations such as:

```text
YouTube URL
     ↓
API Request
     ↓
Transcript Extraction
     ↓
AI Processing
     ↓
Generated Summary
     ↓
API Response
```

API endpoints may include functionality for:

- Video summarization
- Transcript processing
- Video information
- User authentication
- Summary history
- Summary deletion
- PDF generation

---

## 📸 Screenshots

### 🏠 Home Page

_Add application screenshot here._

```text
screenshots/home.png
```

### 📊 Dashboard

_Add dashboard screenshot here._

```text
screenshots/dashboard.png
```

### 📝 Generated Summary

_Add summary page screenshot here._

```text
screenshots/summary.png
```

### 📄 PDF Export

_Add PDF export screenshot here._

```text
screenshots/pdf.png
```

> Recommended: create a `screenshots/` folder in the repository and place your application screenshots inside it.

---

## 🎯 Example Workflow

A typical user workflow looks like this:

```text
1. User opens the application
              ↓
2. User enters a YouTube URL
              ↓
3. Application extracts the video ID
              ↓
4. Transcript is retrieved
              ↓
5. Transcript is processed
              ↓
6. Generative AI creates the summary
              ↓
7. User selects English / Hindi
              ↓
8. Summary is displayed
              ↓
9. User can save the summary
              ↓
10. Summary can be exported as PDF
```

---

## 🧩 Key Components

### `youtube_service.py`

Handles YouTube-related operations such as:

- Extracting video information
- Working with YouTube APIs
- Retrieving transcript data

### `prompts.py`

Contains prompts used to guide the Generative AI model during summarization.

### `utils.py`

Contains reusable helper functions used throughout the application.

### `models.py`

Defines database models used for storing application data and summary history.

### `serializers.py`

Handles serialization and validation of API data using Django REST Framework.

### `views.py`

Contains application and API views responsible for processing user requests.

---

## 🔐 Security

The project follows basic security practices:

- API keys are stored in environment variables.
- `.env` is excluded from Git.
- Django authentication is used for user accounts.
- Sensitive credentials are not stored directly in source code.

For production deployment, additional security configuration should be applied.

---

## 🚀 Future Improvements

Planned improvements include:

- 🌍 Support for additional languages
- 🎬 Better handling of long YouTube videos
- 📄 Downloadable TXT/Markdown summaries
- 🤖 Support for additional LLM providers
- 🧪 Automated unit and API testing
- 🗄️ Production database support such as PostgreSQL
- ⚡ Background processing for long-running summaries
- 📈 Improved dashboard analytics
- 🔐 Enhanced authentication and security
- ☁️ Production deployment and cloud storage

---

## 🐛 Known Limitations

- Videos must have an accessible transcript/caption track.
- Very long transcripts may require additional processing or chunking.
- AI-generated summaries may occasionally contain inaccuracies.
- API availability and usage limits depend on the configured AI/YouTube services.

---

## 📚 Learning Outcomes

This project helped me gain practical experience with:

- Python backend development
- Django and Django REST Framework
- REST API development
- Generative AI integration
- Prompt engineering
- NLP and text processing
- YouTube API integration
- Authentication and database management
- PDF generation
- Environment variable management
- Building an end-to-end AI-powered web application

---

## 👨‍💻 Author

### Nirbhay Meher

**MCA | AI/ML Enthusiast | Python | Django | Machine Learning**

Interested in building practical applications using **Artificial Intelligence, Machine Learning, NLP, and Python**.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational and portfolio purposes.