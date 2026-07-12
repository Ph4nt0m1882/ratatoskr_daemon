from typing import Protocol, AsyncGenerator

class BaseTextProvider(Protocol):
    """
    Contract for all text generation providers.
    Any class implementing this protocol must provide the methods below.
    """
    
    async def generate_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """
        Generates a text response as a stream of chunks.
        
        Args:
            prompt (str): The user's input text.
            
        Yields:
            str: Chunks of the generated text as they become available.
        """
        ...
        
    async def generate_text(self, prompt: str) -> str:
        """
        Generates a complete text response (blocking until finished).
        
        Args:
            prompt (str): The user's input text.
            
        Returns:
            str: The full generated text.
        """
        ...
