# AI Use Disclosure

## Stage 1: Project setup and data verification
- **How AI was used:** Used AI to understand the project requirements,
  compare the four candidate papers, and select Card & Krueger (1994).
  AI also helped set up the Python environment and write a data-verification
  script (`code/check_data.py`).
- **How it was checked:** Verified the data against the paper's Table 1
  (410 stores, 331 NJ / 79 PA, 6 permanent closures, etc.).
- **Corrections:** AI initially suggested using Stata, but I switched to
  Python to follow the official repository template (`run_all.py`).
## Stage 2: Data cleaning and variable construction
- **How AI was used:** AI wrote `code/01_clean.py` to construct FTE employment
  (full-time + managers + 0.5 × part-time) and to handle store closures
  according to the paper (permanently closed stores set to 0; refused,
  renovation, and temporarily closed stores set to missing).
- **How it was checked:** Verified that the pre-policy mean FTE equals the
  paper's Table 3 (PA = 23.33, NJ = 20.44).
- **Corrections:** None — the FTE definition was taken directly from the
  paper's Table 2 note and confirmed against the data.
## Stage 3: Replication of Tables 3 and 4

### Table 3 (descriptive DID)
- **How AI was used:** AI wrote `code/02_table3.py` to reproduce all eight
  columns of Table 3, including the NJ-internal comparison by initial wage
  ($4.25, $4.26–4.99, ≥$5.00).
- **How it was checked:** Compared every cell against the published Table 3.
  All 40 cells match within rounding error (DiD = 2.75 vs. 2.76; low-vs-high
  difference = 3.36 in both).
- **Corrections:** The first version of the code produced empty columns for
  NJ and NJ−PA because the wage-group label function did not include an
  "all NJ" category. I identified the bug and had AI add a separate filter
  (`nj == 1`).

### Table 4 (regression models)
- **How AI was used:** AI wrote `code/03_table4.py` to estimate the five
  reduced-form models (NJ dummy and wage-gap specifications, with and without
  chain/ownership and region controls) using `statsmodels`.
- **How it was checked:** Compared coefficients, standard errors, and the
  regression standard error against Table 4. The NJ dummy (2.36 vs. 2.33) and
  the wage-gap coefficient (15.89 vs. 15.65) are very close to the published
  values.
- **Corrections / debugging:** Determining the correct sample was an iterative
  process:
  1. Requiring both wave-1 and wave-2 starting wages gave 351 stores.
  2. Restricting to stores open in wave 2 (STATUS2 == 1) gave 359 stores, but
     this shifted the dependent-variable mean from −0.25 to −0.05 and inflated
     the wage-gap coefficient, because it dropped the permanently closed stores
     whose wave-2 employment the paper sets to zero.
  3. The final specification retains permanently closed stores (wave-2 FTE = 0)
     and only drops stores with missing employment or wave-1 wage data, giving
     365 stores — closest to the paper's 357 with coefficients that match
     closely.
  I made the final call on the sample definition, reasoning that wave-2
  starting wages are an outcome and should not be used for sample selection.
## Stage 4: Replication of Figure 1 (distribution of starting wages)
- **How AI was used:** AI wrote `code/04_figure1.py` to reproduce the two-panel
  histogram of starting wages (February 1992 vs. November 1992) for New Jersey
  and Pennsylvania, binning wages from $4.25 to $5.55 in $0.10 intervals.
- **How it was checked:** Compared the visual pattern against the published
  Figure 1. In February 1992 the NJ and PA distributions are similar and
  concentrated at $4.25; in November 1992 nearly all NJ stores report $5.05
  while the PA distribution is unchanged.
- **Corrections:** None — the figure matched the paper's key pattern on the
  first run.
## Stage 5: Replication of Table 2 (descriptive statistics)
- **How AI was used:** AI wrote `code/05_table2.py` to reproduce the store-type
  distribution and the wave-1 / wave-2 means for both states, with t-tests for
  cross-state differences.
- **How it was checked:** Compared all cells against the published Table 2.
  Store-type shares, FTE employment, starting wages, prices, hours, and
  recruiting bonuses all match closely. The only exception is the
  "percentage of full-time employees," where our values are about 4 percentage
  points lower, likely reflecting a different denominator in the original paper.
- **Corrections:** None required for the matching rows; the full-time-share
  definition is flagged as a limitation in the report.
## Stage 6: Independent extension — heterogeneity analysis
- **How AI was used:** AI wrote `code/06_extension.py` to examine whether the
  employment effect varies by (1) binding intensity, (2) chain, and
  (3) ownership structure. The script reports means with standard errors,
  t-tests, and separate regressions.
- **How it was checked:** The binding-intensity grouping reproduces the paper's
  Table 3 pattern (low-wage +1.21 vs high-wage −2.16). Brand and ownership
  splits are original analyses; I verified the regression specification and
  interpreted the coefficients.
- **Key findings:** (i) Employment gains are larger where the minimum wage
  binds more tightly (p=0.011 vs the high-wage group). (ii) Positive effects
  appear in Burger King and Roy Rogers but not KFC. (iii) The effect is driven
  by franchise-owned stores (+22.2, p=0.007); company-owned stores show none.
- **Corrections:** None; this is an original extension beyond the replication.