from google import genai
from app.core.config import settings

client = genai.Client(
    api_key=settings.google_api_key
)

def get_models_by_category():
    """
    Retrieve and categorize all available Google GenAI models.
    Returns:
        dict: A dictionary where keys are generation categories (e.g., 'text_generation') 
              and values are lists of corresponding model objects.
    """

    categories = {
        "text_generation": [],
        "image_generation": [],
        "video_generation": [],
        "audio_generation": [],
        "embedding": [],
        "gui_agents": [],
        "sandbox_agents": [],
        "deep_research": [],
        "Grounded_qa": []
    }
    
    # Get all models available
    available_models = client.models.list()
    
    for model in available_models:
        name = model.name.lower()
        display_name = model.display_name.lower()

        if "banana" in display_name or "imagen" in name:
            categories["image_generation"].append(model)

        elif "omni" in name or "veo" in name:
            categories["video_generation"].append(model)

        elif any(k in name for k in ["tts", "lyria", "audio", "live"]):
            categories["audio_generation"].append(model)

        elif "embedding" in name:
            categories["embedding"].append(model)

        elif "computer_use" in name:
            categories["gui_agents"].append(model)

        elif "antigravity" in name:
            categories["sandbox_agents"].append(model)

        elif "deep" in name:
            categories["deep_research"].append(model)

        elif "aqa" in name:
            categories["Grounded_qa"].append(model)
            
        elif "robotics" in name:
            categories["robotics"].append(model)
            
        elif "gemini" in name or "gemma" in name:
            categories["text_generation"].append(model)

    return categories
