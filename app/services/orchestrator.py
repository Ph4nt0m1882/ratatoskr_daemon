from typing import AsyncGenerator
from app.services.core.base_text import BaseTextProvider
from app.services.text_generation.google_ai import GoogleTextProvider

class Orchestrator:
    """
    Main router that delegates requests to the appropriate AI provider.
    """

    def _get_text_provider(self, provider_name: str, model_name: str) -> BaseTextProvider:
        """
        Instantiates and returns the correct text provider.
        
        Args:
            provider_name (str): The name of the provider (e.g., 'google', 'anthropic').
            model_name (str): The specific model to use.
            
        Returns:
            BaseTextProvider: A configured text generation provider.
            
        Raises:
            ValueError: If the provider is not supported.
        """
        provider_name = provider_name.lower()
        
        if provider_name == "google": # google provider 
            return GoogleTextProvider(model_name=model_name)
        ## add only 2 lines for add a new provider
        
        else:
            raise ValueError(f"Provider '{provider_name}' is not supported for text generation.")

    async def stream_text(self, provider_name: str, model_name: str, prompt: str) -> AsyncGenerator[str, None]:
        """
        Streams text from the requested provider.
        
        Args:
            provider_name (str): The provider to use.
            model_name (str): The model to use.
            prompt (str): The user's input.
            
        Yields:
            str: Chunks of the generated text.
        """
        provider = self._get_text_provider(provider_name, model_name)
        
        async for chunk in provider.generate_stream(prompt):
            yield chunk


orchestrator = Orchestrator()