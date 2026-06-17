# NPCIL Guide

A comprehensive web application providing information about the Nuclear Power Corporation of India Limited (NPCIL), including real-time recruitment updates, career guidance, and an AI-powered assistant.

## 🌟 Features

- **Educational Content**: Complete guide about NPCIL's history, plant sites, technology, and role in India's energy sector
- **Real-time Job Updates**: Live recruitment notifications fetched directly from [npcilcareers.co.in](https://npcilcareers.co.in)
- **AI Career Assistant**: Chat interface powered by Google Gemini AI to answer questions about NPCIL careers
- **Interactive UI**: Modern, responsive design with particle animations and smooth navigation
- **Exam Guidance**: Detailed information about GATE, written tests, and selection processes

## 📁 Project Structure

```
npcil-guide/
├── backend/
│   ├── main.py          # FastAPI backend with job scraping and AI chat
│   └── __pycache__/
├── frontend/
│   ├── index.html       # Main HTML page with NPCIL guide content
│   ├── script.js        # JavaScript for interactivity and API calls
│   └── style.css        # Styling and animations
└── README.md
```

## 🚀 Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **BeautifulSoup4**: Web scraping for job listings
- **Google Gemini AI**: AI-powered chat assistant
- **Requests**: HTTP library for web scraping

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript (Vanilla)**: Client-side logic and API integration

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- pip package manager
- Google Gemini API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install required dependencies:
```bash
pip install fastapi uvicorn beautifulsoup4 requests google-generativeai python-dotenv pydantic
```

3. Create a `.env` file in the backend directory:
```
API_KEY=your_google_gemini_api_key_here
```

4. Run the FastAPI server:
```bash
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Start a simple HTTP server (Python):
```bash
python -m http.server 5500
```

Or use any other static file server of your choice.

3. Open your browser and navigate to:
```
http://localhost:5500
```

## 📡 API Endpoints

### GET `/jobs`
Returns all job listings scraped from NPCIL careers portal with status (Open/Closed).

**Response:**
```json
[
  {
    "title": "Job Title",
    "start_date": "DD/MM/YYYY",
    "last_date": "DD/MM/YYYY",
    "status": "Open/Closed",
    "link": "https://npcilcareers.co.in/..."
  }
]
```

### GET `/open-jobs`
Returns only currently open job listings.

### GET `/closed-jobs`
Returns only closed job listings.

### POST `/chat`
AI-powered chat endpoint for NPCIL career queries.

**Request:**
```json
{
  "message": "What are the current open positions?"
}
```

**Response:**
```json
{
  "response": "AI-generated response based on current job data"
}
```

## 🎯 Key Sections in the Guide

### 1. About NPCIL
- Government enterprise under Department of Atomic Energy
- Headquarters in Mumbai, Maharashtra
- Mission and technology overview
- Role in India's energy sector

### 2. History Timeline
- From 1948 (Atomic Energy Commission) to present
- Key milestones in India's nuclear program
- NPCIL's establishment in 1987

### 3. Plant Sites
- 7 nuclear power stations across 6 states
- Detailed information about each site:
  - RAPS (Rawatbhata, Rajasthan)
  - TAPS (Tarapur, Maharashtra)
  - MAPS (Kalpakkam, Tamil Nadu)
  - NAPS (Narora, Uttar Pradesh)
  - Kaiga (Karnataka)
  - Kakrapar (Gujarat)
  - KKNPP (Kudankulam, Tamil Nadu)

### 4. Careers
- Real-time job updates
- Different recruitment pathways
- Salary and benefits information

### 5. Exams & Selection
- GATE pathway for Executive Trainees
- Written test for Trainees and Assistants
- Medical standards
- Age relaxation rules

### 6. How to Apply
- Step-by-step application guide
- Document requirements
- Fee structure
- Training process

## 🔗 Useful Links

- [NPCIL Official Website](https://www.npcil.nic.in)
- [NPCIL Careers Portal](https://www.npcilcareers.co.in)
- [GATE Official](https://gate2025.iitr.ac.in)
- [Atomic Energy Regulatory Board](https://www.aerb.gov.in)

## 📝 Notes

- Job data is scraped in real-time from the official NPCIL careers portal
- The AI assistant only answers based on provided recruitment data
- Status of jobs (Open/Closed) is determined based on the last date
- This is an educational project and not affiliated with NPCIL

## 🤝 Contributing

This is an open-source educational project. Feel free to submit issues and pull requests.

## 📄 License

This project is for educational purposes. Please refer to NPCIL's official channels for authoritative information.(AQ.Ab8RN6L5avWoPy78BMkB7tRMt2vsoZBw2eGJr03XHfMPXqg9DQ)
