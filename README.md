# Research Summarizer API

The **Research Summarizer API** allows users to find, analyze, and summarize research papers from various sources. It supports uploading PDFs, fetching papers by DOI or URL, and converting summaries into podcast-style audio.

---

## Table of Contents
- [Overview](#overview)
- [Core Features](#core-features)
- [Installation](#installation)
- [Tech Stack](#tech-stack)
- [API Endpoints](#api-endpoints)
- [Sample Requests & Responses](#sample-requests--responses)
- [System Architecture](#system-architecture)
- [Multi-Agent Design](#multi-agent-design)
- [Paper Processing Methodology](#paper-processing-methodology)
- [Audio Generation](#audio-generation)
- [Limitations & Future Improvements](#limitations--future-improvements)
- [Postman Collection](#postman-collection)
- [Environment Variables](#environment-variables)
- [Sample Input & Output](#sample-input--output)

---

## Overview

The Research Summarizer API enables users to:
- Search for academic papers by topic
- Process research documents via URL, file upload, or DOI
- Classify papers by topic using NLP
- Generate readable summaries from long papers
- Convert summaries into podcast-like audio using gTTS

---

## Core Features

✔️ Paper discovery via arXiv API  
✔️ Upload and extract from PDFs  
✔️ Process papers from DOIs and academic repository URLs  
✔️ NLP-based topic classification and summarization  
✔️ Generate podcast-style audio output  
✔️ Store and retrieve paper data from a PostgreSQL database  
✔️ Fully Dockerized for easy setup and deployment  

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/your-username/research-summarizer-api.git
cd research-summarizer-api
```

### Run the Project with Docker
```bash
docker-compose up --build
```

The API will be available at:
```
http://localhost:8000/
```

Example: `http://localhost:8000/api/process-url/`

---

## Tech Stack

- **Backend Framework**: Django + Django REST Framework
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL
- **NLP Models**: Hugging Face Transformers (`facebook/bart-large-cnn`, `zero-shot-classification`)
- **Audio Generation**: gTTS (Google Text-to-Speech)
- **PDF Parsing**: PyMuPDF (fitz)
- **Scraping Academic Pages**: BeautifulSoup
- **Search Source**: arXiv (via RSS feed)

---

## API Endpoints

| Method | Endpoint                        | Description                                     |
|--------|----------------------------------|-------------------------------------------------|
| GET    | `/search/?topic=AI`             | Search and classify papers by topic             |
| POST   | `/process-url/`                 | Process PDF from a direct URL                   |
| POST   | `/process-doi/`                 | Process paper via DOI                           |
| POST   | `/process-academic-url/`        | Process landing page from an academic site      |
| POST   | `/upload/`                      | Upload and process a local PDF file             |
| GET    | `/papers/`                      | List all saved research papers                  |
| GET    | `/papers/<id>/`                 | Get details of a specific paper                 |
| GET    | `/synthesize/?topic=AI`         | Cross-paper summary by topic                    |

---

## Sample Requests & Responses

### Register Paper by URL
```json
POST /process-url/
{
  "url": "https://arxiv.org/pdf/1706.03762.pdf"
}
```

### Register Paper by DOI
```json
POST /process-doi/
{
  "doi": "10.48550/arXiv.1706.03762"
}
```

### Process Academic Page
```json
POST /process-academic-url/
{
  "url": "https://www.nature.com/articles/s41586-020-2649-2"
}
```

### Upload PDF (form-data)
Key: `file`, Value: Select PDF file

### Get All Papers
```http
GET /papers/
```

### Get Single Paper
```http
GET /papers/1/
```

### Synthesize Summaries by Topic
```http
GET /synthesize/?topic=Quantum Computing
```

---

## System Architecture
<p align="center">
  <img src="https://i.imghippo.com/files/ka9143A.jpeg" alt="Architecture" width="500"/>
</p>



## Multi-Agent Design

| Agent Name             | Responsibility                                  |
|------------------------|--------------------------------------------------|
| `PaperSearchAgent`     | Searches papers from arXiv by topic             |
| `ExtractionAgent`      | Extracts text from PDF, URL, DOI                |
| `TopicClassificationAgent` | Classifies text using zero-shot classification |
| `SummaryAgent`         | Summarizes long text using transformer models   |
| `AudioAgent`           | Converts summary into podcast-style audio       |

Agents communicate in a pipeline to process and enrich research content.

---

## Paper Processing Methodology

1. **Input**: URL, PDF, DOI, or academic repository
2. **Text Extraction**: From file or remote link using PyMuPDF or BeautifulSoup
3. **Classification**: Using Hugging Face's zero-shot classification pipeline
4. **Summarization**: Using Facebook's `bart-large-cnn` model
5. **Storage**: Title, summary, topic, source, and audio path saved in DB

---

## Audio Generation

- Uses `gTTS` (Google Text-to-Speech) to convert summaries into `.mp3`
- Includes podcast-style intros and outros for better engagement
- Files are saved and served from `/media/audios/`

---

## Limitations & Future Improvements

### Limitations:
- Currently supports only English summaries via gTTS
- Only English supported via gTTS
- Basic citation capture (only arXiv and links)

### Future Enhancements:
- Add support for multilingual summarization
- Integrate speaker voice cloning (e.g., ElevenLabs)
- Add task queues (Celery) for async processing
- Build UI dashboard to explore topics and listen to audio

---

## Postman Collection

Import this collection to test endpoints quickly:  
🔗 [Postman Collection](https://documenter.getpostman.com/view/your_collection_id)

---

## Environment Variables

Create a `.env` file:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=your_host
DB_PORT=5432
```

---

## Sample Input & Output

### API: `/process-url/`
**Input:**
```json
{
  "url": "https://arxiv.org/pdf/1706.03762.pdf"
}
```
**Output:**
```json
{
  "id": 1,
  "title": "Attention Is All You Need",
  "topic": "Artificial Intelligence",
  "summary": "This paper proposes the Transformer model...",
  "source_url": "https://arxiv.org/pdf/1706.03762.pdf",
  "audio": "audios/abcd1234.mp3"
}
```

### API: `/process-doi/`
**Input:**
```json
{
  "doi": "10.48550/arXiv.1706.03762"
}
```
**Output:**
```json
{
  "id": 2,
  "title": "10.48550/arXiv.1706.03762",
  "topic": "Artificial Intelligence",
  "summary": "This paper introduces a novel architecture...",
  "doi": "10.48550/arXiv.1706.03762",
  "audio": "audios/xyz5678.mp3"
}
```

### API: `/synthesize/?topic=Quantum Computing`
**Output:**
```json
{
  "topic": "Quantum Computing",
  "synthesized_summary": "Across various papers, the key advancements in quantum computing..."
}
```

**Sample Input:**
```json
{
  "url": "https://arxiv.org/pdf/1706.03762.pdf"
}
```

**Sample Output:**
```json
{
  "id": 1,
  "title": "Attention Is All You Need",
  "topic": "Artificial Intelligence",
  "summary": "This paper proposes the Transformer model...",
  "source_url": "https://arxiv.org/pdf/1706.03762.pdf",
  "audio": "audios/abcd1234.mp3"
}
```

---

## Author

Made with ❤️ by Pankaj Jaiswal

