from typing import List

from fastapi import (
    FastAPI,
    File,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import (
    process_uploaded_files,
    answer_query,
)

app = FastAPI(
    title="RAG API",
    version="1.0.0",
)

# Allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Model
class PromptRequest(BaseModel):
    query: str


# Upload Endpoint
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    return await process_uploaded_files(files)


# Prompt Endpoint
@app.post("/prompt")
async def prompt(payload: PromptRequest):
    return answer_query(payload.query)


# Health Endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}
