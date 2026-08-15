# Profile Validation Record

**Date:** 2026-08-10  
**Status:** PASS

## Workflow

| 항목 | 값 |
|---|---|
| Workflow | `Validate organization profile` |
| Run | `31358791351` |
| Run number | `28` |
| Trigger commit | `9b83f98425d5b768b84559e4582cb1723ebd29f9` |
| Conclusion | `success` |

## Active Profile Contract

- `profile/README.md` — reader-facing copy
- `profile/assets/hero-current.svg` — active hero
- `profile/assets/final-architecture.svg` — active architecture
- image wrapper — `#_` no-op link
- active GIF references — none

## Final Presentation State

| 항목 | 값 |
|---|---:|
| Final model | **BS 8/6 — ExtraTrees + Pair-Neighbor** |
| Internal validation MAE | **0.147300** |
| Public MAE | **0.1266866667** |
| Private MAE | **0.1473** |
| Blend | **ExtraTrees 76% + Pair-Neighbor 24%** |

## Repository Visibility

| Repository | Visibility |
|---|---|
| `stress_project_UNIFIED` | Public |
| `stress_project_BS` | Public |
| `stress_project_JH` | Public |
| `stress_project_SK` | Private |

## Validation Checks

- active SVG existence · XML parse
- active GIF reference absence
- profile image `#_` wrapper
- final model / MAE metadata consistency
- four-repository visibility metadata consistency
- unrelated fertility/smoking Organization content absence
- public CSV/parquet/pickle/joblib/`.env` absence
- files > 10 MB absence
- workflow `contents: read`

## Legacy Cleanup

Removed from prior multi-section landing contract:
- obsolete renderer
- obsolete dependency file
- GIF optimization metadata
- unused `final-*` SVGs
