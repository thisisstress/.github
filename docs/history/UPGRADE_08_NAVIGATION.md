# Upgrade 08 — Landing navigation

이번 업그레이드는 README 상단 내비게이션 한 요소만 변경합니다.

## 변경점

- 기존 텍스트 링크를 브랜드 SVG 버튼 6개로 교체
- Overview · Research · Baseline V1 · Workflow · Principles · Team
- 모든 버튼은 실제 README 앵커로 이동
- Overview는 활성 상태의 딥그린·골드 디자인
- 나머지는 화이트·세이지 디자인
- 모바일에서는 GitHub 화면 폭에 맞춰 자연스럽게 줄바꿈
- 외부 CDN이나 유료 자원 없이 리포 내부 SVG만 사용

## 주요 파일

- `profile/README.md`
- `profile/assets/nav-*.svg`
- `profile/assets/navigation-preview.png`
- `scripts/render_assets.py`
