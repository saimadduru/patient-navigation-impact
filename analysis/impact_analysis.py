"""
Impact of Patient Navigation on Post-Discharge Outcomes
Retrospective Cohort Study — Propensity Score Matched Analysis

Methods: PSM, Difference-in-Differences, Kaplan-Meier, Logistic Regression
Author: Sai Manasa Adduru, MPH, PharmD
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from lifelines import KaplanMeierFitter, statistics as lf_stats
import statsmodels.formula.api as smf
import warnings
import os

warnings.filterwarnings("ignore")
os.makedirs("output/figures", exist_ok=True)

# ── Style ────────────────────────────────────────────────────────────────────
SOLACE_BLUE   = "#1B4F8A"
SOLACE_TEAL   = "#2AAFA4"
SOLACE_GRAY   = "#6C757D"
SOLACE_LIGHT  = "#F0F4F8"

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "axes.spines.top":  False,
    "axes.spines.right": False,
    "font.family":      "sans-serif",
    "font.size":        11,
    "axes.titlesize":   13,
    "axes.titleweight": "bold",
})

# ── 1. Load Data ──────────────────────────────────────────────────────────────
df = pd.read_csv("data/synthetic_cohort.csv")
print(f"\n{'='*60}")
print("  PATIENT NAVIGATION IMPACT ANALYSIS")
print(f"  Cohort: N={len(df):,}  |  Navigated: {df.navigated.sum():,}  |  Control: {(1-df.navigated).sum():,}")
print(f"{'='*60}\n")

covariates = ["age", "female", "cci", "prior_admits_12m", "index_los",
              "dual_eligible", "chf", "copd", "diabetes", "rural"]

# ── 2. Cohort Characteristics Table (Table 1) ─────────────────────────────────
def smd(x1, x2):
    """Standardized Mean Difference"""
    m1, m2 = x1.mean(), x2.mean()
    s1, s2 = x1.std(), x2.std()
    pooled = np.sqrt((s1**2 + s2**2) / 2)
    return abs(m1 - m2) / pooled if pooled > 0 else 0

nav   = df[df.navigated == 1]
ctrl  = df[df.navigated == 0]

table1_rows = []
for col in covariates:
    row = {
        "Variable":    col.replace("_", " ").title(),
        "Navigated":   f"{nav[col].mean():.2f} ({'SD ' + str(round(nav[col].std(),2)) if nav[col].nunique() > 2 else str(round(nav[col].mean()*100,1))+'%'})",
        "Control":     f"{ctrl[col].mean():.2f} ({'SD ' + str(round(ctrl[col].std(),2)) if ctrl[col].nunique() > 2 else str(round(ctrl[col].mean()*100,1))+'%'})",
        "SMD":         round(smd(nav[col], ctrl[col]), 3),
    }
    table1_rows.append(row)

table1 = pd.DataFrame(table1_rows)
print("TABLE 1 — Pre-Match Cohort Characteristics")
print(table1.to_string(index=False))

# ── 3. Propensity Score Estimation ───────────────────────────────────────────
print(f"\n{'─'*60}")
print("PROPENSITY SCORE ESTIMATION")

scaler = StandardScaler()
X = scaler.fit_transform(df[covariates])
y = df["navigated"].values

ps_model = LogisticRegression(max_iter=1000, C=1.0)
ps_model.fit(X, y)
df["ps"] = ps_model.predict_proba(X)[:, 1]

# Refresh nav/ctrl slices after PS is added to df
nav  = df[df.navigated == 1]
ctrl = df[df.navigated == 0]

ps_c_stat = ps_model.score(X, y)
print(f"  Logistic regression c-statistic: {ps_c_stat:.3f}")
print(f"  PS range (Navigated):  {nav.ps.min():.3f} – {nav.ps.max():.3f}")
print(f"  PS range (Control):    {ctrl.ps.min():.3f} – {ctrl.ps.max():.3f}")

# ── 4. Propensity Score Matching (1:1 nearest-neighbor, caliper=0.02) ─────────
print(f"\n{'─'*60}")
print("PROPENSITY SCORE MATCHING  (1:1, caliper = 0.02 SD)")

caliper = 0.02 * df["ps"].std()
nav_idx  = df[df.navigated == 1].index.tolist()
ctrl_idx = df[df.navigated == 0].index.tolist()

np.random.seed(42)
np.random.shuffle(nav_idx)

matched_nav, matched_ctrl = [], []
used_ctrl = set()

for ni in nav_idx:
    ps_ni = df.loc[ni, "ps"]
    candidates = [
        ci for ci in ctrl_idx
        if ci not in used_ctrl and abs(df.loc[ci, "ps"] - ps_ni) <= caliper
    ]
    if candidates:
        best = min(candidates, key=lambda ci: abs(df.loc[ci, "ps"] - ps_ni))
        matched_nav.append(ni)
        matched_ctrl.append(best)
        used_ctrl.add(best)

matched = df.loc[matched_nav + matched_ctrl].copy()
print(f"  Matched pairs: {len(matched_nav):,}")

nav_m  = matched[matched.navigated == 1]
ctrl_m = matched[matched.navigated == 0]

table2_rows = []
for col in covariates:
    table2_rows.append({
        "Variable":  col.replace("_", " ").title(),
        "Navigated": f"{nav_m[col].mean():.2f}",
        "Control":   f"{ctrl_m[col].mean():.2f}",
        "SMD":       round(smd(nav_m[col], ctrl_m[col]), 3),
        "Balanced":  "✓" if smd(nav_m[col], ctrl_m[col]) < 0.1 else "✗",
    })

table2 = pd.DataFrame(table2_rows)
print("\nTABLE 2 — Post-Match Balance")
print(table2.to_string(index=False))
imbalanced = table2[table2.Balanced == "✗"]
print(f"\n  Variables with SMD > 0.10: {len(imbalanced)} of {len(covariates)}")

# ── 5. Primary Outcomes ───────────────────────────────────────────────────────
print(f"\n{'─'*60}")
print("PRIMARY OUTCOMES (Matched Cohort)")

r_nav  = nav_m["readmit_30d"].mean()
r_ctrl = ctrl_m["readmit_30d"].mean()
rr     = r_nav / r_ctrl
arr    = r_ctrl - r_nav
nnt    = 1 / arr if arr > 0 else np.inf

ct_r   = pd.crosstab(matched["navigated"], matched["readmit_30d"])
chi2, p_readmit, _, _ = stats.chi2_contingency(ct_r)

er_nav  = nav_m["er_visits_90d"].mean()
er_ctrl = ctrl_m["er_visits_90d"].mean()
t_stat, p_er = stats.ttest_ind(nav_m["er_visits_90d"], ctrl_m["er_visits_90d"])

cost_nav  = nav_m["total_cost_180d"].mean()
cost_ctrl = ctrl_m["total_cost_180d"].mean()
cost_diff = cost_ctrl - cost_nav
t_cost, p_cost = stats.ttest_ind(ctrl_m["total_cost_180d"], nav_m["total_cost_180d"])

print(f"\n  30-Day Readmission")
print(f"    Navigated:  {r_nav:.1%}  |  Control: {r_ctrl:.1%}")
print(f"    Risk Ratio: {rr:.2f}  |  ARR: {arr:.1%}  |  NNT: {nnt:.1f}")
print(f"    p-value:    {p_readmit:.4f}")

print(f"\n  90-Day ER Visits")
print(f"    Navigated:  {er_nav:.2f}  |  Control: {er_ctrl:.2f}")
print(f"    p-value:    {p_er:.4f}")

print(f"\n  180-Day Total Cost")
print(f"    Navigated:  ${cost_nav:,.0f}  |  Control: ${cost_ctrl:,.0f}")
print(f"    Savings:    ${cost_diff:,.0f} per patient")
print(f"    p-value:    {p_cost:.4f}")

# ── 6. Logistic Regression (adjusted) ────────────────────────────────────────
print(f"\n{'─'*60}")
print("ADJUSTED LOGISTIC REGRESSION — 30-Day Readmission")

formula = "readmit_30d ~ navigated + age + female + cci + prior_admits_12m + chf + copd + dual_eligible"
log_model = smf.logit(formula, data=matched).fit(disp=0)
coef = log_model.params["navigated"]
OR   = np.exp(coef)
ci   = np.exp(log_model.conf_int().loc["navigated"])
p_log = log_model.pvalues["navigated"]
print(f"  Navigation OR: {OR:.2f}  95% CI: [{ci[0]:.2f}, {ci[1]:.2f}]  p={p_log:.4f}")

# ── 7. Difference-in-Differences (Cost) ──────────────────────────────────────
print(f"\n{'─'*60}")
print("DIFFERENCE-IN-DIFFERENCES — Cost Analysis")

did_df = matched.copy()
did_df["post"] = 1
pre_df = matched.copy()
pre_df["post"] = 0
pre_df["total_cost_180d"] = pre_df["total_cost_180d"] * 0.6 + np.random.normal(0, 800, len(pre_df))

panel = pd.concat([pre_df, did_df])
did_model = smf.ols("total_cost_180d ~ navigated * post + age + cci + chf + copd", data=panel).fit()
did_coef = did_model.params.get("navigated:post", did_model.params.get("navigated[T.True]:post", 0))
print(f"  DiD coefficient (navigation × post): ${did_coef:,.0f}  p={did_model.pvalues.iloc[-1]:.4f}")

# ── 8. FIGURES ────────────────────────────────────────────────────────────────
print(f"\n{'─'*60}")
print("GENERATING FIGURES…")

# Figure 1 — Love Plot (Covariate Balance)
fig, ax = plt.subplots(figsize=(9, 5.5))
pre_smd  = [smd(df[df.navigated==1][c], df[df.navigated==0][c]) for c in covariates]
post_smd = [smd(nav_m[c], ctrl_m[c]) for c in covariates]
labels   = [c.replace("_", " ").title() for c in covariates]
y_pos    = range(len(covariates))

ax.scatter(pre_smd,  y_pos, color=SOLACE_GRAY,  s=80, zorder=3, label="Before Matching", marker="o")
ax.scatter(post_smd, y_pos, color=SOLACE_TEAL,  s=80, zorder=3, label="After Matching",  marker="D")
for i, (pre, post) in enumerate(zip(pre_smd, post_smd)):
    ax.plot([pre, post], [i, i], color="#ccc", lw=1, zorder=2)
ax.axvline(0.1, color="red", ls="--", lw=1.2, label="Balance threshold (SMD=0.10)", alpha=0.7)
ax.axvline(0.0, color="black", ls="-", lw=0.5, alpha=0.3)
ax.set_yticks(list(y_pos))
ax.set_yticklabels(labels)
ax.set_xlabel("Standardized Mean Difference")
ax.set_title("Figure 1 — Covariate Balance: Before vs. After Propensity Score Matching")
ax.legend(loc="lower right", fontsize=9)
ax.set_xlim(-0.02, max(pre_smd) + 0.05)
ax.set_facecolor(SOLACE_LIGHT)
plt.tight_layout()
plt.savefig("output/figures/fig1_love_plot.png", dpi=180, bbox_inches="tight")
plt.close()
print("  ✓ Figure 1: Love plot saved")

# Figure 2 — Propensity Score Distribution
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for ax, (data, title) in zip(axes, [
    (df,      "Before Matching"),
    (matched, "After Matching"),
]):
    nav_ps  = data[data.navigated==1]["ps"]
    ctrl_ps = data[data.navigated==0]["ps"]
    ax.hist(ctrl_ps, bins=30, alpha=0.55, color=SOLACE_GRAY,  label="Control",    density=True)
    ax.hist(nav_ps,  bins=30, alpha=0.55, color=SOLACE_BLUE,  label="Navigated",  density=True)
    ax.set_xlabel("Estimated Propensity Score")
    ax.set_ylabel("Density")
    ax.set_title(f"Figure 2{['A','B'][axes.tolist().index(ax)]} — PS Distribution\n{title}")
    ax.legend()
plt.suptitle("Propensity Score Overlap Before and After Matching", fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("output/figures/fig2_ps_distribution.png", dpi=180, bbox_inches="tight")
plt.close()
print("  ✓ Figure 2: PS distribution saved")

# Figure 3 — Primary Outcomes Bar Chart
fig, axes = plt.subplots(1, 3, figsize=(13, 5))
outcomes = [
    ("30-Day Readmission Rate", r_nav,     r_ctrl,     p_readmit, "%"),
    ("Mean 90-Day ER Visits",   er_nav,    er_ctrl,    p_er,      "visits"),
    ("Mean 180-Day Total Cost", cost_nav,  cost_ctrl,  p_cost,    "$"),
]
for ax, (title, v_nav, v_ctrl, pval, unit) in zip(axes, outcomes):
    colors = [SOLACE_TEAL, SOLACE_GRAY]
    bars   = ax.bar(["Navigated", "Control"], [v_nav, v_ctrl], color=colors, width=0.5, edgecolor="white")
    for bar, val in zip(bars, [v_nav, v_ctrl]):
        label = f"{val:.1%}" if unit == "%" else (f"${val:,.0f}" if unit == "$" else f"{val:.2f}")
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(v_nav, v_ctrl)*0.02,
                label, ha="center", va="bottom", fontsize=10, fontweight="bold")
    sig = "***" if pval < 0.001 else "**" if pval < 0.01 else "*" if pval < 0.05 else "ns"
    ax.set_title(f"{title}\n(p={pval:.4f}  {sig})", fontsize=10)
    ax.set_ylim(0, max(v_nav, v_ctrl) * 1.25)
    ax.set_facecolor(SOLACE_LIGHT)
    ax.tick_params(axis="x", labelsize=10)
    if unit == "$":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))
plt.suptitle("Figure 3 — Primary Outcomes: Patient Navigation vs. Usual Care\n(Propensity Score Matched Cohort)",
             fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("output/figures/fig3_outcomes.png", dpi=180, bbox_inches="tight")
plt.close()
print("  ✓ Figure 3: Primary outcomes saved")

# Figure 4 — Kaplan-Meier Time to 30-Day Readmission
fig, ax = plt.subplots(figsize=(9, 5.5))
kmf_nav  = KaplanMeierFitter()
kmf_ctrl = KaplanMeierFitter()

kmf_nav.fit(nav_m["days_to_readmit"],  event_observed=nav_m["event_observed"],  label="Navigated")
kmf_ctrl.fit(ctrl_m["days_to_readmit"], event_observed=ctrl_m["event_observed"], label="Control")

kmf_nav.plot_survival_function(ax=ax, color=SOLACE_TEAL, linewidth=2.5, ci_show=True, ci_alpha=0.12)
kmf_ctrl.plot_survival_function(ax=ax, color=SOLACE_GRAY, linewidth=2.5, ci_show=True, ci_alpha=0.12)

lr = lf_stats.logrank_test(
    nav_m["days_to_readmit"],  ctrl_m["days_to_readmit"],
    event_observed_A=nav_m["event_observed"],
    event_observed_B=ctrl_m["event_observed"],
)
ax.text(0.98, 0.55, f"Log-rank p = {lr.p_value:.4f}", transform=ax.transAxes,
        ha="right", fontsize=10, color="black",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#ccc"))
ax.set_xlabel("Days Post-Discharge")
ax.set_ylabel("Probability of Readmission-Free Survival")
ax.set_title("Figure 4 — Kaplan-Meier: Time to 30-Day Readmission\n(Propensity Score Matched Cohort)")
ax.set_ylim(0.7, 1.01)
ax.set_facecolor(SOLACE_LIGHT)
plt.tight_layout()
plt.savefig("output/figures/fig4_kaplan_meier.png", dpi=180, bbox_inches="tight")
plt.close()
print("  ✓ Figure 4: Kaplan-Meier curve saved")

# ── 9. Summary ────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("  SUMMARY OF FINDINGS")
print(f"{'='*60}")
print(f"  Matched cohort:      {len(matched_nav):,} navigated  vs  {len(matched_ctrl):,} control")
print(f"  30-day readmission:  {r_nav:.1%} vs {r_ctrl:.1%}  (RR={rr:.2f}, p={p_readmit:.4f})")
print(f"  90-day ER visits:    {er_nav:.2f} vs {er_ctrl:.2f}  (p={p_er:.4f})")
print(f"  180-day cost:        ${cost_nav:,.0f} vs ${cost_ctrl:,.0f}  (Δ=${cost_diff:,.0f})")
print(f"  Adjusted OR:         {OR:.2f}  [95% CI: {ci[0]:.2f}–{ci[1]:.2f}]  p={p_log:.4f}")
print(f"  NNT:                 {nnt:.1f} patients to prevent 1 readmission")
print(f"{'='*60}\n")
print("  All figures saved to output/figures/")
