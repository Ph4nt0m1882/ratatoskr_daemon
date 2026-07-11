from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime, timezone

class Provider(SQLModel, table=True):
    """
    Represents an AI provider (e.g., Google AI Studio, Anthropic, Local vLLM).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True) # e.g., "google", "anthropic", "local"
    display_name: str # e.g., "Google Gemini"
    base_url: Optional[str] = None
    api_key: Optional[str] = None # In a real prod app, encrypt this!
    is_active: bool = Field(default=True)

class ChatSession(SQLModel, table=True):
    """
    Represents a single conversation thread.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default="New Conversation")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatMessage(SQLModel, table=True):
    """
    Represents a single message inside a ChatSession.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="chatsession.id")
    role: str # "user", "model", or "system"
    content: str
    
    # Which provider generated this message (null if it's a user message)
    provider_id: Optional[int] = Field(default=None, foreign_key="provider.id")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
