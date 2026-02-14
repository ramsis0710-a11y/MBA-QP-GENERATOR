```python
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
import os
from datetime import datetime

def generate_qp_pdf(operations, of_data, qcp_ref, material, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/QP_{of_data['wo_no']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=10*mm, leftMargin=10*mm, topMargin=10*mm, bottomMargin=10*mm)
    styles = getSampleStyleSheet()
    normal = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=8)
    elements = []

    # Header
    header_data = [
        ["Global metallic products industries (GMPI)", "", "", ""],
        ["Cod : FO-24-PRO", "", "", ""],
        ["Indice de rév : 4", "", "", ""],
        ["Quality Plan", "", "", ""],
        ["Date de rév : 10/12/2014", "", "", ""],
        ["N° de page : 1/1", "", "", ""],
        ["", "", "", ""],
        [f"Date : {of_data['date']}", f"Commande N°: {of_data['order_no']}", "", ""],
        [f"Quality Control Plan Ref : {qcp_ref}", "Note :", "", ""],
        [f"N° WO : {of_data['wo_no']}", "", "", ""],
        [f"Customer : {of_data['customer']}", "", "", ""],
        [f"In Brief Job : {of_data['product']}", "", "", ""],
    ]
    tbl = Table(header_data, colWidths=[2.2*inch, 2.2*inch, 1.3*inch, 1.3*inch])
    tbl.setStyle(TableStyle([('SPAN', (0,0), (-1,0)), ('SPAN', (0,1), (-1,1)), ('SPAN', (0,2), (-1,2)),
        ('SPAN', (0,3), (-1,3)), ('SPAN', (0,4), (-1,4)), ('SPAN', (0,5), (-1,5)),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,0), 16),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('GRID', (0,7), (-1,-1), 0.5, colors.black)]))
    elements.append(tbl)
    elements.append(Spacer(1, 0.1*inch))

    # Title
    title = Table([["OPERATIONS DE FABRICATION ET DE CONTROLE", "", "", "", "", "", "", ""]], colWidths=[0.5*inch,1.5*inch,0.4*inch,0.4*inch,1.2*inch,1.4*inch,0.8*inch,0.8*inch])
    title.setStyle(TableStyle([('SPAN', (0,0), (-1,0)), ('BACKGROUND', (0,0), (-1,0), colors.grey), ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke)]))
    elements.append(title)

    # Headers
    headers = [["", "Manufacture and Cheking Operations", "Interne", "Tierce Parties", "Documents Applicable", "Critère d'acceptance", "Emargement", "Records", "Commentaire"],
               ["", "", "In-House", "Third Party", "Applicable Specification", "Acceptance criteria", "Signature", "", ""]]
    htable = Table(headers, colWidths=[0.5*inch,1.5*inch,0.4*inch,0.4*inch,1.2*inch,1.4*inch,0.8*inch,0.8*inch])
    htable.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('SPAN', (0,0), (0,1)), ('SPAN', (1,0), (1,1)), ('SPAN', (2,0), (2,1)), ('SPAN', (3,0), (3,1)),
        ('SPAN', (4,0), (4,1)), ('SPAN', (5,0), (5,1)), ('SPAN', (6,0), (6,1)), ('SPAN', (7,0), (7,1)), ('SPAN', (8,0), (8,1))]))
    elements.append(htable)

    for op in operations:
        row = [op['op'], Paragraph(op['description'], normal), op['interne'], op['tierce'],
               Paragraph(op['document'], normal), Paragraph(op['criteria'][:150], normal),
               op['signature'], op['record'], op['comment']]
        rtable = Table([row], colWidths=[0.5*inch,1.5*inch,0.4*inch,0.4*inch,1.2*inch,1.4*inch,0.8*inch,0.8*inch])
        rtable.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 7), ('VALIGN', (0,0), (-1,-1), 'TOP'), ('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
        elements.append(rtable)

    yesno = [["", "", "", "", "", "", "", "Yes", "No"]]
    ytable = Table(yesno, colWidths=[0.5*inch,1.5*inch,0.4*inch,0.4*inch,1.2*inch,1.4*inch,0.8*inch,0.8*inch])
    ytable.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), ('ALIGN', (7,0), (8,0), 'CENTER'), ('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
    elements.append(ytable)
    elements.append(Spacer(1,0.2*inch))

    sig = [["Rédigé par", "Approuvé par"]]
    sigtable = Table(sig, colWidths=[3*inch, 3*inch])
    sigtable.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), ('GRID', (0,0), (-1,-1), 0.5, colors.black)]))
    elements.append(sigtable)

    doc.build(elements)
    return filename
```
