from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Depends
from pydantic import BaseModel
from rag_pipeline import initialize_query_engine, clean_temp_directory
import os
import shutil
import uuid

app = FastAPI()

# Store query engines per session
query_engines = {}

class QueryRequest(BaseModel):
    session_id: str
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    openai_key: str = Form(...),
    session_id: str = Form(...)
):
    
    print(f"Received session_id: {session_id}") #debug check 1

    temp_dir = f"./temp/{session_id}"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Initialize the query engine and store it
        query_engines[session_id] = initialize_query_engine(file_path, openai_key=openai_key, parser_type='semantic')
        
        print(f"Session ID: {session_id}, Query Engines: {query_engines.keys()}") #debug check

        # Clean up uploaded files
        os.remove(file_path)
        return {"message": f"Successfully processed {file.filename}"}
    except Exception as e:
        clean_temp_directory(session_id)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):

    print(f"Received session_id: {request.session_id}") #debug check 3
    print(f"Query Engines: {query_engines.keys()}") #debug check 4

    query_engine = query_engines.get(request.session_id)
    if not query_engine:
        raise HTTPException(status_code=400, detail="No document uploaded yet. Please upload a document first.")
    try:
        response = query_engine.query(request.question)
        return QueryResponse(answer=str(response))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cleanup")
def cleanup_session(session_id: str = Form(...)):
    """Clean up the session data."""
    if session_id in query_engines:
        del query_engines[session_id]
    clean_temp_directory(session_id)
    return {"message": f"Session {session_id} cleaned up."}

@app.get("/")
def home():
    return {"message": "Welcome to the RAG API! Upload a document to start querying."}
