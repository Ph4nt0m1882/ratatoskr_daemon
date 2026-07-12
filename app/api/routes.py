from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.services.orchestrator import orchestrator

router = APIRouter()

## On définit le format exact de la requête attendue par notre API
class ChatRequest(BaseModel):
    provider: str
    model: str
    prompt: str

@router.get("/health")
def health_check() -> dict:
    """
    Check the health status of the API.
    """
    return {"status": "ok", "message": "Ratatoskr Daemon is listening..."}

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streams the response from the AI provider chunk by chunk.
    
    Args:
        request (ChatRequest): The provider, model, and user prompt.
        
    Returns:
        StreamingResponse: A continuous stream of text chunks.
    """
    try:
        ## On récupère notre générateur asynchrone depuis l'orchestrateur
        generator = orchestrator.stream_text(
            provider_name=request.provider,
            model_name=request.model,
            prompt=request.prompt
        )
        
        ## FastAPI gère nativement le "Chunked Transfer Encoding" !
        return StreamingResponse(generator, media_type="text/plain")
        
    except ValueError as e:
        ## Si le fournisseur demandé n'existe pas, on renvoie une erreur 400 proprement
        raise HTTPException(status_code=400, detail=str(e))