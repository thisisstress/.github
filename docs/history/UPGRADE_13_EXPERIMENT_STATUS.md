# Upgrade 13 — Experiment status registry

이번 업그레이드는 현재 연구 상태를 보여주는 보드 한 요소만 추가합니다.

## 상태 스냅샷

- V1 Baseline: `LOCKED`
- N06 split-seed stability: `VERIFIED`
- Alternative model screen: `ACTIVE`
- Unified promotion: `GATED`
- Public release: `LOCKED`

스냅샷 기준일은 `2026-07-31`입니다. 최신 상태가 달라지면
`profile/content.json`의 `experiment_status`만 갱신할 수 있습니다.

## 주요 파일

- `profile/README.md`
- `profile/content.json`
- `profile/assets/section-status.svg`
- `profile/assets/experiment-status.gif`
- `profile/assets/experiment-status-preview.png`
- `scripts/render_assets.py`
