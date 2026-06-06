import os
import threading
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import rag_service
from eval_service import run_evaluation, get_latest_eval_results

app = FastAPI(title="Galactic Archive RAG API", version="1.0.0")

# Enable CORS for React frontend (default Vite dev port is 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global lock/status for evaluation background job
eval_status = {
    "is_running": False,
    "last_run": None
}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: Optional[List[ChatMessage]] = None

@app.on_event("startup")
async def startup_event():
    # Load and index documents in a background thread to speed up startup
    print("Startup: Initializing document index...")
    threading.Thread(target=rag_service.load_and_index_documents, kwargs={"force_rebuild": False}).start()

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    try:
        # Convert history back to dict format
        history_list = []
        if request.history:
            history_list = [{"role": msg.role, "content": msg.content} for msg in request.history]
        
        response = rag_service.generate_rag_answer(request.query, history=history_list)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents")
def get_documents():
    """
    Returns lists of all distinct documents in the archive
    """
    if not os.path.exists(rag_service.DOCS_DIR):
        return []
    
    unique_docs = {}
    for chunk in rag_service.chunks_db:
        doc_id = chunk["doc_id"]
        if doc_id not in unique_docs:
            unique_docs[doc_id] = {
                "id": doc_id,
                "title": chunk["title"],
                "category": chunk["category"],
                "classification": chunk["classification"],
                "chunks_count": 0
            }
        unique_docs[doc_id]["chunks_count"] += 1
        
    return list(unique_docs.values())

@app.get("/api/documents/{doc_id}")
def get_document_by_id(doc_id: str):
    """
    Reads the full raw markdown content of a document
    """
    filepath = os.path.join(rag_service.DOCS_DIR, f"{doc_id}.md")
    if not os.path.exists(filepath):
         # Try with extension just in case doc_id was stored with it
         filepath = os.path.join(rag_service.DOCS_DIR, doc_id)
         if not os.path.exists(filepath):
             raise HTTPException(status_code=404, detail="Document not found")
             
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return {"id": doc_id, "raw_content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rebuild-index")
def rebuild_index(background_tasks: BackgroundTasks):
    """
    Triggers re-indexing of documents
    """
    try:
        background_tasks.add_task(rag_service.load_and_index_documents, force_rebuild=True)
        return {"status": "Reindexing started in background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Evaluation Endpoints ---
def run_evaluation_task():
    global eval_status
    eval_status["is_running"] = True
    try:
        summary = run_evaluation()
        eval_status["last_run"] = summary
    except Exception as e:
        print(f"Error in background evaluation: {e}")
    finally:
        eval_status["is_running"] = False

@app.post("/api/evaluate")
def trigger_evaluation(background_tasks: BackgroundTasks):
    global eval_status
    if eval_status["is_running"]:
        return {"status": "Evaluation is already running", "is_running": True}
        
    background_tasks.add_task(run_evaluation_task)
    return {"status": "Evaluation scheduled", "is_running": True}

@app.get("/api/evaluation-status")
def get_evaluation_status():
    global eval_status
    latest_results = get_latest_eval_results()
    return {
        "is_running": eval_status["is_running"],
        "latest_results": latest_results or eval_status["last_run"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
