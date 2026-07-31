# Upgrade 11 — Mobile rhythm and readability

이번 업그레이드는 GitHub 모바일 화면의 여백과 읽기 흐름만 변경합니다.

## 변경점

- 내비게이션을 3개씩 두 줄로 고정
- 버튼 폭을 112px로 축소해 작은 화면에서 안정적으로 배치
- 각 챕터 사이에 가벼운 SVG 스페이서 추가
- Baseline 설정을 두 줄로 분리해 가로 넘침 방지
- Workflow 상세 설명과 Public policy를 접을 수 있는 `<details>`로 변경
- 기존 GIF, 모델 정보와 연구 내용은 변경하지 않음

## 주요 파일

- `profile/README.md`
- `profile/assets/section-spacer.svg`
- `profile/assets/mobile-layout-preview.png`
- `scripts/render_assets.py`
