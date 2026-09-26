import os
import re
import time
import hashlib
import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

PANEL_DIR = os.path.join("static", "panels")
os.makedirs(PANEL_DIR, exist_ok=True)

HF_API_KEY = os.getenv("HF_API_KEY")


def sanitize_filename(prompt: str, max_length: int = 40) -> str:
    """Sanitizes the prompt into a safe filesystem filename."""
    clean = re.sub(r'[^a-zA-Z0-9_\-\s]', '', prompt)
    clean = re.sub(r'\s+', '_', clean).strip('_')
    if not clean:
        clean = "comic_panel"
    short_hash = hashlib.md5(prompt.encode('utf-8')).hexdigest()[:6]
    return f"{clean[:max_length]}_{short_hash}.png"


def generate_image(prompt: str, filename: str = None) -> str:
    """
    Generates a comic-style image based on the provided image prompt.
    Saves to static/panels and returns the relative web path.
    
    Args:
        prompt (str): Prompt describing the comic panel scene.
        filename (str, optional): Target filename. If not provided, generates sanitized name.
        
    Returns:
        str: Relative file path to the saved image (e.g., 'static/panels/...').
    """
    if not filename:
        filename = sanitize_filename(prompt)
    elif not filename.endswith(".png") and not filename.endswith(".jpg"):
        filename = f"{filename}.png"

    output_path = os.path.join(PANEL_DIR, filename)

    # If image already generated, reuse it
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1024:
        return output_path.replace("\\", "/")

    # Strategy 1: Hugging Face Inference API (if HF_API_KEY is provided)
    hf_token = os.getenv("HF_API_KEY")
    if hf_token and hf_token != "your-huggingface-api-key-here":
        try:
            api_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": f"Bearer {hf_token}"}
            payload = {
                "inputs": f"comic book illustration, {prompt}, masterpiece, vibrant comic style, comic book coloring, detailed ink linework",
                "options": {"wait_for_model": True}
            }
            res = requests.post(api_url, headers=headers, json=payload, timeout=30)
            if res.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(res.content)
                print(f"[AI] Generated image via HF API: {output_path}")
                return output_path.replace("\\", "/")
        except Exception as e:
            print("[X] HF API error, falling back to dynamic comic renderer:", e)

    # Strategy 2: High quality stylized comic canvas generator (Pillow)
    _create_stylized_comic_art(prompt, output_path)
    return output_path.replace("\\", "/")


