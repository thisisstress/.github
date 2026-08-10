# Final profile validation

Validated on **2026-08-10** for the current `thisisstress/.github` Organization profile.

## Result

**PASS**

- Workflow: `Validate organization profile`
- Run: `31357367641`
- Run number: `24`
- Trigger commit: `ecf10077e75016c985c24dd87c24dc66b39b8f6d`
- Conclusion: `success`

## Active profile contract

The public landing page intentionally uses only two SVG visuals:

- `profile/assets/hero-current.svg`
- `profile/assets/final-architecture.svg`

The reader-facing content remains in `profile/README.md`. Images use a `#_` no-op link wrapper so clicking them does not open the raw SVG asset.

## Final presentation state

- Final model: **BS 8/6 — ExtraTrees + Pair-Neighbor**
- Internal validation MAE: **0.147300**
- Public MAE: **0.1266866667**
- Private MAE: **0.1473**
- Blend: **ExtraTrees 76% + Pair-Neighbor 24%**

## Repository visibility metadata

| Repository | Visibility |
|---|---|
| `stress_project_UNIFIED` | Public |
| `stress_project_BS` | Public |
| `stress_project_JH` | Public |
| `stress_project_SK` | Private |

`profile/content.json` is aligned with this state.

## Validation checks

The current validator confirms:

- the two active SVG references exist and parse correctly
- no active GIF is referenced by the landing README
- profile images use the no-op link wrapper
- final model and MAE metadata match the adopted result
- repository visibility metadata matches the current four-repository layout
- fertility and smoking Organization content is not mixed into the active profile package
- public data/model artifact types such as CSV, parquet, pickle, joblib, and `.env` are absent
- files larger than 10 MB are absent
- the GitHub Actions workflow has read-only contents permission

The obsolete renderer, dependency file, GIF optimization metadata, and unused `final-*` SVGs from the previous multi-section landing contract were removed during this cleanup.
