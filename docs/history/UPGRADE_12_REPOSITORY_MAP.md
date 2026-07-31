# Upgrade 12 — Research repository map

이번 업그레이드는 공개 프로젝트 쇼케이스 영역 한 요소만 추가합니다.

현재 확인된 `thisisstress` 연구 리포 4개가 모두 비공개이므로,
공개 방문자에게 작동하지 않는 링크를 제공하지 않습니다.

## 변경점

- JH · BS · SK 개인 연구 리포를 잠금 카드로 표시
- 세 개인 노드가 `stress_project_UNIFIED` 허브에 연결
- 상태 표현: `LOCKED → SYNCING → CONNECTED`
- 현재 상태를 `4 PRIVATE REPOSITORIES`로 명확히 표시
- 공식 공개가 가능한 시점에 링크를 활성화할 수 있도록
  `profile/content.json`에 repository map 데이터 추가
- 기존 애니메이션과 다른 README 영역은 변경하지 않음

## 공개 전환 방법

`profile/content.json`에서 대상 리포의 값을 변경합니다.

```json
{
  "visibility": "public",
  "public_url": "https://github.com/thisisstress/REPOSITORY_NAME"
}
```

## 주요 파일

- `profile/README.md`
- `profile/content.json`
- `profile/assets/section-repositories.svg`
- `profile/assets/repository-map.gif`
- `profile/assets/repository-map-preview.png`
- `scripts/render_assets.py`
