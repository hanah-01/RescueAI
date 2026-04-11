# Rescue AI (Gemma 4 Hackathon)

Rescue AI is a modular, microservice-inspired platform for disaster response, combining advanced computer vision, retrieval-augmented generation (RAG), and local LLM reasoning.

## Architecture Overview

- **Frontend**: React + TypeScript chat and image interface.
- **Backend**: FastAPI, modular services for:
	- **YOLOv8n**: Object detection (people, vehicles, etc.)
	- **CLIP (Vision-Language Model)**: Scene classification (e.g., "fire", "flood") with confidence thresholding and CUDA/CPU support
	- **RAG (Retrieval-Augmented Generation)**: Reads and chunks disaster manuals from `data/`, uses `BAAI/bge-small-en-v1.5` embeddings, FAISS vector search, hybrid re-ranking, and metadata tagging
	- **Gemma (Ollama LLM)**: Local LLM for reasoning and response generation
	- **Modular Routing**: All logic orchestrated via FastAPI routers and service classes

## Key Features (as of April 2026)

- **Hybrid Vision Pipeline**: YOLO for objects, CLIP for disaster scene detection ("fire", "flood", etc.)
- **Advanced RAG**:
	- Dynamic chunking with `langchain-text-splitters`
	- Strong open-source embeddings (`BAAI/bge-small-en-v1.5`)
	- FAISS vector search with hybrid scoring (metadata and keyword boosts)
	- Clean, formatted context output for LLM
- **Local LLM Reasoning**: Integrates with Ollama (Gemma 2b) for fast, private, on-device response generation
- **Microservice Structure**: All major logic (vision, RAG, LLM) is modularized under `services/` and `routes/`
- **Easy Extensibility**: Add new disaster types by dropping `.txt` files into `backend/data/`

## Project Structure

- `frontend/` - React + TypeScript application for the user interface
- `backend/` - FastAPI backend for multimodal analysis and LLM reasoning
	- `services/` - Modular service classes (YOLO, CLIP, Gemma, RAG)
	- `routes/` - API endpoints for chat and image analysis
	- `data/` - Disaster manual text files (not committed to git)

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