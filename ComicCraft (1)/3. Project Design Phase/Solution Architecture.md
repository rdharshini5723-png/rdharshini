**Team ID:** SWTID-2026-9211  
**Project Title:** ComicCraft - AI Comic Story Creator using Gemini Models  
**Team Size:** 5  
**Team Leader:** Dharshini  
**Team Members:** Pavi, J. Sakthi Devathai, Pavithra Mahadevan, Bhuvaneshwari

---

# Solution Architecture

```
+-----------+     +-------------------+     +--------------------------+
|   User    | --> | Streamlit Web UI  | --> |   Application Backend    |
+-----------+     +-------------------+     |  (Python Controller)     |
                                            +-----------+--------------+
                                                        |
        +-----------------------+-----------------------+-----------------------+
        |                       |                       |                       |
+---------------+     +-------------------+   +--------------------+   +----------------+
| Prompt Builder|     | Gemini Text Model |   | Gemini Image Model |   | Pillow Layout  |
| + Char Sheet  |     | (Panel Script)    |   | (Panel Artwork)    |   | + PDF Export   |
+---------------+     +-------------------+   +--------------------+   +----------------+
                                                        |
                                            +-----------v--------------+
                                            |   Final Comic (PDF/PNG)  |
                                            +--------------------------+
```

| Component | Description | Technology |
|-----------|-------------|------------|
| Presentation Layer | Collects story input, shows script, panels and download buttons | Streamlit |
| Prompt Builder | Creates structured prompts with style and character sheet | Python |
| Script Generator | Produces panel scenes, dialogue and captions as JSON | Gemini text model |
| Image Generator | Creates one illustration per panel | Gemini image model |
| Layout Engine | Draws speech bubbles, captions and arranges panels | Pillow |
| Export Module | Converts the final layout into PDF and PNG | ReportLab / img2pdf |
| Config & Security | Loads API key from environment | python-dotenv |
