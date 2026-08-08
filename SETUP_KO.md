# thisisstress 조직 프로필 설치 및 업데이트 방법

GitHub 조직의 공개 메인 화면은 **Public `.github` 리포지토리의 `profile/README.md`**를 표시합니다.

현재 프로필은 **2026-08-08 최종 발표 기준**으로 정리되어 있으며, 활성 애니메이션은 SVG 벡터 자산을 사용합니다.

## 1. 기본 구조

```text
.github/
├─ profile/
│  ├─ README.md
│  ├─ content.json
│  ├─ performance.json        # 과거 GIF 최적화 기록
│  └─ assets/
├─ scripts/
│  ├─ render_assets.py        # 레거시 렌더러 · 자동 실행하지 않음
│  └─ validate_profile.py     # 현재 프로필 검증기
├─ .github/workflows/
│  └─ render-profile-assets.yml  # 현재는 validation-only
├─ requirements.txt
└─ SETUP_KO.md
```

## 2. 현재 최종 프로필 상태

`profile/content.json`의 핵심 상태는 다음과 같습니다.

```json
{
  "profile_status": {
    "state": "final_presentation_aligned",
    "as_of": "2026-08-08"
  },
  "model": "ExtraTrees + Pair-Neighbor",
  "public_mae": "0.1266866667",
  "private_mae": "0.1473",
  "blend": "76:24",
  "final_release": {
    "status": "adopted",
    "model": "8/6 Team Integrated Model — ExtraTrees + Pair-Neighbor"
  }
}
```

현재 최종 발표 기준은 다음과 같습니다.

- 최종 채택: **8/6 Team Integrated Model — ExtraTrees + Pair-Neighbor**
- Public MAE: **0.1266866667**
- Private MAE: **0.1473**
- ExtraTrees 1,200
- Tree Quantile 54%
- Pair Quantile 48%
- Blend 76:24

모델 표시명은 팀 공동 결과를 기준으로 사용하고, 개별 리포명은 실행 원본이나 기록 위치를 추적하는 출처 정보로만 사용합니다.

## 3. 활성 애니메이션 자산

Profile README에서 사용하는 주요 애니메이션은 모두 SVG입니다.

```text
hero-current.svg
final-architecture.svg
final-workflow.svg
final-principles.svg
final-team.svg
final-repositories.svg
final-status.svg
final-footer.svg
```

기존 GIF 파일은 연구·디자인 이력 보존을 위해 `profile/assets/`에 남아 있을 수 있지만 **현재 README에서는 사용하지 않습니다.**

`profile/performance.json` 역시 과거 GIF 최적화 작업의 기록으로 봅니다.

## 4. 이미지와 글자 분리 원칙

최종 프로필에서는 큰 제목, 모델명, 점수처럼 정확성이 필요한 내용은 README 텍스트로 표시하고 애니메이션은 시각적 흐름만 담당합니다.

- 모델명·점수를 애니메이션 이미지 안에 새로 박아 넣지 않습니다.
- 결과가 변경될 경우 우선 `content.json`과 README 텍스트를 수정합니다.
- SVG 애니메이션은 구조 자체가 달라질 때만 수정합니다.
- 이미지의 `alt` 설명도 실제 의미와 맞게 유지합니다.

## 5. 이미지 클릭 동작

GitHub README에서 이미지는 모두 명시적인 페이지 내부 링크 또는 Organization Overview 링크로 감쌉니다.

- 애니메이션을 클릭해도 `.gif`·`.svg` 원본 파일 화면으로 이동하지 않게 합니다.
- `href="./assets/..."` 형태의 직접 자산 링크를 만들지 않습니다.
- 이미지에서 `<a href="...">` 래퍼를 제거하지 않습니다.
- 새 이미지를 추가할 때도 관련 섹션 앵커 또는 Organization Overview로 연결합니다.

## 6. 현재 자동화 방식

`.github/workflows/render-profile-assets.yml`은 현재 **검증 전용**입니다.

자동으로 이미지를 재생성하거나 커밋하지 않습니다.

실행 내용:

1. 저장소 Checkout
2. Python 3.12 설정
3. 의존성 설치
4. `python scripts/validate_profile.py`
5. `git diff --check`

Workflow 권한은 `contents: read`이므로 최종 SVG를 자동으로 덮어쓸 수 없습니다.

## 7. 로컬 검증

Windows PowerShell 예시:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\validate_profile.py
git diff --check
```

macOS / Linux 예시:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_profile.py
git diff --check
```

`render_assets.py`는 과거 GIF 기반 프로필을 생성하던 레거시 렌더러입니다. **현재 최종 프로필 유지보수 과정에서는 실행하지 않습니다.**

## 8. `validate_profile.py`가 확인하는 것

- README의 로컬 이미지 파일 존재 여부
- 활성 GIF 참조가 없는지
- 최종 SVG 세트가 모두 연결되어 있는지
- 8개 앵커와 내부 이동 링크
- 모든 이미지에 명시적인 클릭 목적지가 있는지
- SVG XML 파싱
- `content.json`의 팀 3명 / 리포 4개 구조
- `final_presentation_aligned` / `adopted` 상태 계약
- 오래된 `pending` 및 GIF 문구가 README에 남아 있지 않은지
- CSV, parquet, pickle, joblib, `.env` 등 공개 금지 파일 여부
- 10MB 초과 파일 여부

## 9. 최종 결과를 다시 수정해야 할 때

새 공식 결과가 생겨 프로필을 변경해야 한다면 다음 순서를 권장합니다.

1. 근거가 되는 발표자료·원본 리포·Notebook을 먼저 확인합니다.
2. `profile/content.json`의 모델·점수·날짜를 갱신합니다.
3. `profile/README.md`의 실제 텍스트를 같은 값으로 갱신합니다.
4. 구조가 달라진 섹션만 해당 `final-*.svg`를 수정합니다.
5. `python scripts/validate_profile.py`를 실행합니다.
6. `git diff --check` 후 Push합니다.

숫자만 바뀌었는데 전체 SVG를 다시 만들거나, 과거 GIF 렌더러를 실행하는 방식은 권장하지 않습니다.

## 10. 공개 안전 원칙

- `.github` 리포는 Organization Profile 표시를 위해 Public으로 유지합니다.
- 원본 대회 데이터와 제출 CSV를 공개하지 않습니다.
- 비밀키와 개인 식별 정보를 커밋하지 않습니다.
- 공개되지 않은 학습 산출물을 Profile 리포로 복사하지 않습니다.
- 내부 CV, Public, Private 점수를 서로 다른 종류의 근거로 구분해 적습니다.
- 공개 전환이 확정되지 않은 Private 연구 리포의 공개 시점을 미리 약속하지 않습니다.

## 11. 권장 Git 명령어

```powershell
git status --short
python -m py_compile scripts\validate_profile.py
python scripts\validate_profile.py
git diff --check
git add .
git commit -m "docs: update final organization profile"
git push origin main
```

현재 최종 검증 결과는 루트의 `FINAL_VALIDATION.md`에 기록합니다.
