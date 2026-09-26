import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def generate_outline(user_prompt: str) -> list:
    """
    Generates a 5-panel comic layout based on the user's story prompt using Gemini Flash.
    
    Args:
        user_prompt (str): The user's comic idea prompt.
        
    Returns:
        list: A list of dictionaries, one for each panel.
    """
    prompt = f"""
You are a professional AI comic planner.

Your task is to generate a *strictly formatted* JSON array containing 5 panel descriptions for a comic based on the story idea below:

STORY: "{user_prompt}"

Each JSON object must include:
- "panel": (integer)
- "title": (string)
- "scene_description": (string)
- "image_prompt": (string)

Respond ONLY in this valid JSON format, without any explanations or markdown:
[
  {{
    "panel": 1,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
  }},
  {{
    "panel": 2,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
  }},
  {{
    "panel": 3,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
  }},
  {{
    "panel": 4,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
  }},
  {{
    "panel": 5,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
  }}
]
"""
    output_text = ""
    try:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY is not configured.")
        genai.configure(api_key=api_key)

        model = None
        for model_name in ["models/gemini-2.5-flash", "gemini-2.5-flash", "models/gemini-3.8-flash", "gemini-3.8-flash", "models/gemini-1.5-flash", "gemini-1.5-flash", "gemini-pro"]:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                output_text = response.text.strip()
                break
            except Exception as model_err:
                print(f"[!] Model {model_name} failed: {model_err}, trying next...")
                continue

        if not output_text:
            raise ValueError("No output generated from Gemini Flash models.")
        print("\n[AI] RAW GEMINI RESPONSE:\n", output_text)

        # Remove any markdown formatting if present
        clean_text = output_text
        if clean_text.startswith("```json"):
            clean_text = clean_text.replace("```json", "", 1).replace("```", "").strip()
        elif clean_text.startswith("```"):
            clean_text = clean_text.replace("```", "").strip()

        # Regex fallback to extract JSON array
        json_match = re.search(r'\[.*\]', clean_text, re.DOTALL)
        if json_match:
            clean_text = json_match.group(0)

        panel_data = json.loads(clean_text)

        if not isinstance(panel_data, list):
            raise ValueError("Gemini response is not a list.")

        for panel in panel_data:
            if not isinstance(panel, dict) or not all(key in panel for key in ("panel", "title", "scene_description", "image_prompt")):
                raise ValueError(f"Invalid panel format or missing keys: {panel}")

        return panel_data

    except json.JSONDecodeError as e:
        print("[X] JSON Decode Error:", e)
        print("[X] Full Text Received:\n", output_text)
        return _fallback_outline(user_prompt)
    except Exception as e:
        print("[X] Gemini Outline Generation Exception / Fallback:", e)
        return _fallback_outline(user_prompt)


def _fallback_outline(user_prompt: str) -> list:
    """Smart fallback generator if Gemini API key is missing or offline."""
    prompt_words = user_prompt.strip()
    return [
        {
            "panel": 1,
            "title": "The Journey Begins",
            "scene_description": f"The story starts as the main character embarks on the quest inspired by: {prompt_words}.",
            "image_prompt": f"Comic book art, opening scene of {prompt_words}, heroic character standing at threshold, vibrant colors, detailed line art, dynamic angle"
        },
        {
            "panel": 2,
            "title": "A Mysterious Discovery",
            "scene_description": "A strange occurrence catches everyone by surprise, shifting the atmosphere.",
            "image_prompt": f"Comic book panel, mysterious discovery related to {prompt_words}, glowing atmospheric lighting, curiosity and wonder, high contrast"
        },
        {
            "panel": 3,
            "title": "Facing the Challenge",
            "scene_description": "The stakes rise as an unexpected obstacle blocks the path forward.",
            "image_prompt": f"Dramatic comic strip illustration, confrontation and tension, bold ink strokes, cinematic composition, action-packed"
        },
        {
            "panel": 4,
            "title": "The Turning Point",
            "scene_description": "With quick thinking and determination, a bold move alters the fate of the journey.",
            "image_prompt": f"Epic comic book climax scene, powerful breakthrough moment, radiant energy, dramatic perspective, stylized comic art"
        },
        {
            "panel": 5,
            "title": "A New Horizon",
            "scene_description": "The dust settles, revealing victory and hope for the adventures ahead.",
            "image_prompt": f"Serene yet triumphant comic scene, sunset background, peaceful resolution, colorful comic palette, detailed finish"
        }
    ]
