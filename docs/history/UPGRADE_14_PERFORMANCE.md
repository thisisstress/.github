# Upgrade 14 — Animation performance

이번 업그레이드는 디자인과 README 내용을 바꾸지 않고,
전체 GIF 전달 성능만 최적화합니다.

## 결과

- GIF 수: 10개
- 최적화 전: 13.22 MB
- 최적화 후: 6.92 MB
- 감소율: 47.6%

## 적용 방식

- GitHub README 실사용 폭을 고려해 최대 1,000px
- 루프 전체 시간은 유지하면서 대표 프레임 최대 22개
- 애니메이션별 공통 80색 팔레트
- 디더링 제거로 노이즈와 용량 감소
- `scripts/render_assets.py` 재실행 시에도 같은 설정 적용

## 주요 파일

- `profile/assets/*.gif`
- `profile/performance.json`
- `profile/assets/performance-optimization-preview.png`
- `scripts/render_assets.py`
