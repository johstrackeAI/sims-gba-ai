import requests
import base64
import io
import json
from PIL import Image

# Import settings from the config file
from sims_gba_ai.config import settings

def image_to_base64(image: Image.Image) -> str:
    """Converts a PIL Image object to a base64 encoded string."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str

def get_llm_suggestion(image: Image.Image) -> str | None:
    """
    Sends the captured screen image to the configured LLM API
    and returns a single suggested GBA button press based on the response.

    Args:
        image: A PIL.Image object of the screen capture.

    Returns:
        A string representing a valid GBA button ("Up", "Down", "Left", "Right", "A", "B")
        if the LLM provides a valid suggestion, otherwise None.
    """
    base64_image = image_to_base64(image)
    prompt = f"Look at this screenshot from The Sims 2 GBA. Based *only* on what you see, suggest *one single button* to press next from this list: {', '.join(settings.VALID_GBA_BUTTONS)}."

    headers = {}
    payload = {}
    api_url = ""

    if settings.LLM_PROVIDER == "lmstudio":
        api_url = f"{settings.LMSTUDIO_API_BASE}/chat/completions"
        # lmstudio uses OpenAI compatible API structure
        payload = {
            "model": "loaded-model", # lmstudio uses the model loaded in the UI
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 10 # Limit response length
        }
        # No specific headers usually needed for local lmstudio

    elif settings.LLM_PROVIDER == "openrouter":
        api_url = f"{settings.OPENROUTER_API_BASE}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": settings.LLM_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 10 # Limit response length
        }
    else:
        print(f"Error: Invalid LLM_PROVIDER configured: {settings.LLM_PROVIDER}")
        return None

    try:
        print(f"LLM Input Payload: {json.dumps(payload, indent=2)}") # DEBUG
        response = requests.post(api_url, headers=headers, json=payload, timeout=30) # Added timeout
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        response_json = response.json()

        # Extract content - structure might vary slightly, adjust if needed
        if 'choices' in response_json and len(response_json['choices']) > 0:
            message = response_json['choices'][0].get('message', {})
            suggestion_text = message.get('content', '').strip()

            # Clean up potential extra formatting
            suggestion_text = suggestion_text.replace('"', '').replace("'", "").strip()

            # Validate against the allowed buttons
            if suggestion_text in settings.VALID_GBA_BUTTONS:
                print(f"LLM Output Suggestion: {suggestion_text}") # DEBUG
                print(f"LLM Suggestion: {suggestion_text}") # Original print
                return suggestion_text
            else:
                print(f"LLM Response ('{suggestion_text}') not a valid button.")
                return None
        else:
            print(f"Error: Unexpected response format from LLM: {response_json}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error sending request to LLM API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during LLM interaction: {e}")
        return None