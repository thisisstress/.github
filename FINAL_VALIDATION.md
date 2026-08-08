# Final profile validation report

Validated on **2026-08-08** for the final-presentation-aligned
`thisisstress/.github` organization profile.

## Result

**PASS — final SVG profile validated on GitHub Actions**

- Workflow: `Validate organization profile`
- Trigger commit: `9df1cf7faae043a2d5d60097737abb741a902c8e`
- Workflow run: `31237505015`
- Conclusion: **success**

## Final profile contract

The active organization README now uses vector assets for every animated visual.
Legacy GIF files remain only as historical repository assets and are not referenced
by the active README.

Required final animation set:

- `profile/assets/hero-current.svg`
- `profile/assets/final-architecture.svg`
- `profile/assets/final-workflow.svg`
- `profile/assets/final-principles.svg`
- `profile/assets/final-team.svg`
- `profile/assets/final-repositories.svg`
- `profile/assets/final-status.svg`
- `profile/assets/final-footer.svg`

## Validation checks

The current validator checks:

- README local asset references exist
- no active README reference points to a legacy GIF
- required final SVG assets are present
- all eight profile anchors resolve exactly
- every README image has an explicit navigation destination
- README images do not link directly to raw asset files
- final-result markers occur exactly once
- stale `pending` / legacy GIF wording is absent from README
- every SVG in `profile/assets` parses as XML
- archival GIFs, when present, still decode and remain within historical size limits
- `content.json` contains exactly three team members and four repository nodes
- final presentation status and final release state use the supported schema
- experiment status is non-empty
- forbidden public data/model file types are absent
- files above 10 MB are absent
- the validation workflow is read-only and invokes `scripts/validate_profile.py`

## Final presentation state

- Profile state: `final_presentation_aligned`
- Final release status: `adopted`
- Final model: **8/6 Team Integrated Model — ExtraTrees + Pair-Neighbor**
- Public MAE: **0.1266866667**
- Private MAE: **0.1473**
- Snapshot date: **2026-08-08**

Model display names in the organization profile use team-level naming. Individual
repository names are retained only where needed to identify source or record locations.

## Automation safety change

The previous workflow automatically regenerated GIF-era assets from
`scripts/render_assets.py`. That behavior was intentionally removed because the
final profile now contains hand-curated SVG animations and final-presentation
section headers.

The workflow is now **validation-only**:

- repository checkout
- Python setup
- dependency installation
- `python scripts/validate_profile.py`
- `git diff --check`

It has `contents: read` permission and cannot overwrite the final visual assets.

## Transition note

A previously queued legacy render run (`31237500468`) started from an older
commit while the validator/workflow migration was being applied. It completed
with **failure at validation**, and its asset commit step was **skipped**. No
legacy regenerated assets from that run were pushed to `main`.

The following validation-only run (`31237505015`) completed successfully and is
the authoritative final profile validation result.
