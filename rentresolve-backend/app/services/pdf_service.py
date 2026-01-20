from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime

class PDFService:
    @staticmethod
    def generate_complaint_pack(issue_data: dict, complaint_kit: dict, user_data: dict) -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Custom Styles
        title_style = styles['Title']
        heading_style = styles['Heading2']
        normal_style = styles['Normal']
        code_style = ParagraphStyle('Code', parent=styles['Normal'], fontName='Courier', fontSize=8, backColor=colors.lightgrey)

        # 1. Title Page
        story.append(Paragraph("RentResolve Resolution Pack", title_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d')}", normal_style))
        story.append(Spacer(1, 24))

        # 2. Issue Summary Table
        story.append(Paragraph("1. Case Summary", heading_style))
        data = [
            ["Item", "Details"],
            ["Title", issue_data.get('title')],
            ["Tenant Name", user_data.get('full_name', 'N/A')],
            ["Phone", user_data.get('phone_number', 'N/A')],
            ["Location", issue_data.get('location')],
            ["Issue Type", issue_data.get('issue_type')],
            ["Date Reported", issue_data.get('created_at', '').split('T')[0]],
            ["Strength Score", f"{complaint_kit.get('complaint_strength_score', 'N/A')}/100"]
        ]
        t = Table(data, colWidths=[120, 400])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(t)
        story.append(Spacer(1, 24))

        # 3. Communications
        if complaint_kit:
            story.append(Paragraph("2. Official Communications", heading_style))
            
            story.append(Paragraph("<b>Email Draft (Subject: " + complaint_kit.get('email_subject', 'Complaint') + ")</b>", normal_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(complaint_kit.get('email_body', '').replace('\n', '<br/>'), normal_style))
            story.append(Spacer(1, 12))
            
            story.append(Paragraph("<b>WhatsApp Message</b>", normal_style))
            story.append(Spacer(1, 6))
            story.append(Paragraph(complaint_kit.get('whatsapp_message', '').replace('\n', '<br/>'), normal_style))
            story.append(Spacer(1, 24))

        # 4. Evidence Checklist
        if complaint_kit and complaint_kit.get('evidence_checklist'):
            story.append(Paragraph("3. Evidence Checklist", heading_style))
            for item in complaint_kit['evidence_checklist']:
                story.append(Paragraph(f"• {item}", normal_style))
            story.append(Spacer(1, 24))

        # 5. Timeline
        current_timeline = issue_data.get('timeline_events', [])
        if current_timeline:
            story.append(Paragraph("4. Case Timeline", heading_style))
            for event in current_timeline:
                date = event.get('date', '').split('T')[0]
                text = f"<b>{date}</b>: {event.get('title')} - {event.get('description')}"
                story.append(Paragraph(text, normal_style))
                story.append(Spacer(1, 6))

        doc.build(story)
        buffer.seek(0)
        return buffer
