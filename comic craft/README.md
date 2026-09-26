# ComicCraft - AI Comic Story Creator using Gemini Models

ComicCraft is a web-based application that uses AI to generate personalized comic book stories and illustrations based on user-provided prompts. Built with **FastAPI** and integrated with Google's **Gemini AI models** along with **Stable Diffusion**, ComicCraft streamlines the creative process of generating storylines, dialogues, and vivid comic-style imagery automatically.

---

## 🌟 Key Features

- **Personalized Comic Creation**: Accepts story prompts, character name, setting, tone, and art style.
- **Gemini 1.5 Flash Outline Generator**: Generates structured 5-panel comic breakdown with scene descriptions and tailored image prompts.
- **Gemini 1.5 Pro Storyteller**: Expands outlines into full narrative scripts with captions and character dialogues.
- **Comic-Style Visuals**: Automatically produces comic illustrations with Stable Diffusion / Hugging Face Diffusers & stylized comic graphic engine.
- **Structured Layout Binding**: Assembles titles, narration, dialogue, and illustrations sequentially.
- **Multi-Page PDF Exporter**: Compiles comics into downloadable PDF format using FPDF.
- **Responsive Web UI**: Jinja2 templates with vibrant comic book styling, live preview, and export confirmation.
- **RESTful API**: Full JSON endpoints for programmatic comic generation.

---

## 📁 Project Structure

```
comic craft/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entrypoint
│   ├── routes.py            # Route handlers & endpoints
│   ├── gemini_flash.py      # Outline generation using Gemini Flash
│   ├── gemini_pro.py        # Story narration using Gemini Pro
│   ├── image_generator.py   # Comic-style image generation
│   ├── layout_builder.py    # Panel-by-panel layout builder
│   └── exporters.py         # PDF compilation and export
├── templates/
│   ├── index.html           # Homepage input form
│   ├── comic_preview.html   # Comic strip preview page
│   └── export_success.html  # Export success confirmation page
├── static/
│   ├── css/
│   │   └── style.css        # Comic book aesthetic styles
│   ├── panels/              # Generated comic panel images
│   ├── exports/             # Exported PDF files
│   └── fonts/               # Custom fonts (if needed)
├── .env                     # Environment variables (API keys)
├── .env.example             # Environment template
├── requirements.txt         # Project dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+ installed
- Google Gemini API Key ([Google AI Studio](https://aistudio.google.com/))
- (Optional) Hugging Face API Token

### 2. Installation

Clone or open the repository, then install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit the `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
HF_API_KEY=your_huggingface_api_key_here
```

### 4. Run the Application

Start the FastAPI server with Uvicorn:

```bash
uvicorn app.main:app --reload
```

Open your browser and navigate to:
- **Web Interface**: `http://127.0.0.1:8000`
- **Interactive API Docs (Swagger)**: `http://127.0.0.1:8000/docs`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Loads the homepage form (`index.html`) |
| `POST` | `/generate` | Form submission endpoint; generates comic and renders preview |
| `POST` | `/generate-comic/json` | JSON API endpoint returning layout data and PDF path |
| `GET` | `/export-success` | Displays comic export success page |
| `GET` | `/test-image` | Developer utility to test image generation |

---

## 🎭 Example Scenarios

1. **Scenario 1 - Fantasy Adventure**:
   - Prompt: *"A brave fox exploring an enchanted forest."*
   - Character: *Free*
   - Setting: *Enchanted Forest*
   - Tone: *Dramatic*
   - Art Style: *Anime*

2. **Scenario 2 - Light-Hearted Comedy**:
   - Prompt: *"A clumsy robot trying to bake a cake for a birthday party."*
   - Tone: *Funny*
   - Art Style: *Comic Book*
