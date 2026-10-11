from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_certificate(name: str, course_name: str, event_date: str, recipient_id: int) -> str:
    file_path = OUTPUT_DIR / f"certificate_{recipient_id}.pdf"

    page_size = landscape(A4)
    pdf = canvas.Canvas(str(file_path), pagesize=page_size)
    width, height = page_size

    pdf.setStrokeColorRGB(0.1, 0.3, 0.6)
    pdf.setLineWidth(4)
    pdf.rect(25, 25, width - 50, height - 50)

    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(width / 2, height - 110, "CERTIFICATE OF COMPLETION")

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width / 2, height - 170, "This certificate is proudly presented to")

    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawCentredString(width / 2, height - 220, name)

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width / 2, height - 270, f"For completing: {course_name}")
    pdf.drawCentredString(width / 2, height - 305, f"Date: {event_date}")

    pdf.save()
    return str(file_path)