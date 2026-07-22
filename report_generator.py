import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

TELEMETRY_FILE = "final_telemetry.json"
OUTPUT_PDF = "Akanno_SOC_Executive_Report.pdf"

def generate_pdf_report():
    print("=" * 60)
    print("      AKANNO LABS - EXECUTIVE SOC REPORT GENERATOR")
    print("=" * 60 + "\n")

    # Load Telemetry
    if not os.path.exists(TELEMETRY_FILE):
        print(f"[❌] Error: Telemetry file '{TELEMETRY_FILE}' not found.")
        return

    with open(TELEMETRY_FILE, "r") as f:
        events = json.load(f)

    # Calculate Summary Metrics
    total_events = len(events)
    critical_count = sum(1 for e in events if e.get("severity", "").upper() == "CRITICAL")
    high_count = sum(1 for e in events if e.get("severity", "").upper() == "HIGH")
    medium_count = sum(1 for e in events if e.get("severity", "").upper() == "MEDIUM")
    info_count = sum(1 for e in events if e.get("severity", "").upper() == "INFO")

    # Initialize PDF Document
    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    # Custom Cyberpunk / Dark Executive Header Style
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor("#00F0FF"),
        spaceAfter=10
    )
    
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#A0A0A0"),
        spaceAfter=20
    )

    # Title & Metadata
    story.append(Paragraph("AKANNO SECURITY LABS — SOC INCIDENT REPORT", title_style))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC | <b>Scope:</b> Internal Telemetry Ingest Feed", meta_style))
    story.append(Spacer(1, 10))

    # Summary Statistics Table
    summary_data = [
        ["Total Events Logged", "Critical Threats", "High Severity", "Medium / Info"],
        [str(total_events), str(critical_count), str(high_count), str(medium_count + info_count)]
    ]
    
    summary_table = Table(summary_data, colWidths=[130, 130, 130, 130])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A1D24")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#00F0FF")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#242832")),
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333A48")),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # Event Breakdown Table
    story.append(Paragraph("<b>Recent High-Priority Security Events</b>", styles['Heading2']))
    story.append(Spacer(1, 8))

    table_data = [["Timestamp", "Event Type", "Severity", "Source IP", "Action Status"]]
    
    for evt in events[:15]:  # Display top 15 events
        sev = evt.get("severity", "INFO").upper()
        table_data.append([
            evt.get("timestamp", "N/A"),
            evt.get("event_type", "Unknown"),
            sev,
            evt.get("ip", "Internal"),
            "BLOCKED" if sev in ["CRITICAL", "HIGH"] else "ANALYZED"
        ])

    event_table = Table(table_data, colWidths=[110, 140, 70, 100, 100])
    event_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#334155")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#1E293B"), colors.HexColor("#0F172A")]),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#CBD5E1")),
    ]))

    story.append(event_table)

    # Build PDF
    doc.build(story)
    print(f"[✅] Executive PDF Report successfully generated: '{OUTPUT_PDF}'")

if __name__ == "__main__":
    generate_pdf_report()