import os
from datetime import datetime
from fpdf import FPDF

EXPORT_FOLDER = os.path.join("static", "exports")
os.makedirs(EXPORT_FOLDER, exist_ok=True)


class ComicPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(120, 120, 140)
        self.cell(0, 8, 'ComicCraft - AI Story Creator', align='L')
        self.cell(0, 8, 'Generated with Gemini Models', align='R', ln=True)
        self.set_draw_color(220, 220, 230)
        self.line(10, 18, 200, 18)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(160, 160, 180)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def clean_pdf_text(text: str) -> str:
    """Removes unsupported characters for standard PDF fonts and cleans markdown syntax."""
    if not text:
        return ""
    # Strip markdown bold/italics
    cleaned = text.replace("**", "").replace("*", "").replace("`", "")
    # Normalize common Unicode characters
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\u2026": "...", "\u2022": "-"
    }
    for orig, rep in replacements.items():
        cleaned = cleaned.replace(orig, rep)
    # Ensure latin-1 / ascii compatibility
    return cleaned.encode('latin-1', 'replace').decode('latin-1')


def save_pdf(layout: list) -> str:
    """
    Compiles the full comic into a multi-page PDF file using FPDF.
    Each panel's image and narration are placed neatly on separate pages.
    
    Args:
        layout (list): List of panel dictionaries.
        
    Returns:
        str: Relative path to the generated PDF.
    """
    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        
        panel_num = panel.get("panel", 1)
        title = clean_pdf_text(panel.get("title", f"Panel {panel_num}"))
        image_path = panel.get("image_path", "")
        story_text = clean_pdf_text(panel.get("text", ""))
        scene_desc = clean_pdf_text(panel.get("scene_description", ""))

        # Panel Header
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 10, f"Panel {panel_num}: {title}", ln=True, align="C")
        pdf.ln(3)

        # Image placement
        if image_path and os.path.exists(image_path):
            img_x = 20
            img_y = pdf.get_y()
            img_w = 170
            img_h = 100
            # Draw comic frame border
            pdf.set_draw_color(40, 40, 50)
            pdf.set_line_width(0.8)
            pdf.rect(img_x - 1, img_y - 1, img_w + 2, img_h + 2)
            pdf.image(image_path, x=img_x, y=img_y, w=img_w, h=img_h)
            pdf.set_xy(10, img_y + img_h + 8)
        else:
            pdf.set_x(10)
            pdf.set_font('Helvetica', 'I', 11)
            pdf.set_text_color(180, 50, 50)
            pdf.multi_cell(0, 10, f"[Panel Illustration: {image_path}]")
            pdf.ln(5)

        # Scene Description (in italics)
        if scene_desc:
            pdf.set_x(10)
            pdf.set_font('Helvetica', 'I', 10)
            pdf.set_text_color(90, 100, 120)
            pdf.multi_cell(w=190, h=6, text=f"Scene: {scene_desc}")
            pdf.ln(4)

        # Story narration & dialogue
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(20, 20, 30)

        # Print line by line with styling for CAPTION / NARRATION / DIALOGUE
        for line in story_text.splitlines():
            line = line.strip()
            if not line:
                continue
            pdf.set_x(10)
            if line.upper().startswith("CAPTION:"):
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_text_color(14, 116, 144)
                pdf.multi_cell(w=190, h=6, text=line)
            elif line.upper().startswith("NARRATION:"):
                pdf.set_font('Helvetica', 'I', 10)
                pdf.set_text_color(51, 65, 85)
                pdf.multi_cell(w=190, h=6, text=line)
            elif line.upper().startswith("DIALOGUE:") or '"' in line:
                pdf.set_font('Helvetica', 'B', 10)
                pdf.set_text_color(194, 65, 12)
                pdf.multi_cell(w=190, h=6, text=line)
            else:
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(30, 41, 59)
                pdf.multi_cell(w=190, h=6, text=line)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(pdf_path)

    print(f"[PDF] Comic exported to {pdf_path}")
    return pdf_path.replace("\\", "/")
