import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def generate_story(outline: list) -> str:
    """
    Generates a detailed comic story with narration and character dialogue
    from a list of comic panel outlines using Gemini Pro.
    
    Args:
        outline (list): A list of dictionaries or strings representing each comic panel's idea.
        
    Returns:
        str: The generated comic story text or formatted fallback story.
    """
    # Format the panel outline as a numbered list for clarity
    formatted_items = []
    for i, item in enumerate(outline):
        if isinstance(item, dict):
            panel_num = item.get("panel", i + 1)
            title = item.get("title", f"Panel {panel_num}")
            desc = item.get("scene_description", "")
            formatted_items.append(f"Panel {panel_num}: {title} - {desc}")
        else:
            formatted_items.append(f"Panel {i+1}: {item}")

    formatted_outline = "\n".join(formatted_items)

    prompt = f"""
You're a comic book writer.

Given the following panel breakdown, write a comic-style story with engaging narration and character dialogues for each panel.

Panel Outline:
{formatted_outline}

Guidelines:
- Use a fun and engaging tone, like an actual comic book.
- Include narration and clearly marked character lines.
- Keep each panel self-contained but part of a cohesive story.
- Structure each panel clearly with "**Panel [number]: [Title]**", followed by "**SCENE:** ...", "**CAPTION:** ...", "**NARRATION:** ...", and "**DIALOGUE:** ...".

Format strictly as:
**Panel 1: [Title]**
**SCENE:** [Brief scene setting description]
**CAPTION:** [Atmospheric caption]
**NARRATION:** [Engaging narration]
**Panel 2: [Title]**
...
"""
    try:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY is not configured.")
        genai.configure(api_key=api_key)

        story_text = ""
        for model_name in ["models/gemini-2.5-pro", "gemini-2.5-pro", "models/gemini-2.5-flash", "gemini-2.5-flash", "models/gemini-3.8-flash", "gemini-3.8-flash", "models/gemini-1.5-pro", "gemini-1.5-pro", "gemini-pro"]:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                story_text = response.text.strip()
                break
            except Exception as model_err:
                print(f"[!] Model {model_name} failed: {model_err}, trying next...")
                continue

        if not story_text:
            raise ValueError("No story generated from Gemini Pro models.")
        print("\n[AI] GEMINI PRO STORY GENERATED:\n", story_text[:200], "...")
        return story_text

    except Exception as e:
        print("[X] Gemini Pro Story Generation Exception / Fallback:", e)
        return _fallback_story(outline)


def _fallback_story(outline: list) -> str:
    """Smart fallback comic story narration and dialogue generator."""
    story_panels = []
    for i, item in enumerate(outline):
        p_num = item.get("panel", i + 1) if isinstance(item, dict) else i + 1
        title = item.get("title", f"The Journey Unfolds") if isinstance(item, dict) else f"Chapter {p_num}"
        desc = item.get("scene_description", "The adventure continues with great excitement.") if isinstance(item, dict) else str(item)

        panel_text = f"""**Panel {p_num}: {title}**
**SCENE:** {desc}
**CAPTION:** The wind whispers secrets across the horizon as destiny calls.
**NARRATION:** With sharp eyes and relentless courage, our hero steps forward into the unknown. Every step reverberates with purpose.
**DIALOGUE:** "Whatever lies ahead, we are ready. Let's make every moment count!" """
        story_panels.append(panel_text)

    return "\n\n".join(story_panels)
