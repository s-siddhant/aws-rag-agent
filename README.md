# Retrieval-Augmented Generation (RAG) Document Q&A System

## Overview
This repository contains a full-stack application that allows users to upload documents and interact with them using a Retrieval-Augmented Generation (RAG) approach. The system processes PDF documents and enables querying via a natural language interface. It is built using FastAPI for the backend and Streamlit for the frontend.

## Features
- Upload PDF documents for processing.
- Query documents using natural language. 
- Session-based interaction to maintain context.
- Dynamic cleanup of sessions and associated temporary files.

## Deployment
This application is deployed on AWS EC2 at: http://35.182.40.143:8501

## Architecture
- Frontend: A Streamlit-based UI for file upload and query interaction.
- Backend: A FastAPI-based server that handles document processing and query requests.
- Document Processing: Utilizes LlamaIndex with OpenAI models (e.g., GPT-3.5-turbo) for summarization and vector-based querying.

## Project Structure
```
.
├── app.py                # FastAPI backend application
├── frontend.py           # Streamlit frontend application
├── rag_pipeline.py       # Document processing and query engine initialization
├── Dockerfile            # Dockerfile for backend container
├── docker-compose.yaml   # Docker Compose setup for frontend and backend
├── requirements.txt      # Python dependencies
└── temp/                 # Temporary directory for session-specific files
```

## Requirements
- Python 3.12+
- Docker & Docker Compose
- OpenAI API Key

## Setup Instructions

1. Clone the Repository

```bash
git clone https://github.com/s-siddhant/aws-rag-agent.git
cd aws-rag-agent
```

2. Install Dependencies
If running locally:
```bash
pip install -r requirements.txt
```

3. Run Using Docker Compose
```bash
docker-compose up --build
```

4. Access the Application
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000

## API Endpoints
### **/upload**
- Method: **POST**
- Description: Upload a PDF document for processing.
- Parameters:
  - file (File): The PDF document to upload.
  - openai_key (str): OpenAI API Key.
  - session_id (str): Unique session identifier.

### **/ask**
- Method: **POST**
- Description: Query the uploaded document.
- Body:
```bash
{
  "session_id": "<session_id>",
  "question": "<your_question>"
}
```
- Response:
```bash
{
  "answer": "<response_from_model>"
}
```

### **/cleanup**
- Method: **POST**
- Description: Clean up session data and temporary files.
- Parameters:
  - session_id (str): Unique session identifier.

## Environment Variables
- OPENAI_API_KEY: Required to use OpenAI models.

## Deployment
### AWS EC2 Deployment
The application is deployed on an AWS EC2 instance. Access it at: http://35.182.40.143:8501

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.




