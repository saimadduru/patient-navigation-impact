"""Generates PDF research brief for Patient Navigation Impact study."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image as RLImage, Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage

DARK_BLUE = colors.HexColor("#1B4F8A")
TEAL      = colors.HexColor("#2AAFA4")
LIGHT_BG  = colors.HexColor("#F0F4F8")
RED_C     = colors.HexColor("#C0392B")

doc = SimpleDocTemplate("report/patient_navigation_report.pdf", pagesize=letter,
                         topMargin=0.6*inch, bottomMargin=0.6*inch,
                         leftMargin=0.75*inch, rightMargin=0.75*inch)
styles = getSampleStyleSheet()

def s(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

title_s   = s("T", fontSize=15, fontName="Helvetica-Bold", textColor=DARK_BLUE, spaceAfter=6)
sub_s     = s("S", fontSize=10, textColor=TEAL, fontName="Helvetica", spaceAfter=4)
author_s  = s("A", fontSize=9,  textColor=colors.gray, fontName="Helvetica", spaceAfter=12)
h2_s      = s("H", fontSize=11, fontName="Helvetica-Bold", textColor=DARK_BLUE, spaceBefore=14, spaceAfter=6)
body_s    = s("B", fontSize=9,  fontName="Helvetica", leading=14, spaceAfter=8, alignment=TA_JUSTIFY)
caption_s = s("C", fontSize=8,  fontName="Helvetica-Oblique", textColor=colors.gray, spaceAfter=10, alignment=TA_CENTER)

story = []
story.append(Paragraph("Impact of Patient Navigation on Post-Discharge Outcomes:", title_s))
story.append(Paragraph("A Retrospective Propensity Score Matched Cohort Study", title_s))
story.append(HRFlowable(width="100%", thickness=2, color=TEAL, spaceAfter=6))
story.append(Paragraph("Sai Manasa Adduru, MPH (Epidemiology), PharmD", author_s))
story.append(Paragraph("Health Outcomes Research · Impact Analytics", sub_s))
story.append(Paragraph("Methods: Propensity Score Matching · Difference-in-Differences · Kaplan-Meier · Causal Inference · SQL", sub_s))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=10))

story.append(Paragraph("ABSTRACT", h2_s))
story.append(Paragraph("<b>Background:</b> Patient navigation programs aim to reduce care fragmentation after hospital discharge. Rigorous evidence of causal impact on utilization and cost remains limited. <b>Methods:</b> Retrospective cohort study of 2,000 patients. 1:1 nearest-neighbor propensity score matching (caliper=0.02 SD) on 10 covariates; yielding 555 matched pairs. Outcomes: 30-day readmission, 90-day ED visits, 180-day total cost. Adjusted logistic regression, difference-in-differences, Kaplan-Meier. <b>Results:</b> Navigated patients had significantly lower 30-day readmission (15.7% vs 24.0%; RR 0.65; adjusted OR 0.58, 95% CI 0.43–0.79; p&lt;0.001), fewer ED visits (0.64 vs 0.80; p=0.002), and $3,329 lower 180-day cost (p&lt;0.001). NNT=12.1. <b>Conclusion:</b> Patient navigation reduces readmission, ED utilization, and cost in a well-balanced propensity-matched cohort.", body_s))

kpi_data = [
    ["Outcome","Navigated","Control","Effect","p-value"],
    ["30-Day Readmission","15.7%","24.0%","RR 0.65  NNT 12.1","0.0007"],
    ["Adjusted OR (readmission)","OR 0.58","—","95% CI: 0.43–0.79","0.0006"],
    ["90-Day ED Visits","0.64","0.80","Δ −0.16 visits","0.0020"],
    ["180-Day Total Cost","$24,461","$27,790","Savings $3,329/pt","<0.0001"],
]
t = Table(kpi_data, colWidths=[1.8*inch,1.1*inch,1.0*inch,1.8*inch,0.85*inch])
t.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),DARK_BLUE),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),8),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[LIGHT_BG,colors.white]),
    ("GRID",(0,0),(-1,-1),0.3,colors.lightgrey),
    ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
]))
story.append(t); story.append(Spacer(1, 0.15*inch))

for fig_key, sec, caption in [
    ("fig1_love_plot","COVARIATE BALANCE — LOVE PLOT",
     "Figure 1. Love plot showing SMDs before and after matching. All 10 covariates achieved SMD<0.10 post-match."),
    ("fig2_ps_distribution","PROPENSITY SCORE DISTRIBUTION",
     "Figure 2. PS distributions before (A) and after (B) matching. Strong overlap confirms positivity assumption."),
    ("fig3_outcomes","PRIMARY OUTCOMES",
     "Figure 3. 30-day readmission, 90-day ED visits, and 180-day cost — navigated vs control (matched cohort). ***p<0.001."),
    ("fig4_kaplan_meier","KAPLAN-MEIER: TIME TO READMISSION",
     "Figure 4. Readmission-free survival curves. Navigated patients show significantly longer survival (log-rank p<0.001)."),
]:
    story.append(Paragraph(sec, h2_s))
    img_path = f"output/figures/{fig_key}.png"
    pil = PILImage.open(img_path)
    w_px, h_px = pil.size
    max_w = 6.5 * inch
    img = RLImage(img_path, width=max_w, height=h_px * (max_w / w_px))
    story.append(img); story.append(Paragraph(caption, caption_s))

story.append(Paragraph("DISCUSSION", h2_s))
story.append(Paragraph("This PSM analysis provides evidence that structured patient navigation reduces 30-day readmission (35% relative reduction), ED utilization, and 180-day cost. Covariate balance was achieved across all 10 covariates (all SMD<0.10). The adjusted OR of 0.58 confirms the effect is robust to measured confounding. The Kaplan-Meier analysis shows the survival benefit emerges within the first week post-discharge. For organizations deploying patient advocacy models, these findings quantify ROI and support evidence-based expansion to dual-eligible, high-comorbidity populations.", body_s))

doc.build(story)
print("PDF report written to report/patient_navigation_report.pdf")
