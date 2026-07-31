# Upgrade 05 — Baseline V1 architecture

이번 업그레이드는 `Baseline V1` 설정표 영역만 변경합니다.

## 변경점

- 정적 Markdown 표를 애니메이션 모델 아키텍처로 교체
- INPUT → FEATURES → EXTRATREES → Q51 → OUTPUT 흐름 시각화
- 골드 예측 패킷이 각 단계를 이동
- 각 단계 전용 아이콘과 진행 바 추가
- 하단에 핵심 하이퍼파라미터 고정 표시
- README의 다른 요소는 변경하지 않음

## 주요 파일

- `profile/README.md`
- `profile/assets/baseline-architecture.gif`
- `profile/assets/baseline-architecture-preview.png`
- `scripts/render_assets.py`
