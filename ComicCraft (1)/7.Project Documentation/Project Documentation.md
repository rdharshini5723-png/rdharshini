**Team ID:** SWTID-2026-9211  
**Project Title:** ComicCraft - AI Comic Story Creator using Gemini Models  
**Team Size:** 5  
**Team Leader:** Dharshini  
**Team Members:** Pavi, J. Sakthi Devathai, Pavithra Mahadevan, Bhuvaneshwari

---

# Project Documentation

| S.No | Section | Details |
|------|---------|---------|
| 1 | Project Title | ComicCraft - AI Comic Story Creator using Gemini Models |
| 2 | Team ID | SWTID-2026-9211 |
| 3 | Team Members | Dharshini (Leader), Pavi, J. Sakthi Devathai, Pavithra Mahadevan, Bhuvaneshwari |
| 4 | Domain | Generative AI - Text and Image Generation |
| 5 | Problem Statement | Non-artists cannot easily convert story ideas into illustrated comics |
| 6 | Objective | Build an app that converts a story idea into a scripted, illustrated and lettered comic using Gemini models |
| 7 | Scope | Story input, script generation, image generation, speech bubbles, layout, edit and export |
| 8 | Models Used | Gemini text model for script; Gemini image model for panel artwork |
| 9 | Technology Stack | Python, Streamlit, google-genai, Pillow, ReportLab, python-dotenv |
| 10 | Architecture | Streamlit UI -> Prompt Builder -> Gemini Text -> Character Sheet -> Gemini Image -> Pillow Layout -> PDF/PNG |
| 11 | Key Features | Character consistency, art styles, editable script, per-panel regenerate, PDF export |
| 12 | Installation | `pip install -r requirements.txt` |
| 13 | Configuration | Add `GEMINI_API_KEY` in `.env` file |
| 14 | How to Run | `streamlit run app.py` |
| 15 | Testing Summary | 12 functional test cases and 6 performance checks passed |
| 16 | Limitations | Minor character variation across panels; depends on API availability and quota |
| 17 | Future Enhancements | Multi-language dialogue, educational mode, voice narration, animated comics |
| 18 | Ethical Considerations | Safety filters enabled; AI-generated content should be labelled; no copyrighted characters |
| 19 | Conclusion | ComicCraft shows how Gemini models can make comic creation simple for everyone |
| 20 | References | Google Gemini API Documentation, Streamlit Documentation, Pillow Documentation |
