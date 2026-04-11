# Rescue AI (Gemma 4 Hackathon)

This project leverages a modular microservice-inspired architecture.

## Structure
- `frontend/` - React + TypeScript application for the user interface.
- `backend/` - FastAPI backend handling multimodal capabilities (RAG, YOLO, agents) and interacting with Gemma.

## Running Locally

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
