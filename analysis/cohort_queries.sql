-- ============================================================
-- PATIENT NAVIGATION IMPACT STUDY — COHORT IDENTIFICATION
-- Mirrors real-world SQL workflow against claims/EHR data
-- Author: Sai Manasa Adduru, MPH, PharmD
-- ============================================================


-- ── 1. COHORT OVERVIEW ───────────────────────────────────────
-- How many patients, and what is the navigation split?
SELECT
    COUNT(*)                                        AS total_patients,
    SUM(n.navigated)                                AS navigated,
    COUNT(*) - SUM(n.navigated)                     AS control,
    ROUND(AVG(n.navigated) * 100, 1)                AS pct_navigated
FROM navigation_enrollment n;


-- ── 2. TABLE 1 — BASELINE CHARACTERISTICS ───────────────────
-- Key demographics and comorbidities by navigation status
SELECT
    n.navigated,
    COUNT(*)                                        AS n,
    ROUND(AVG(p.age), 1)                            AS mean_age,
    ROUND(AVG(p.female)  * 100, 1)                  AS pct_female,
    ROUND(AVG(p.dual_eligible) * 100, 1)            AS pct_dual_eligible,
    ROUND(AVG(p.rural)   * 100, 1)                  AS pct_rural,
    ROUND(AVG(d.cci), 2)                            AS mean_cci,
    ROUND(AVG(d.chf)     * 100, 1)                  AS pct_chf,
    ROUND(AVG(d.copd)    * 100, 1)                  AS pct_copd,
    ROUND(AVG(d.diabetes)* 100, 1)                  AS pct_diabetes,
    ROUND(AVG(u.prior_admits_12m), 2)               AS mean_prior_admits,
    ROUND(AVG(p.index_los), 2)                      AS mean_index_los
FROM navigation_enrollment   n
JOIN patient_encounters      p ON p.patient_id = n.patient_id
JOIN diagnoses               d ON d.patient_id = n.patient_id
JOIN utilization             u ON u.patient_id = n.patient_id
GROUP BY n.navigated
ORDER BY n.navigated;


-- ── 3. PRIMARY OUTCOMES BY NAVIGATION STATUS ────────────────
SELECT
    n.navigated,
    COUNT(*)                                        AS n,
    ROUND(AVG(u.readmit_30d)     * 100, 1)         AS readmit_rate_30d_pct,
    ROUND(AVG(u.er_visits_90d),  2)                 AS mean_er_visits_90d,
    ROUND(AVG(u.total_cost_180d), 0)                AS mean_cost_180d
FROM navigation_enrollment n
JOIN utilization           u ON u.patient_id = n.patient_id
GROUP BY n.navigated
ORDER BY n.navigated;


-- ── 4. HIGH-RISK SUBGROUP — Dual Eligible + CCI ≥ 3 ─────────
-- Target population most likely to benefit from navigation
SELECT
    n.navigated,
    COUNT(*)                                        AS n,
    ROUND(AVG(u.readmit_30d) * 100, 1)             AS readmit_rate_pct,
    ROUND(AVG(u.total_cost_180d), 0)                AS mean_cost
FROM navigation_enrollment   n
JOIN patient_encounters      p ON p.patient_id = n.patient_id
JOIN diagnoses               d ON d.patient_id = n.patient_id
JOIN utilization             u ON u.patient_id = n.patient_id
WHERE p.dual_eligible = 1
  AND d.cci >= 3
GROUP BY n.navigated
ORDER BY n.navigated;


-- ── 5. COMORBIDITY BURDEN AND READMISSION ───────────────────
-- Does navigation help more for higher-risk patients?
SELECT
    CASE
        WHEN d.cci = 0            THEN '0 — None'
        WHEN d.cci BETWEEN 1 AND 2 THEN '1–2 — Mild'
        WHEN d.cci BETWEEN 3 AND 4 THEN '3–4 — Moderate'
        ELSE '5+ — Severe'
    END                                             AS cci_group,
    n.navigated,
    COUNT(*)                                        AS n,
    ROUND(AVG(u.readmit_30d) * 100, 1)             AS readmit_rate_pct,
    ROUND(AVG(u.total_cost_180d), 0)                AS mean_cost_180d
FROM navigation_enrollment   n
JOIN diagnoses               d ON d.patient_id = n.patient_id
JOIN utilization             u ON u.patient_id = n.patient_id
GROUP BY cci_group, n.navigated
ORDER BY d.cci, n.navigated;


-- ── 6. COST DISTRIBUTION — PERCENTILES ──────────────────────
-- Understand cost spread (required for budget impact modeling)
SELECT
    n.navigated,
    ROUND(MIN(u.total_cost_180d), 0)                AS min_cost,
    ROUND(AVG(u.total_cost_180d), 0)                AS mean_cost,
    ROUND(MAX(u.total_cost_180d), 0)                AS max_cost,
    COUNT(CASE WHEN u.total_cost_180d > 50000 THEN 1 END) AS high_cost_patients
FROM navigation_enrollment n
JOIN utilization           u ON u.patient_id = n.patient_id
GROUP BY n.navigated;


-- ── 7. REPEAT READMISSION RISK ───────────────────────────────
-- Patients with prior admissions — highest risk segment
SELECT
    CASE
        WHEN u.prior_admits_12m = 0 THEN '0 prior'
        WHEN u.prior_admits_12m = 1 THEN '1 prior'
        WHEN u.prior_admits_12m = 2 THEN '2 prior'
        ELSE '3+ prior'
    END                                             AS prior_admit_group,
    n.navigated,
    COUNT(*)                                        AS n,
    ROUND(AVG(u.readmit_30d) * 100, 1)             AS readmit_rate_pct
FROM navigation_enrollment   n
JOIN utilization             u ON u.patient_id = n.patient_id
GROUP BY prior_admit_group, n.navigated
ORDER BY u.prior_admits_12m, n.navigated;


-- ── 8. DATA QUALITY CHECK ────────────────────────────────────
-- Every real analysis starts with a DQ check
SELECT
    'patient_encounters'    AS tbl, COUNT(*) AS rows FROM patient_encounters
UNION ALL SELECT 'diagnoses',          COUNT(*) FROM diagnoses
UNION ALL SELECT 'utilization',        COUNT(*) FROM utilization
UNION ALL SELECT 'navigation_enrollment', COUNT(*) FROM navigation_enrollment;
