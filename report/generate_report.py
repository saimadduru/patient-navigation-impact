"""
Generates a standalone HTML research report embedding all figures and results.
"""

import base64, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

figs = {
    "fig1": "output/figures/fig1_love_plot.png",
    "fig2": "output/figures/fig2_ps_distribution.png",
    "fig3": "output/figures/fig3_outcomes.png",
    "fig4": "output/figures/fig4_kaplan_meier.png",
}

imgs = {k: img_to_b64(v) for k, v in figs.items()}

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Impact of Patient Navigation on Post-Discharge Outcomes</title>
<style>
  :root {{
    --blue:  #1B4F8A;
    --teal:  #2AAFA4;
    --gray:  #6C757D;
    --light: #F0F4F8;
    --dark:  #1a1a2e;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #fff;
    color: #222;
    line-height: 1.65;
    font-size: 15px;
  }}
  header {{
    background: linear-gradient(135deg, var(--blue), var(--teal));
    color: white;
    padding: 48px 40px 40px;
    border-bottom: 4px solid var(--teal);
  }}
  header h1 {{ font-size: 1.75rem; font-weight: 700; margin-bottom: 8px; line-height: 1.3; }}
  header .meta {{ opacity: 0.85; font-size: 0.9rem; margin-top: 12px; }}
  header .badge {{
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.78rem;
    margin: 4px 4px 0 0;
  }}
  .container {{ max-width: 1000px; margin: 0 auto; padding: 40px 24px; }}
  h2 {{
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--blue);
    border-left: 4px solid var(--teal);
    padding-left: 12px;
    margin: 36px 0 16px;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }}
  h3 {{ font-size: 1rem; font-weight: 600; color: #333; margin: 20px 0 8px; }}
  p {{ margin-bottom: 12px; }}
  .abstract {{
    background: var(--light);
    border-left: 4px solid var(--teal);
    border-radius: 0 8px 8px 0;
    padding: 20px 24px;
    margin: 24px 0;
  }}
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 16px;
    margin: 24px 0;
  }}
  .kpi {{
    background: var(--light);
    border-radius: 10px;
    padding: 20px 16px;
    text-align: center;
    border-top: 3px solid var(--teal);
  }}
  .kpi .number {{
    font-size: 2rem;
    font-weight: 800;
    color: var(--blue);
    line-height: 1;
  }}
  .kpi .label {{ font-size: 0.8rem; color: var(--gray); margin-top: 6px; }}
  .kpi .sub {{ font-size: 0.75rem; color: #999; margin-top: 4px; }}
  figure {{ margin: 28px 0; }}
  figure img {{ width: 100%; border-radius: 8px; border: 1px solid #e8edf2; box-shadow: 0 2px 12px rgba(0,0,0,0.07); }}
  figcaption {{ font-size: 0.82rem; color: var(--gray); margin-top: 8px; font-style: italic; padding: 0 4px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; margin: 16px 0; }}
  th {{
    background: var(--blue);
    color: white;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 0.82rem;
    letter-spacing: 0.03em;
  }}
  td {{ padding: 9px 14px; border-bottom: 1px solid #e8edf2; }}
  tr:nth-child(even) td {{ background: var(--light); }}
  tr:last-child td {{ border-bottom: none; }}
  .highlight {{ color: var(--teal); font-weight: 700; }}
  .sig {{ color: #e63946; font-weight: 700; }}
  .methods-box {{
    background: var(--light);
    border-radius: 8px;
    padding: 20px 24px;
    margin: 16px 0;
    font-size: 0.88rem;
  }}
  .methods-box ul {{ padding-left: 18px; }}
  .methods-box li {{ margin-bottom: 6px; }}
  footer {{
    background: var(--dark);
    color: #aaa;
    text-align: center;
    padding: 24px;
    font-size: 0.82rem;
    margin-top: 48px;
  }}
  footer a {{ color: var(--teal); text-decoration: none; }}
  @media (max-width: 600px) {{
    header {{ padding: 28px 20px; }}
    .container {{ padding: 24px 16px; }}
    .kpi .number {{ font-size: 1.5rem; }}
  }}
</style>
</head>
<body>

<header>
  <h1>Impact of Patient Navigation on Post-Discharge Outcomes:<br>A Retrospective Propensity Score Matched Cohort Study</h1>
  <div class="meta">
    <strong>Sai Manasa Adduru</strong>, MPH (Epidemiology), PharmD &nbsp;|&nbsp; Kent State University
    <br>
    <span class="badge">Retrospective Cohort Study</span>
    <span class="badge">Propensity Score Matching</span>
    <span class="badge">Causal Inference</span>
    <span class="badge">Health Outcomes Research</span>
  </div>
</header>

<div class="container">

  <div class="abstract">
    <h3>Abstract</h3>
    <p><strong>Background:</strong> Patient navigation programs aim to reduce care fragmentation and improve outcomes after hospital discharge, yet rigorous evidence of their causal impact on utilization and cost remains limited.</p>
    <p><strong>Methods:</strong> We conducted a retrospective cohort study of 2,000 patients discharged from an acute care facility. Using 1:1 nearest-neighbor propensity score matching (caliper = 0.02 SD) on age, comorbidity burden, prior utilization, and social risk factors, we assembled a balanced cohort of 555 navigated and 555 control patients. Primary outcomes were 30-day readmission, 90-day emergency department visits, and 180-day total healthcare cost, assessed via adjusted logistic regression and difference-in-differences.</p>
    <p><strong>Results:</strong> After matching, navigated patients had significantly lower 30-day readmission (15.7% vs. 24.0%; RR 0.65; adjusted OR 0.58, 95% CI 0.43–0.79; p&lt;0.001), fewer 90-day ED visits (0.64 vs. 0.80; p=0.002), and $3,329 lower mean 180-day cost (p&lt;0.001). Number needed to treat was 12.1.</p>
    <p><strong>Conclusion:</strong> Patient navigation is associated with substantial reductions in readmission, ED utilization, and healthcare cost. These findings support investment in advocacy-based care coordination as a high-value intervention in complex patient populations.</p>
  </div>

  <!-- KPI strip -->
  <div class="kpi-grid">
    <div class="kpi">
      <div class="number">35%</div>
      <div class="label">Reduction in 30-Day Readmissions</div>
      <div class="sub">15.7% vs 24.0%  (p&lt;0.001)</div>
    </div>
    <div class="kpi">
      <div class="number">0.58</div>
      <div class="label">Adjusted Odds Ratio</div>
      <div class="sub">95% CI: 0.43–0.79</div>
    </div>
    <div class="kpi">
      <div class="number">$3,329</div>
      <div class="label">Cost Savings Per Patient</div>
      <div class="sub">180-day total cost (p&lt;0.001)</div>
    </div>
    <div class="kpi">
      <div class="number">12.1</div>
      <div class="label">Number Needed to Treat</div>
      <div class="sub">To prevent 1 readmission</div>
    </div>
  </div>

  <!-- Methods -->
  <h2>Methods</h2>
  <div class="methods-box">
    <ul>
      <li><strong>Study Design:</strong> Retrospective observational cohort study with propensity score matching</li>
      <li><strong>Cohort:</strong> N=2,000 adult patients with index hospital admission; 593 received patient navigation post-discharge, 1,407 received usual care</li>
      <li><strong>Matching:</strong> 1:1 nearest-neighbor PSM with caliper of 0.02 SD on estimated propensity score; yielding 555 matched pairs</li>
      <li><strong>Propensity Model:</strong> Logistic regression on age, sex, Charlson Comorbidity Index, prior admissions, index LOS, dual eligibility, CHF, COPD, diabetes, rurality (c-statistic = 0.71)</li>
      <li><strong>Balance Assessment:</strong> Standardized mean differences (SMD) before and after matching; balance achieved at SMD &lt;0.10 for all 10 covariates</li>
      <li><strong>Statistical Methods:</strong> Chi-square test, independent t-test, adjusted logistic regression, Kaplan-Meier with log-rank test, difference-in-differences</li>
      <li><strong>Software:</strong> Python 3.9 (pandas, scikit-learn, statsmodels, lifelines, matplotlib)</li>
    </ul>
  </div>

  <!-- Figure 1 -->
  <h2>Covariate Balance</h2>
  <figure>
    <img src="data:image/png;base64,{imgs['fig1']}" alt="Love plot — covariate balance before and after matching">
    <figcaption>Figure 1. Love plot showing standardized mean differences (SMD) for all covariates before and after propensity score matching. All covariates achieved SMD &lt;0.10 post-match, indicating adequate balance.</figcaption>
  </figure>

  <!-- Figure 2 -->
  <h2>Propensity Score Distribution</h2>
  <figure>
    <img src="data:image/png;base64,{imgs['fig2']}" alt="Propensity score distribution before and after matching">
    <figcaption>Figure 2. Distribution of estimated propensity scores for navigated and control groups before (left) and after (right) 1:1 nearest-neighbor matching. Post-match distributions show strong overlap, confirming positivity assumption.</figcaption>
  </figure>

  <!-- Table 2 -->
  <h2>Post-Match Cohort Characteristics</h2>
  <table>
    <tr><th>Variable</th><th>Navigated (n=555)</th><th>Control (n=555)</th><th>SMD</th></tr>
    <tr><td>Age, mean (SD)</td><td>66.2 (11.9)</td><td>66.5 (11.5)</td><td class="highlight">0.023</td></tr>
    <tr><td>Female, %</td><td>51.2%</td><td>51.7%</td><td class="highlight">0.011</td></tr>
    <tr><td>CCI, mean (SD)</td><td>2.18 (1.35)</td><td>2.13 (1.38)</td><td class="highlight">0.034</td></tr>
    <tr><td>Prior admissions (12m), mean</td><td>1.41</td><td>1.43</td><td class="highlight">0.017</td></tr>
    <tr><td>Index LOS, mean days</td><td>4.21</td><td>4.22</td><td class="highlight">0.007</td></tr>
    <tr><td>Dual eligible (Medicare+Medicaid), %</td><td>29.2%</td><td>30.1%</td><td class="highlight">0.024</td></tr>
    <tr><td>CHF, %</td><td>31.9%</td><td>31.2%</td><td class="highlight">0.023</td></tr>
    <tr><td>COPD, %</td><td>30.3%</td><td>31.2%</td><td class="highlight">0.016</td></tr>
    <tr><td>Diabetes, %</td><td>35.3%</td><td>39.1%</td><td class="highlight">0.071</td></tr>
    <tr><td>Rural, %</td><td>19.1%</td><td>17.1%</td><td class="highlight">0.061</td></tr>
  </table>
  <p style="font-size:0.82rem; color:#888;">All SMD values &lt;0.10 indicate well-balanced cohorts. CCI = Charlson Comorbidity Index; LOS = Length of stay; CHF = Congestive heart failure; COPD = Chronic obstructive pulmonary disease.</p>

  <!-- Figure 3 -->
  <h2>Primary Outcomes</h2>
  <figure>
    <img src="data:image/png;base64,{imgs['fig3']}" alt="Primary outcomes comparison">
    <figcaption>Figure 3. Comparison of primary outcomes between navigated and control patients in the propensity score matched cohort. Asterisks denote statistical significance: *** p&lt;0.001, ** p&lt;0.01.</figcaption>
  </figure>

  <table>
    <tr><th>Outcome</th><th>Navigated</th><th>Control</th><th>Effect Size</th><th>p-value</th></tr>
    <tr>
      <td>30-day readmission rate</td>
      <td class="highlight">15.7%</td>
      <td>24.0%</td>
      <td>RR 0.65 &nbsp;|&nbsp; ARR 8.3% &nbsp;|&nbsp; NNT 12.1</td>
      <td class="sig">0.0007</td>
    </tr>
    <tr>
      <td>Adjusted OR (30-day readmit)</td>
      <td colspan="2">OR 0.58</td>
      <td>95% CI: 0.43–0.79</td>
      <td class="sig">0.0006</td>
    </tr>
    <tr>
      <td>90-day ED visits, mean</td>
      <td class="highlight">0.64</td>
      <td>0.80</td>
      <td>Δ −0.16 visits/patient</td>
      <td class="sig">0.0020</td>
    </tr>
    <tr>
      <td>180-day total cost, mean</td>
      <td class="highlight">$24,461</td>
      <td>$27,790</td>
      <td>Savings $3,329/patient</td>
      <td class="sig">&lt;0.0001</td>
    </tr>
  </table>

  <!-- Figure 4 -->
  <h2>Kaplan-Meier: Time to 30-Day Readmission</h2>
  <figure>
    <img src="data:image/png;base64,{imgs['fig4']}" alt="Kaplan-Meier survival curves">
    <figcaption>Figure 4. Kaplan-Meier readmission-free survival curves for navigated vs. control patients in the matched cohort. Shaded regions represent 95% confidence intervals. Log-rank test confirms significantly longer readmission-free survival in the navigated group.</figcaption>
  </figure>

  <!-- Discussion -->
  <h2>Discussion</h2>
  <p>
    This retrospective propensity score matched analysis provides evidence that structured patient navigation significantly reduces 30-day readmission, emergency department utilization, and 180-day healthcare costs. The magnitude of effect — a 35% relative risk reduction in readmission and $3,329 in per-patient savings — is consistent with peer-reviewed literature on care coordination and case management interventions in high-risk populations.
  </p>
  <p>
    Critically, covariate balance was achieved across all 10 measured confounders (all post-match SMD &lt;0.10), strengthening the validity of group comparisons. The adjusted odds ratio of 0.58 (95% CI 0.43–0.79) confirms the readmission benefit is robust to measured confounding. The Kaplan-Meier analysis illustrates that the survival benefit emerged within the first week post-discharge and was sustained throughout the 30-day observation window.
  </p>
  <p>
    <strong>Implications:</strong> For organizations deploying patient advocacy models, these findings quantify return on investment and support evidence-based expansion of navigation programs, particularly in dual-eligible, high-comorbidity populations where fragmentation risk is greatest.
  </p>
  <p>
    <strong>Limitations:</strong> As with all retrospective designs, unmeasured confounding (e.g., patient motivation, social support) may persist despite matching. Generalizability is subject to the population characteristics of the source data. Prospective randomized evaluation would provide stronger causal evidence.
  </p>

  <h2>Conclusion</h2>
  <p>
    Patient navigation is associated with a <strong>35% reduction in 30-day readmission</strong>, <strong>20% fewer 90-day ED visits</strong>, and <strong>$3,329 in per-patient cost savings</strong> in a propensity score matched retrospective cohort. These findings have direct relevance for health systems, payers, and advocacy organizations seeking to demonstrate the measurable value of coordinated, patient-centered care.
  </p>

</div>

<footer>
  <p>
    Sai Manasa Adduru, MPH (Epidemiology), PharmD &nbsp;|&nbsp;
    <a href="mailto:saimanasaadduru@gmail.com">saimanasaadduru@gmail.com</a>
  </p>
  <p style="margin-top:6px; font-size:0.75rem;">
    Analysis conducted in Python 3.9 · pandas · scikit-learn · lifelines · statsmodels · matplotlib
  </p>
</footer>

</body>
</html>"""

with open("report/impact_analysis_report.html", "w") as f:
    f.write(html)

print("Report written to report/impact_analysis_report.html")
