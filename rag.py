import os
import uuid
import shutil

import google.generativeai as genai

from fastapi import UploadFile

from config import (
    GEMINI_API_KEY,
    LLM_MODEL_NAME,
    UPLOAD_DIR,
)

from parser import extract_text
from chunking import semantic_chunk
from embeddings import (
    generate_embedding,
    generate_embeddings,
)
from chroma_client import (
    add_documents,
    search_documents,
)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

llm = genai.GenerativeModel(LLM_MODEL_NAME)


# Upload Processing
async def process_uploaded_files(files: list[UploadFile]):

    ids = []
    chunks = []
    metadata = []

    total_chunks = 0

    for file in files:

        # Save uploaded file
        save_path = os.path.join(
            UPLOAD_DIR,
            file.filename,
        )

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read file contents
        with open(save_path, "rb") as f:
            file_bytes = f.read()

        text = extract_text(
            file.filename,
            file_bytes,
        )

        # Semantic chunking
        document_chunks = semantic_chunk(text)

        # Build metadata
        for index, chunk in enumerate(document_chunks):

            ids.append(str(uuid.uuid4()))

            chunks.append(chunk)

            metadata.append(
                {
                    "filename": file.filename,
                    "chunk_number": index + 1,
                }
            )

        total_chunks += len(document_chunks)

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Store in ChromaDB
    add_documents(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata,
    )

    return {
        "status": "success",
        "documents_uploaded": len(files),
        "chunks_created": total_chunks,
    }


# Prompt Processing
def answer_query(query: str):

    # Generate embedding for the query
    query_embedding = generate_embedding(query)

    # Retrieve relevant chunks
    results = search_documents(
        query_embedding=query_embedding,
        top_k=5,
    )

    retrieved_chunks = []

    if results["documents"]:

        retrieved_chunks = results["documents"][0]

    context = "\n\n".join(retrieved_chunks)

    # Prompt sent to Gemini
    prompt = f"""
You are a helpful AI assistant.

Answer the user's question ONLY using the supplied context.

If the answer cannot be found in the context, reply with:

"I don't know based on the uploaded documents."

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.generate_content(prompt)

    return {
        "answer": response.text,
        "context_used": retrieved_chunks,
    }
