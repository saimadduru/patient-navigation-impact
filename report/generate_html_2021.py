"""
2021-era HTML report — plain academic paper style.
Simple, clean, no gradients, no modern CSS tricks.
Looks like a grad student research write-up.
"""
import base64, os

def b64(p):
    with open(p,"rb") as f: return base64.b64encode(f.read()).decode()

imgs = {k: b64(f"output/figures/{k}.png") for k in
        ["fig1_love_plot","fig2_ps_distribution","fig3_outcomes","fig4_kaplan_meier"]}

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Patient Navigation Impact Study</title>
<style>
  body {{ font-family: "Times New Roman", Times, serif; font-size: 14px;
          color: #111; background: #fff; margin: 0; padding: 0; line-height: 1.7; }}
  .page {{ max-width: 860px; margin: 0 auto; padding: 48px 40px; }}
  h1 {{ font-size: 1.5rem; text-align: center; margin-bottom: 6px; font-weight: bold; }}
  .authors {{ text-align: center; font-size: 0.95rem; color: #333; margin-bottom: 4px; }}
  .affil {{ text-align: center; font-size: 0.85rem; color: #555; font-style: italic; margin-bottom: 20px; }}
  hr {{ border: none; border-top: 1px solid #999; margin: 20px 0; }}
  h2 {{ font-size: 1.05rem; font-weight: bold; text-transform: uppercase;
        letter-spacing: 0.05em; margin-top: 28px; margin-bottom: 8px; border-bottom: 1px solid #ccc; padding-bottom: 3px; }}
  h3 {{ font-size: 1rem; font-weight: bold; margin-top: 16px; margin-bottom: 4px; }}
  p {{ margin-bottom: 10px; text-align: justify; }}
  .abstract-box {{ border: 1px solid #bbb; padding: 14px 18px; margin: 18px 0;
                   background: #fafafa; font-size: 0.92rem; }}
  .keywords {{ font-size: 0.88rem; color: #444; margin-top: 6px; }}
  figure {{ margin: 20px 0; text-align: center; }}
  figure img {{ max-width: 100%; border: 1px solid #ccc; }}
  figcaption {{ font-size: 0.82rem; color: #444; margin-top: 6px;
                text-align: left; font-style: italic; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; margin: 14px 0; }}
  th {{ background: #444; color: white; padding: 7px 10px; text-align: left; font-size: 0.85rem; }}
  td {{ padding: 7px 10px; border-bottom: 1px solid #ddd; }}
  tr:nth-child(even) td {{ background: #f5f5f5; }}
  .footnote {{ font-size: 0.78rem; color: #666; border-top: 1px solid #ddd; margin-top: 32px; padding-top: 10px; }}
</style>
</head>
<body>
<div class="page">
  <h1>Impact of Patient Navigation on Post-Discharge Outcomes:<br>
  A Retrospective Propensity Score Matched Cohort Study</h1>
  <p class="authors">Sai Manasa Adduru, MPH (Epidemiology), PharmD</p>
  <p class="affil">Kent State University, College of Public Health · Department of Epidemiology</p>
  <hr>

  <div class="abstract-box">
    <h3>Abstract</h3>
    <p><strong>Background:</strong> Hospital readmissions impose substantial burden on patients and healthcare systems. Patient navigation programs may reduce fragmentation of post-discharge care, yet rigorous evidence of causal impact remains limited.</p>
    <p><strong>Methods:</strong> Retrospective cohort study of 2,000 patients. 1:1 nearest-neighbor propensity score matching (caliper = 0.02 SD) yielded 555 matched pairs. Primary outcomes: 30-day readmission, 90-day emergency department visits, 180-day total cost. Adjusted by logistic regression; difference-in-differences for cost; Kaplan-Meier for time-to-event.</p>
    <p><strong>Results:</strong> Navigated patients had significantly lower 30-day readmission (15.7% vs 24.0%, RR=0.65, OR=0.58 [95% CI 0.43–0.79], p&lt;0.001), fewer 90-day ED visits (0.64 vs 0.80, p=0.002), and $3,329 lower 180-day cost (p&lt;0.001). Number needed to treat = 12.1.</p>
    <p><strong>Conclusion:</strong> Patient navigation is associated with substantial reductions in readmission, ED utilization, and cost. Findings support expansion of advocacy-based care coordination models.</p>
    <p class="keywords"><strong>Keywords:</strong> patient navigation, readmission, propensity score matching, health outcomes, causal inference</p>
  </div>

  <h2>Introduction</h2>
  <p>Approximately one in five Medicare patients is readmitted within 30 days of hospital discharge, at an estimated annual cost of $26 billion. Patient navigation programs — in which trained advocates assist patients in navigating care transitions, scheduling follow-up, and addressing social needs — have emerged as a promising intervention, yet the evidence base from rigorous observational studies remains thin.</p>
  <p>This study uses propensity score matching to estimate the causal effect of patient navigation on post-discharge outcomes in a retrospective cohort, controlling for clinical and demographic confounders.</p>

  <h2>Methods</h2>
  <p><strong>Study Design.</strong> Retrospective cohort study with 1:1 nearest-neighbor propensity score matching.</p>
  <p><strong>Population.</strong> 2,000 adult patients (≥18 years) with acute care index admission. 593 received patient navigation post-discharge; 1,407 received usual care.</p>
  <p><strong>Propensity Score Model.</strong> Logistic regression on age, sex, Charlson Comorbidity Index (CCI), prior 12-month admissions, index length of stay, dual eligibility, CHF, COPD, diabetes, and rurality (c-statistic = 0.71). Matching caliper set at 0.02 SD of the estimated PS.</p>
  <p><strong>Balance Assessment.</strong> Standardized mean differences (SMD) computed pre- and post-match. Balance defined as SMD &lt;0.10.</p>
  <p><strong>Statistical Analysis.</strong> Chi-square (readmission), t-test (ED visits, cost), adjusted logistic regression, difference-in-differences (cost), Kaplan-Meier with log-rank test. Analysis conducted in Python 3.9.</p>

  <h2>Results</h2>
  <h3>Cohort Characteristics and Balance</h3>
  <figure>
    <img src="data:image/png;base64,{imgs['fig1_love_plot']}" alt="Love plot">
    <figcaption>Figure 1. Standardized mean differences for all covariates before and after propensity score matching. All post-match SMDs &lt;0.10, indicating adequate balance.</figcaption>
  </figure>
  <figure>
    <img src="data:image/png;base64,{imgs['fig2_ps_distribution']}" alt="PS distribution">
    <figcaption>Figure 2. Propensity score distributions for navigated and control groups before and after 1:1 matching.</figcaption>
  </figure>

  <h3>Primary Outcomes</h3>
  <table>
    <tr><th>Outcome</th><th>Navigated (n=555)</th><th>Control (n=555)</th><th>Effect Estimate</th><th>p-value</th></tr>
    <tr><td>30-day readmission</td><td>15.7%</td><td>24.0%</td><td>RR=0.65; OR=0.58 [0.43–0.79]</td><td>&lt;0.001</td></tr>
    <tr><td>90-day ED visits (mean)</td><td>0.64</td><td>0.80</td><td>Δ=−0.16 visits/patient</td><td>0.002</td></tr>
    <tr><td>180-day total cost (mean)</td><td>$24,461</td><td>$27,790</td><td>Savings=$3,329/patient</td><td>&lt;0.001</td></tr>
    <tr><td>Number needed to treat</td><td colspan="4">12.1 patients to prevent 1 readmission</td></tr>
  </table>
  <figure>
    <img src="data:image/png;base64,{imgs['fig3_outcomes']}" alt="Primary outcomes">
    <figcaption>Figure 3. Primary outcomes comparison in propensity score matched cohort.</figcaption>
  </figure>
  <figure>
    <img src="data:image/png;base64,{imgs['fig4_kaplan_meier']}" alt="Kaplan-Meier">
    <figcaption>Figure 4. Kaplan-Meier readmission-free survival curves with 95% confidence intervals. Log-rank test confirms significantly longer survival in navigated group.</figcaption>
  </figure>

  <h2>Discussion</h2>
  <p>This propensity score matched analysis demonstrates that patient navigation is associated with a 35% relative reduction in 30-day readmission, fewer emergency department visits, and approximately $3,329 in per-patient cost savings over 180 days. Balance was achieved across all 10 measured covariates, and the adjusted odds ratio of 0.58 (95% CI 0.43–0.79) confirms robustness to measured confounding.</p>
  <p>These findings are consistent with the broader literature on care coordination interventions and suggest that structured patient navigation programs represent a high-value investment, particularly in dual-eligible and high-comorbidity populations where care fragmentation risk is greatest. The number needed to treat of 12.1 compares favorably to many pharmacologic interventions in similar populations.</p>
  <p><strong>Limitations.</strong> As with all observational studies, unmeasured confounding may persist. Generalizability is subject to the source population characteristics. Prospective evaluation would strengthen causal inference.</p>

  <h2>Conclusion</h2>
  <p>Patient navigation is associated with meaningful improvements in post-discharge outcomes. A 35% reduction in readmissions, 20% fewer ED visits, and $3,329 in per-patient savings support investment in advocacy-based care coordination as a clinically and economically justified intervention.</p>

  <div class="footnote">
    <p>Data: Synthetic cohort generated using NumPy (seed=42) to mirror real-world claims data distributions. Methods follow published PSM guidance (Austin 2011; Rosenbaum & Rubin 1983).</p>
    <p>Software: Python 3.9 · pandas · scikit-learn · statsmodels · lifelines · matplotlib</p>
    <p>Contact: saimanasaadduru@gmail.com · GitHub: github.com/saimadduru/patient-navigation-impact</p>
  </div>
</div>
</body></html>"""

with open("report/impact_analysis_report.html","w") as f: f.write(html)
print("HTML written — 2021 academic style")
