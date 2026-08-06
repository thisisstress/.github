# thisisstress 조직 프로필 설치 및 업데이트 방법

GitHub 조직의 공개 메인 화면은 **퍼블릭 `.github` 리포지토리의 `profile/README.md`**를 표시합니다.

## 1. GitHub에서 리포 만들기

조직 `thisisstress`에서 새 리포를 만듭니다.

- Repository name: `.github`
- Visibility: **Public**
- README 자동 생성: 끔

## 2. 로컬 Clone

```powershell
cd C:\gitrepository
git clone https://github.com/thisisstress/.github.git
cd .github
```

## 3. 기본 구조

```text
.github/
├─ profile/
│  ├─ README.md
│  ├─ content.json
│  ├─ performance.json
│  └─ assets/
├─ scripts/
│  ├─ render_assets.py
│  └─ validate_profile.py
├─ requirements.txt
└─ SETUP_KO.md
```

## 현재 연구 중인 화면 관리

현재 조직 프로필은 **최종 우승 모델이 아니라 공개 가능한 재현 기준점**을 보여줍니다.

`profile/content.json`의 주요 필드:

```json
{
  "profile_status": {
    "state": "research_in_progress",
    "as_of": "2026-08-06"
  },
  "baseline": "V1 Weighted Quantile ExtraTrees",
  "public_mae": "0.1282776667",
  "model": "ExtraTrees × 1,200",
  "aggregation": "51% Quantile",
  "final_release": {
    "status": "pending"
  }
}
```

- `baseline`, `public_mae`, `model`, `aggregation`은 현재 공개 가능한 재현 기준점입니다.
- `final_release.status`는 연구 중에는 `pending`으로 유지합니다.
- 애니메이션 실험 현황이 실제보다 오래된 경우 `experiment_status.snapshot_date`를 임의로 최신 날짜로 바꾸지 않습니다.
- `profile/README.md`의 `CURRENT-RESULT:START/END` 블록은 현재 상태를 설명하는 공개 문구입니다.

## 연구 종료 후 최종 결과 업데이트

최종 모델과 공개 범위가 확정되면 다음 순서로 갱신합니다.

1. `profile/content.json`
   - `profile_status.state` → `research_complete`
   - `profile_status.as_of` → 확정일
   - `baseline`, `public_mae`, `model`, `aggregation` → 최종 공개값
   - `final_release.status` → `published`
   - 공개 가능한 `model`, `public_mae`, `private_mae`, `repository_url`, `presentation_url`, `updated_at` 입력
   - `experiment_status.snapshot_date`와 항목을 최종 연구 상태로 갱신
2. `profile/README.md`
   - `CURRENT-RESULT:START/END` 사이 문구만 최종 결과로 교체
   - Baseline 섹션의 “not the final champion” 문구를 최종 결과 설명으로 교체
3. 애셋 재생성 및 검증
4. 변경 내역 확인 후 Push

## 이미지 클릭 동작

GitHub README는 이미지 클릭 시 원본 애셋 파일로 이동할 수 있습니다.

이 프로필은 모든 이미지를 명시적인 페이지 내부 링크 또는 조직 Overview 링크로 감싸 두었습니다.

- 애니메이션을 클릭해도 `.gif`·`.svg` 파일 화면으로 이동하지 않습니다.
- `href="./assets/..."` 형태의 링크를 새로 만들지 않습니다.
- 이미지에서 `<a href="...">` 래퍼를 제거하지 않습니다.
- 새 이미지를 추가할 때도 관련 섹션 앵커로 연결합니다.

## 로컬에서 애니메이션 다시 만들기

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\render_assets.py
python scripts\validate_profile.py
```

정상이라면 다음과 비슷한 결과가 나옵니다.

```text
Profile assets regenerated.
PASS: ... README assets, 8 anchors, ... SVGs, 10 GIFs
```

## 비용 및 공개 안전 원칙

- `.github` 리포는 반드시 Public으로 둡니다.
- Workflow는 소스·설정 변경 때만 실행합니다.
- Scheduled workflow를 사용하지 않습니다.
- 외부 유료 API, 호스팅, 이미지 CDN을 사용하지 않습니다.
- GIF와 SVG는 모두 리포 자체에서 제공합니다.
- 원본 데이터, 제출 CSV, 비밀키와 개인 식별 정보는 커밋하지 않습니다.

## 공개 리포 Pin

조직 프로필에는 최대 6개의 공개 리포를 Pin할 수 있습니다.
공개 쇼케이스 리포가 생기면 조직 Settings에서 직접 선택합니다.

## 권장 Git 명령어

```powershell
git status --short
python -m py_compile scripts\render_assets.py scripts\validate_profile.py
python scripts\render_assets.py
python scripts\validate_profile.py
git diff --check
git add .
git commit -m "docs: update organization research profile"
git push origin main
```
