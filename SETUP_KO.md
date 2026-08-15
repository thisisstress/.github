# thisisstress Organization Profile 관리

**Entry:** `profile/README.md`

## 공개 구조

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

**Active visuals:** `hero-current.svg` · `final-architecture.svg`  
**Image link contract:** `<a href="#_">...</a>`

## 최종 결과

- 최종 채택: **BS 8/6 — ExtraTrees + Pair-Neighbor**
- 내부 검증 MAE: **0.147300**
- Public MAE: **0.1266866667**
- Private MAE: **0.1473**
- Blend: **ExtraTrees 76% + Pair-Neighbor 24%**

**Result SSOT:** `stress_project_UNIFIED` · `stress_project_BS`

## Repository 공개 상태

| Repository | 공개 상태 |
|---|---|
| `stress_project_UNIFIED` | Public |
| `stress_project_BS` | Public |
| `stress_project_JH` | Public |
| `stress_project_SK` | Private |

**Metadata mirror:** `profile/content.json.repository_map`

## 검증 계약

`Validate organization profile` · read-only contents permission

- active SVG 존재 · XML parse
- active GIF reference 없음
- profile image `#_` wrapper
- final model / MAE metadata
- repository visibility metadata
- unrelated fertility/smoking Organization copy 없음
- CSV · parquet · pickle · joblib · `.env` 공개 금지
- file size ≤ 10 MB

```bash
python scripts/validate_profile.py
git diff --check
```

## 수정 규칙

1. 공식 근거 확인 — 발표자료 · source repository
2. `profile/content.json` / `profile/README.md` 동기화
3. 시각 구조 변경 시에만 SVG 수정
4. 신규 profile image → `#_` wrapper 유지
5. 원본 대회 데이터 · submission CSV · secret · PII · 비공개 연구 artifact 복사 금지
