# thisisstress Organization Profile 관리

GitHub Organization 메인 화면은 Public `.github` 저장소의 `profile/README.md`를 사용합니다.

## 현재 공개 구조

```text
.github/
├─ profile/
│  ├─ README.md
│  ├─ content.json
│  └─ assets/
│     ├─ hero-current.svg
│     └─ final-architecture.svg
├─ scripts/
│  └─ validate_profile.py
└─ .github/workflows/
   └─ render-profile-assets.yml
```

현재 랜딩페이지에서 직접 사용하는 시각 자료는 `hero-current.svg`와 `final-architecture.svg` 두 개입니다. 두 이미지는 README에서 `#_` 링크로 감싸 원본 SVG 화면으로 이동하지 않도록 합니다.

## 최종 결과

- 최종 채택: **BS 8/6 — ExtraTrees + Pair-Neighbor**
- 내부 검증 MAE: **0.147300**
- Public MAE: **0.1266866667**
- Private MAE: **0.1473**
- Blend: **ExtraTrees 76% + Pair-Neighbor 24%**

최종 결과의 원본과 모델 계보는 `stress_project_UNIFIED`와 `stress_project_BS`를 기준으로 확인합니다.

## Repository 공개 상태

| Repository | 공개 상태 |
|---|---|
| `stress_project_UNIFIED` | Public |
| `stress_project_BS` | Public |
| `stress_project_JH` | Public |
| `stress_project_SK` | Private |

`profile/content.json`의 `repository_map`도 이 상태와 일치하게 유지합니다.

## 검증

GitHub Actions의 `Validate organization profile` workflow는 쓰기 권한 없이 다음 항목을 확인합니다.

- README가 사용하는 두 SVG 파일의 존재와 XML 파싱
- 활성 GIF 참조가 없는지
- 이미지가 `#_` no-op 링크로 감싸져 있는지
- 최종 모델명과 MAE 값
- 네 저장소의 공개 상태 메타데이터
- 난임·흡연 Organization 문구가 섞이지 않았는지
- CSV, parquet, pickle, joblib, `.env` 등의 공개 금지 파일 여부
- 10MB 초과 파일 여부

로컬에서는 추가 패키지 설치 없이 실행할 수 있습니다.

```bash
python scripts/validate_profile.py
git diff --check
```

## 수정 원칙

새 공식 결과가 생긴 경우 먼저 근거가 되는 발표자료와 원본 저장소를 확인한 뒤 `profile/content.json`과 `profile/README.md`를 같은 값으로 수정합니다. 시각 구조가 달라질 때만 SVG를 수정합니다.

`.github` 저장소에는 원본 대회 데이터, 제출 CSV, 비밀키, 개인 식별 정보, 공개되지 않은 연구 산출물을 복사하지 않습니다.
