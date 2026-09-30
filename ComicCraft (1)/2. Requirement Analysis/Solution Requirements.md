**Team ID:** SWTID-2026-9211  
**Project Title:** ComicCraft - AI Comic Story Creator using Gemini Models  
**Team Size:** 5  
**Team Leader:** Dharshini  
**Team Members:** Pavi, J. Sakthi Devathai, Pavithra Mahadevan, Bhuvaneshwari

---

# Solution Requirements

## Functional Requirements

| FR No. | Functional Requirement (Epic) | Sub Requirement (Story / Sub-Task) |
|--------|-------------------------------|------------------------------------|
| FR-1 | Story Input | User enters story idea, genre, characters, number of panels |
| FR-2 | Art Style Selection | User selects style: Manga, Cartoon, Superhero, Watercolor, Retro |
| FR-3 | Script Generation | Gemini text model creates panel-wise scene description, dialogue and caption in JSON |
| FR-4 | Character Consistency | System builds a character sheet and reuses it in every panel prompt |
| FR-5 | Panel Image Generation | Gemini image model generates one image per panel |
| FR-6 | Speech Bubble Overlay | Dialogue and captions are drawn on each panel image |
| FR-7 | Comic Layout | Panels are arranged into a comic page grid |
| FR-8 | Edit & Regenerate | User edits dialogue or regenerates a single panel |
| FR-9 | Export | User downloads comic as PDF and PNG |

## Non-Functional Requirements

| NFR No. | Non-Functional Requirement | Description |
|---------|----------------------------|-------------|
| NFR-1 | Usability | Simple single-page interface usable by non-technical users |
| NFR-2 | Security | Gemini API key stored in environment variable / secrets, never in code |
| NFR-3 | Reliability | Retry logic for API failures and JSON parsing errors |
| NFR-4 | Performance | Script generated in under 10 seconds; each panel image in about 15-30 seconds |
| NFR-5 | Availability | Available whenever Gemini API and hosting service are online |
| NFR-6 | Scalability | Modular design allows more styles, languages and panel counts |
| NFR-7 | Content Safety | Gemini safety filters block unsafe story inputs and outputs |
