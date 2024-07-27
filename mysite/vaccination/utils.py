from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from django.http import FileResponse
import io


def generate_pdf(context):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setTitle(context["pdf_title"])
    p.drawString(40, 800, context["date"])
    p.line(20, 795, 570, 795)
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(300, 750, context["title"])
    p.setFont("Helvetica", 12)
    p.drawCentredString(300, 700, context["subtitle"])
    para_style = ParagraphStyle(
        "paraStyle", fontSize=14, leading=20, firstLineIndent=25
    )
    para = Paragraph(context["content"], para_style)
    para.wrapOn(p, 500, 200)  
    para.drawOn(p, 40, 600) 
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True, filename=context["pdf_title"] + ".pdf"
    )