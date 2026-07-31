# Upgrade 09 — Section headers

이번 업그레이드는 섹션 구분선과 챕터 헤더 시스템만 변경합니다.

## 변경점

- Research부터 Team까지 5개 섹션 헤더를 동일한 브랜드 디자인으로 통일
- `01`부터 `05`까지 챕터 번호 부여
- 딥그린 번호 카드, 골드 포인트, 세이지 그라데이션 라인 적용
- 기존 README 앵커를 유지해 상단 내비게이션이 그대로 작동
- 외부 폰트·CDN·JavaScript 없이 리포 내부 SVG만 사용
- 각 섹션의 본문과 애니메이션은 변경하지 않음

## 주요 파일

- `profile/README.md`
- `profile/assets/section-research.svg`
- `profile/assets/section-baseline.svg`
- `profile/assets/section-workflow.svg`
- `profile/assets/section-principles.svg`
- `profile/assets/section-team.svg`
- `scripts/render_assets.py`
