**Team ID:** SWTID-2026-9211  
**Project Title:** ComicCraft - AI Comic Story Creator using Gemini Models  
**Team Size:** 5  
**Team Leader:** Dharshini  
**Team Members:** Pavi, J. Sakthi Devathai, Pavithra Mahadevan, Bhuvaneshwari

---

# Project Development

## Module-wise Development Summary

| S.No | Module | Description | Technology / Model Used | Developed By | Status |
|------|--------|-------------|-------------------------|--------------|--------|
| 1 | Project Setup | Repository, virtual environment, requirements.txt, .env for API key | Python, Git | Dharshini | Completed |
| 2 | Story Input UI | Form for story idea, genre, style, characters and panel count | Streamlit | Bhuvaneshwari | Completed |
| 3 | Script Generator | Converts story into panel JSON (scene, dialogue, caption) | Gemini text model | Pavi | Completed |
| 4 | Character Sheet | Builds fixed character descriptions reused in every panel | Prompt engineering | Pavithra Mahadevan | Completed |
| 5 | Image Generator | Creates panel artwork from scene prompt and style | Gemini image model | J. Sakthi Devathai | Completed |
| 6 | Speech Bubble Engine | Draws dialogue bubbles and captions on panels | Pillow | Bhuvaneshwari | Completed |
| 7 | Layout & Export | Page grid layout and PDF / PNG download | Pillow, ReportLab | Dharshini | Completed |
| 8 | Edit & Regenerate | Edit dialogue and regenerate a single panel | Streamlit session state | J. Sakthi Devathai | Completed |

## Key Prompt Design

| Prompt Type | Purpose | Sample Prompt |
|-------------|---------|---------------|
| Script Prompt | Get panel-wise JSON | "Convert this story into {n} comic panels. Return only JSON with panel_no, scene, dialogue, caption." |
| Character Prompt | Keep look consistent | "Describe each main character in fixed visual detail: age, hair, clothes, colours." |
| Image Prompt | Draw one panel | "{style} comic panel. Scene: {scene}. Characters: {character_sheet}. No text in image." |

## Suggested Code Structure

| File | Purpose |
|------|---------|
| app.py | Streamlit main application |
| script_generator.py | Gemini text calls and JSON parsing |
| image_generator.py | Gemini image calls |
| layout.py | Speech bubbles, page layout, export |
| requirements.txt | streamlit, google-genai, pillow, reportlab, python-dotenv |
| .env | GEMINI_API_KEY (not uploaded to GitHub) |
