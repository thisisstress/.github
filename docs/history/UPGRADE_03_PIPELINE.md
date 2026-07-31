# Upgrade 03 — Research workflow pipeline

이번 업그레이드는 Research workflow 애니메이션만 변경합니다.

## 변경점

- DATA → FEATURES → MODEL → Q51 → VALIDATE 흐름 시각화
- 골드 데이터 패킷이 단계 사이를 이동
- 완료 단계는 체크 배지로 표시
- 각 단계에 전용 아이콘 추가
- V1 baseline → controlled change → multi-seed validation → shared evidence 흐름 강조
- 기존 README 구조와 다른 애니메이션은 유지

## 주요 파일

- `profile/assets/pipeline.gif`
- `profile/assets/pipeline-preview.png`
- `scripts/render_assets.py`
