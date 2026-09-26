import re


def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    """
    Organizes the generated images and full comic story into a structured layout.
    
    Args:
        image_paths (list): List of image file paths for each panel.
        full_story (str): Full story text returned by Gemini Pro.
        outline (list): List of outline dictionaries from Gemini Flash.
        
    Returns:
        list: A list of dictionaries containing panel number, title, image_path, text, scene_description, and image_prompt.
    """
    # Split the full story into individual panel segments
    raw_segments = re.split(r'\*\*Panel\s*\d+[:\s]*', full_story, flags=re.IGNORECASE)
    segments = [s.strip() for s in raw_segments if s.strip()]

    # If regex split gave fewer segments than expected, fallback to line splitting
    if len(segments) < len(outline):
        parts = [p.strip() for p in full_story.split("**Panel") if p.strip()]
        if parts:
            segments = parts

    layout = []
    num_panels = max(len(image_paths), len(outline), len(segments), 1)

    for idx in range(1, num_panels + 1):
        # Image path
        img = image_paths[idx - 1] if idx - 1 < len(image_paths) else "static/panels/default.png"
        
        # Panel Info from outline
        panel_info = outline[idx - 1] if idx - 1 < len(outline) and isinstance(outline[idx - 1], dict) else {}
        title = panel_info.get("title", f"Panel {idx}")
        scene_desc = panel_info.get("scene_description", "")
        img_prompt = panel_info.get("image_prompt", "")

        # Story text for this panel
        if idx - 1 < len(segments):
            text_seg = segments[idx - 1]
            # Strip initial redundant title line if present
            lines = text_seg.splitlines()
            if len(lines) > 1 and ("Panel" in lines[0] or ":" in lines[0]):
                cleaned_text = "\n".join(lines[1:]).strip()
            else:
                cleaned_text = text_seg.strip()
        else:
            cleaned_text = scene_desc

        layout.append({
            "panel": idx,
            "title": title,
            "image_path": img,
            "text": cleaned_text,
            "scene_description": scene_desc,
            "image_prompt": img_prompt
        })

    return layout