def _create_stylized_comic_art(prompt: str, output_path: str):
    """Generates a vivid, stylish comic-book visual panel using Pillow."""
    width, height = 768, 512
    img = Image.new("RGB", (width, height), (20, 24, 38))
    draw = ImageDraw.Draw(img)

    # Compute a deterministic palette based on prompt
    p_hash = int(hashlib.md5(prompt.encode('utf-8')).hexdigest(), 16)
    
    # Comic color themes
    themes = [
        # Sunset / Dramatic
        {"sky_top": (255, 94, 98), "sky_bot": (255, 153, 102), "glow": (255, 220, 120), "shadow": (35, 20, 50)},
        # Enchanted Forest / Fantasy
        {"sky_top": (18, 52, 86), "sky_bot": (42, 128, 98), "glow": (144, 238, 144), "shadow": (12, 28, 20)},
        # Cyberpunk / Sci-Fi
        {"sky_top": (20, 10, 40), "sky_bot": (0, 168, 255), "glow": (255, 0, 128), "shadow": (10, 5, 25)},
        # Comic Action / Classic
        {"sky_top": (230, 57, 70), "sky_bot": (241, 250, 238), "glow": (255, 215, 0), "shadow": (29, 53, 87)},
        # Mystic Night / Deep Space
        {"sky_top": (10, 10, 30), "sky_bot": (80, 40, 120), "glow": (200, 160, 255), "shadow": (5, 5, 15)},
    ]
    theme = themes[p_hash % len(themes)]

    # Draw sky gradient
    top_c = theme["sky_top"]
    bot_c = theme["sky_bot"]
    for y in range(height):
        r = int(top_c[0] + (bot_c[0] - top_c[0]) * (y / height))
        g = int(top_c[1] + (bot_c[1] - top_c[1]) * (y / height))
        b = int(top_c[2] + (bot_c[2] - top_c[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add sun / celestial glow
    sun_x = (p_hash % 300) + 200
    sun_y = 120 + (p_hash % 80)
    for radius in range(110, 0, -10):
        alpha_factor = (110 - radius) / 110.0
        glow_c = (
            int(theme["glow"][0] * alpha_factor + top_c[0] * (1 - alpha_factor)),
            int(theme["glow"][1] * alpha_factor + top_c[1] * (1 - alpha_factor)),
            int(theme["glow"][2] * alpha_factor + top_c[2] * (1 - alpha_factor)),
        )
        draw.ellipse([sun_x - radius, sun_y - radius, sun_x + radius, sun_y + radius], fill=glow_c)

    # Draw comic sunburst / speed lines
    for i in range(16):
        import math
        angle = (i * 22.5 + (p_hash % 20)) * math.pi / 180
        x2 = sun_x + int(math.cos(angle) * 600)
        y2 = sun_y + int(math.sin(angle) * 600)
        draw.line([(sun_x, sun_y), (x2, y2)], fill=(255, 255, 255), width=1)

    # Draw silhouette mountain / landscape layers
    shadow = theme["shadow"]
    
    # Layer 1: Distant hills
    l1_points = [(0, height)]
    for x in range(0, width + 50, 40):
        hill_y = int(height * 0.55 + math.sin((x + p_hash) * 0.01) * 45)
        l1_points.append((x, hill_y))
    l1_points.append((width, height))
    mid_shadow = (int((shadow[0] + bot_c[0]) * 0.5), int((shadow[1] + bot_c[1]) * 0.5), int((shadow[2] + bot_c[2]) * 0.5))
    draw.polygon(l1_points, fill=mid_shadow)

    # Layer 2: Foreground ground
    l2_points = [(0, height)]
    for x in range(0, width + 50, 30):
        ground_y = int(height * 0.72 + math.cos((x + p_hash * 2) * 0.015) * 35)
        l2_points.append((x, ground_y))
    l2_points.append((width, height))
    draw.polygon(l2_points, fill=shadow)

    # Draw comic hero / focal silhouette
    cx = width // 2 + ((p_hash % 100) - 50)
    cy = int(height * 0.73)
    
    # Silhouette character (Caped hero / adventurer / explorer)
    draw.ellipse([cx - 16, cy - 65, cx + 16, cy - 33], fill=(10, 10, 15)) # head/helmet
    draw.polygon([(cx - 28, cy - 35), (cx + 28, cy - 35), (cx + 22, cy + 25), (cx - 22, cy + 25)], fill=(10, 10, 15)) # body
    # Legs
    draw.line([(cx - 14, cy + 25), (cx - 20, cy + 65)], fill=(10, 10, 15), width=9)
    draw.line([(cx + 14, cy + 25), (cx + 20, cy + 65)], fill=(10, 10, 15), width=9)
    # Cape fluttering
    draw.polygon([(cx - 20, cy - 30), (cx - 65, cy + 15), (cx - 45, cy + 45), (cx - 10, cy + 10)], fill=(20, 15, 30))

    # Bold comic border and comic halftone effect
    draw.rectangle([6, 6, width - 6, height - 6], outline=(255, 255, 255), width=3)
    draw.rectangle([10, 10, width - 10, height - 10], outline=(15, 15, 20), width=4)

    # Comic style header badge
    badge_w, badge_h = 240, 32
    draw.rectangle([14, 14, 14 + badge_w, 14 + badge_h], fill=(255, 220, 0), outline=(0, 0, 0), width=2)
    
    # Render stylized badge text
    title_snippet = "COMIC CRAFT STUDIO"
    draw.text((24, 20), title_snippet, fill=(0, 0, 0))

    img.save(output_path, "PNG")
