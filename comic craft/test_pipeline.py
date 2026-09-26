import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

def run_test():
    print("Testing ComicCraft pipeline...")
    prompt = "A brave fox named Felix exploring an enchanted forest in search of the Sun Stone."
    
    # 1. Outline
    outline = generate_outline(prompt)
    print(f"Outline generated with {len(outline)} panels.")
    assert len(outline) == 5, f"Expected 5 panels, got {len(outline)}"
    
    # 2. Story
    story = generate_story(outline)
    print(f"Story generated ({len(story)} chars).")
    assert len(story) > 50, "Story too short"
    
    # 3. Images
    images = []
    for p in outline:
        img = generate_image(p["image_prompt"])
        images.append(img)
    print(f"Generated {len(images)} images: {images}")
    assert len(images) == 5, "Images count mismatch"
    
    # 4. Layout
    layout = build_comic_layout(images, story, outline)
    print(f"Layout built with {len(layout)} panels.")
    assert len(layout) == 5, "Layout count mismatch"
    
    # 5. PDF Export
    pdf_path = save_pdf(layout)
    print(f"PDF saved to: {pdf_path}")
    assert os.path.exists(pdf_path), "PDF file does not exist"
    print("All pipeline tests PASSED!")

if __name__ == "__main__":
    run_test()
