from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Route simple pour vérifier que le Daemon est bien en ligne.
    C'est ce que le client Flutter appellera en premier.
    """
    return {"status": "online", "message": "Le cerveau Ratatoskr est actif."}
