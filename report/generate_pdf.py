"""PDF — 2021 plain academic paper style. Simple, grayscale, no fancy design."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image as RLImage, Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage

# 2021 style — academic, minimal color, Times-like
doc = SimpleDocTemplate("report/patient_navigation_report.pdf", pagesize=letter,
                         topMargin=1*inch, bottomMargin=1*inch,
                         leftMargin=1.25*inch, rightMargin=1.25*inch)
styles = getSampleStyleSheet()

def s(name, parent="Normal", **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

title_s  = s("T", fontSize=14, fontName="Times-Bold", textColor=colors.black,
              spaceAfter=4, alignment=TA_CENTER)
center_s = s("Ctr", fontSize=10, fontName="Times-Roman", textColor=colors.black,
              spaceAfter=3, alignment=TA_CENTER)
italic_s = s("It",  fontSize=9, fontName="Times-Italic", textColor=colors.HexColor("#444444"),
              spaceAfter=10, alignment=TA_CENTER)
h2_s     = s("H2", fontSize=10, fontName="Times-Bold", textColor=colors.black,
              spaceBefore=14, spaceAfter=5, textTransform="uppercase")
body_s   = s("Bd", fontSize=10, fontName="Times-Roman", leading=16,
              spaceAfter=8, alignment=TA_JUSTIFY)
caption_s= s("Cap", fontSize=8, fontName="Times-Italic", textColor=colors.HexColor("#555555"),
              spaceAfter=10, alignment=TA_CENTER)

story = []

# Header — academic paper style
story.append(Paragraph("Impact of Patient Navigation on Post-Discharge Outcomes:", title_s))
story.append(Paragraph("A Retrospective Propensity Score Matched Cohort Study", title_s))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Sai Manasa Adduru, MPH (Epidemiology), PharmD", center_s))
story.append(Paragraph("Department of Epidemiology, Kent State University", italic_s))
story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=10))

# Abstract box (plain border)
abstract_data = [[Paragraph(
    "<b>ABSTRACT</b><br/>"
    "<b>Background:</b> Hospital readmissions impose substantial burden on patients. Patient navigation "
    "programs may reduce post-discharge fragmentation, yet causal evidence is limited. "
    "<b>Methods:</b> Retrospective cohort (N=2,000). 1:1 PSM (caliper=0.02 SD), 555 matched pairs. "
    "Outcomes: 30-day readmission, 90-day ED visits, 180-day cost. Adjusted logistic regression, DiD, KM. "
    "<b>Results:</b> Navigated patients: 15.7% vs 24.0% readmission (OR=0.58 [0.43–0.79], p&lt;0.001); "
    "0.64 vs 0.80 ED visits (p=0.002); $3,329 lower cost (p&lt;0.001). NNT=12.1. "
    "<b>Conclusion:</b> Navigation significantly reduces readmission, ED use, and cost.",
    s("ABS", fontSize=9, fontName="Times-Roman", leading=14, alignment=TA_JUSTIFY))]]
t = Table(abstract_data, colWidths=[6*inch])
t.setStyle(TableStyle([
    ("BOX", (0,0),(-1,-1), 0.8, colors.black),
    ("BACKGROUND",(0,0),(-1,-1), colors.HexColor("#f7f7f7")),
    ("TOPPADDING",(0,0),(-1,-1), 8),("BOTTOMPADDING",(0,0),(-1,-1), 8),
    ("LEFTPADDING",(0,0),(-1,-1), 10),("RIGHTPADDING",(0,0),(-1,-1), 10),
]))
story.append(t); story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("INTRODUCTION", h2_s))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=6))
story.append(Paragraph("Approximately one in five Medicare patients is readmitted within 30 days of discharge. Patient navigation — trained advocates assisting patients through care transitions — has emerged as a promising intervention. This study uses propensity score matching to estimate the causal effect of navigation on post-discharge outcomes.", body_s))

story.append(Paragraph("METHODS", h2_s))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=6))
story.append(Paragraph("Retrospective cohort study, N=2,000 patients (593 navigated, 1,407 control). 1:1 nearest-neighbor PSM on 10 covariates (age, sex, CCI, prior admissions, index LOS, dual eligibility, CHF, COPD, diabetes, rurality). Caliper = 0.02 SD. Balance assessed by SMD. Primary outcomes: 30-day readmission (chi-square), 90-day ED visits (t-test), 180-day cost (t-test, DiD). Kaplan-Meier with log-rank. Python 3.9.", body_s))

# Results tables
story.append(Paragraph("RESULTS", h2_s))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=6))
story.append(Paragraph("All 10 covariates achieved SMD &lt;0.10 post-match. Primary outcomes:", body_s))

res_data = [
    ["Outcome","Navigated (n=555)","Control (n=555)","Effect","p"],
    ["30-day readmission","15.7%","24.0%","OR=0.58 [0.43–0.79]","<0.001"],
    ["90-day ED visits","0.64","0.80","Δ=−0.16","0.002"],
    ["180-day cost","$24,461","$27,790","Savings=$3,329","<0.001"],
    ["NNT","—","—","12.1 patients","—"],
]
t2 = Table(res_data, colWidths=[1.8*inch,1.2*inch,1.2*inch,1.6*inch,0.7*inch])
t2.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#333333")),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("FONTNAME",(0,0),(-1,0),"Times-Bold"),
    ("FONTSIZE",(0,0),(-1,-1),9),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#f0f0f0"),colors.white]),
    ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#aaaaaa")),
    ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
]))
story.append(t2); story.append(Spacer(1,0.12*inch))

# Figures
for fig_key, cap in [
    ("fig1_love_plot",   "Figure 1. Covariate balance before and after PSM. All post-match SMDs <0.10."),
    ("fig2_ps_distribution", "Figure 2. Propensity score distributions before and after matching."),
    ("fig3_outcomes",    "Figure 3. Primary outcomes — navigated vs control (matched cohort)."),
    ("fig4_kaplan_meier","Figure 4. Kaplan-Meier readmission-free survival (log-rank p<0.001)."),
]:
    story.append(Paragraph(cap.split(".")[0] + ".", h2_s))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=6))
    pil = PILImage.open(f"output/figures/{fig_key}.png")
    w,h = pil.size
    mw = 6.0*inch
    story.append(RLImage(f"output/figures/{fig_key}.png", width=mw, height=h*(mw/w)))
    story.append(Paragraph(cap, caption_s))

story.append(Paragraph("DISCUSSION", h2_s))
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=6))
story.append(Paragraph("This analysis demonstrates a 35% relative reduction in 30-day readmission and $3,329 in per-patient cost savings attributable to patient navigation. Balance across all 10 covariates and the adjusted OR of 0.58 confirm robustness. NNT of 12.1 compares favorably to many pharmacologic interventions. Limitations include potential unmeasured confounding and synthetic data generalizability.", body_s))

story.append(Paragraph("Software: Python 3.9 · pandas · scikit-learn · statsmodels · lifelines · matplotlib", s("Ft", fontSize=8, fontName="Times-Italic", textColor=colors.gray)))

doc.build(story)
print("PDF written — 2021 academic style")
