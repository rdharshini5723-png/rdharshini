import os
import traceback
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")


class PromptRequest(BaseModel):
    prompt: str = Field(..., description="Main story prompt")
    character_name: str = Field(default="Hero", description="Main character name")
    setting: str = Field(default="Enchanted Forest", description="Setting location")
    tone: str = Field(default="Dramatic", description="Tone of the story")
    style: str = Field(default="Anime", description="Visual art style")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Loads the homepage where users can submit their story details."""
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form("Hero"),
    setting: str = Form("Enchanted Forest"),
    tone: str = Form("Dramatic"),
    style: str = Form("Anime")
):
    """Handles HTML form submission, processes input through AI pipeline, and returns comic preview."""
    try:
        # Combine user input into a single full prompt
        full_prompt = (
            f"{prompt.strip()}\n"
            f"The main character is {character_name.strip()}.\n"
            f"The setting is a {setting.strip()}.\n"
            f"The tone is {tone.strip()}.\n"
            f"The art style is {style.strip()}."
        )

        # Step 1: Generate panel outline
        outline = generate_outline(full_prompt)
        if not isinstance(outline, list):
            raise ValueError("Invalid outline structure from Gemini response.")

        # Step 2: Generate story
        full_story = generate_story(outline)

        # Step 3: Generate images for each panel
        images = []
        for panel in outline:
            p_prompt = panel.get("image_prompt", "")
            if not p_prompt:
                p_prompt = f"{style} style, {character_name} in {setting}, {panel.get('scene_description', '')}"
            img_path = generate_image(p_prompt)
            images.append(img_path)

        # Step 4: Build Layout
        layout = build_comic_layout(images, full_story, outline)

        # Step 5: Export to PDF
        pdf_path = save_pdf(layout)
        web_pdf_path = "/" + pdf_path.replace("\\", "/").lstrip("/")

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout,
                "pdf_path": web_pdf_path,
                "prompt": prompt,
                "character_name": character_name,
                "setting": setting,
                "tone": tone,
                "style": style
            }
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    """API route that accepts JSON payloads and returns comic layout and PDF path."""
    try:
        full_prompt = (
            f"{payload.prompt}\n"
            f"The main character is {payload.character_name}.\n"
            f"The setting is a {payload.setting}.\n"
            f"The tone is {payload.tone}.\n"
            f"The art style is {payload.style}."
        )

        outline = generate_outline(full_prompt)
        full_story = generate_story(outline)
        images = [generate_image(panel.get("image_prompt", payload.prompt)) for panel in outline]
        layout = build_comic_layout(images, full_story, outline)
        pdf_path = save_pdf(layout)

        return JSONResponse(content={
            "status": "success",
            "layout": layout,
            "pdf_path": "/" + pdf_path.replace("\\", "/").lstrip("/")
        })
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str = ""):
    """Displays a success confirmation page after the comic is downloaded."""
    clean_path = "/" + pdf_path.replace("\\", "/").lstrip("/") if pdf_path else ""
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_path": clean_path}
    )


@router.get("/test-image")
async def test_image(prompt: str = "A futuristic city at sunset, sci-fi, cinematic, artstation"):
    """Developer utility route to test image generation from a direct prompt."""
    try:
        image_path = generate_image(prompt)
        return {
            "message": "Image generated successfully",
            "path": "/" + image_path.replace("\\", "/").lstrip("/")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
