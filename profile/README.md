<a id="top"></a>

<p align="center">
  <a href="#research" aria-label="연구 소개로 이동">
    <img src="./assets/hero-current.svg" width="100%" alt="건강 신호, ExtraTrees, Pair-Neighbor가 하나의 예측으로 결합되는 추상 애니메이션" />
  </a>
</p>

<h1 align="center">THIS IS STRESS</h1>

<p align="center">
  <strong>스트레스 지수 예측 해커톤 · 2거 스트레스조</strong><br />
  개인의 건강·생활 데이터를 바탕으로 0~1 범위의 스트레스 점수를 예측합니다.
</p>

<p align="center">
  <strong>최종 채택 · 8월 6일 통합모델</strong><br />
  <code>ExtraTrees 76%</code> + <code>Pair-Neighbor 24%</code><br />
  <strong>Public MAE 0.1266866667</strong> · Private MAE 0.1473
</p>

<p align="center">
  <a href="https://github.com/thisisstress"><img src="./assets/nav-overview.svg" width="112" alt="Overview" /></a>
  <a href="#research"><img src="./assets/nav-research.svg" width="112" alt="Research" /></a>
  <a href="#baseline"><img src="./assets/nav-baseline.svg" width="112" alt="Final result" /></a><br />
  <a href="#workflow"><img src="./assets/nav-workflow.svg" width="112" alt="Workflow" /></a>
  <a href="#principles"><img src="./assets/nav-principles.svg" width="112" alt="Principles" /></a>
  <a href="#team"><img src="./assets/nav-team.svg" width="112" alt="Team" /></a><br />
  <a href="#repositories"><img src="./assets/nav-repositories.svg" width="112" alt="Repositories" /></a>
  <a href="#status"><img src="./assets/nav-status.svg" width="112" alt="Experiment status" /></a>
</p>

<!-- CURRENT-RESULT:START -->

> **Final presentation aligned · updated 2026-08-08**  
> 최종 발표에서는 **재현 가능하고 Private까지 확인된 8월 6일 통합모델**을 최종 채택했습니다.  
> `ExtraTrees 1,200` · `Tree Q=54%` · `Pair Q=48%` · `Blend 76:24` · **Public MAE 0.1266866667 · Private MAE 0.1473**  
> Public `0.1265`의 Fresh V6는 내부·Private 검증 기록이 없어 최종 채택에서 제외했습니다.

<!-- CURRENT-RESULT:END -->

<a href="#research" aria-label="연구 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="research"></a>

<a href="#research" aria-label="연구 섹션">
  <img src="./assets/section-research.svg" width="100%" alt="01 Research — What we are building" />
</a>

<p align="center">
  <a href="#baseline" aria-label="최종 결과로 이동">
    <img src="./assets/research-visual.svg" width="100%" alt="animated flow from health signals to hybrid modeling and shared evidence" />
  </a>
</p>

| Health signals | Hybrid modeling | Shared evidence |
|---|---|---|
| BMI, 맥압, 평균동맥압, 콜레스테롤·혈당 비율과 결측 패턴처럼 원본 건강 데이터를 더 의미 있게 표현합니다. | ExtraTrees가 전역 비선형 패턴을, Pair-Neighbor가 국소 유사 프로필을 보완하는 구조를 검증합니다. | Fold-local 전처리와 재현 가능한 실험 기록을 바탕으로 개인 실험을 팀의 공통 근거로 축적합니다. |

<p align="center">
  <sub>이미지는 연구 흐름만 표현하고, 모델명·수치·설명은 README 텍스트로 분리해 이후 결과 변경에도 재사용할 수 있도록 구성했습니다.</sub>
</p>

<a href="#baseline" aria-label="최종 결과 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="baseline"></a>

<a href="#baseline" aria-label="최종 모델 결과 섹션">
  <img src="./assets/section-baseline.svg" width="100%" alt="02 Final Result — final adopted hybrid model" />
</a>

<p align="center">
  <a href="#workflow" aria-label="연구 워크플로로 이동">
    <img src="./assets/final-architecture.svg" width="100%" alt="건강 신호가 ExtraTrees와 Pair-Neighbor 두 분기로 흐른 뒤 블렌드와 근접중복 보정을 거쳐 최종 예측으로 합쳐지는 애니메이션" />
  </a>
</p>

<p align="center">
  <strong>Final adopted model · BS 8/6</strong><br />
  <code>ExtraTrees × 1,200</code> · <code>Tree Q=0.54</code><br />
  <code>Pair-Neighbor 8 features / 28 pairs</code> · <code>Pair Q=0.48</code><br />
  <code>Blend 76:24</code> · <code>Near-duplicate override &lt; 0.2</code><br />
  <strong>Public MAE 0.1266866667</strong> · Private MAE 0.1473
</p>

<p align="center">
  <sub>최종 발표에서는 Public 최저값만이 아니라 내부 검증과 Private 결과까지 확인된 모델을 최종 채택했습니다.</sub>
</p>

<a href="#workflow" aria-label="워크플로 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="workflow"></a>

<a href="#workflow" aria-label="워크플로 섹션">
  <img src="./assets/section-workflow.svg" width="100%" alt="03 Workflow — From health data to final validation" />
</a>

<p align="center">
  <a href="#principles" aria-label="연구 원칙으로 이동">
    <img src="./assets/final-workflow.svg" width="100%" alt="건강 데이터가 Train 기반 전처리, 파생변수, 하이브리드 모델링, 검증과 최종 선택으로 이어지는 5단계 애니메이션" />
  </a>
</p>

| 01 Data | 02 Preprocess | 03 Features | 04 Hybrid Model | 05 Validate |
|---|---|---|---|---|
| 신체·건강·생활 데이터 | Train 기준 결측·인코딩 | BMI·혈압·대사·결측 파생 | ExtraTrees + Pair-Neighbor | CV·Public·Private 근거 종합 |

<details>
<summary><strong>5-step workflow details</strong></summary>

1. **Data** — Train 3,000건 × 18개 컬럼에서 `stress_score`를 학습하고, Test 3,000건 × 17개 컬럼의 점수를 예측합니다.
2. **Preprocess** — 수치형 결측은 Train 중앙값, 범주형 결측은 `missing` 범주로 처리하고 One-Hot Encoding 기준도 Train에서만 학습합니다.
3. **Features** — BMI, 맥압, 평균동맥압, 혈압 비율, 콜레스테롤·혈당 비율, 결측치 개수를 만들고 중요 피처 선택 기회를 높입니다. 최종 모델에서는 `gender` 제거와 Fold-local Winsorization도 적용합니다.
4. **Hybrid Model** — ExtraTrees 1,200개의 54% 분위수와 8개 피처·28개 Pair-Neighbor의 48% 분위수를 `76:24`로 결합하고, 거리 `< 0.2`의 근접중복은 최근접 Train 타깃으로 보정합니다.
5. **Validate & Select** — 내부 CV와 실제 Public·Private 결과를 함께 확인합니다. Public `0.1265`의 Fresh V6보다 검증 근거가 완전한 **8월 6일 통합모델**을 최종 채택했습니다.

</details>

<a href="#principles" aria-label="연구 원칙 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="principles"></a>

<a href="#principles" aria-label="연구 원칙 섹션">
  <img src="./assets/section-principles.svg" width="100%" alt="04 Principles — Evidence before leaderboard" />
</a>

<p align="center">
  <a href="#team" aria-label="팀 섹션으로 이동">
    <img src="./assets/final-principles.svg" width="100%" alt="Train 기준 전처리, 데이터 누수 방지, 고정 설정 재현성, 검증 근거 기반 최종 선택을 표현한 애니메이션" />
  </a>
</p>

| 01 Train-only | 02 No Leakage | 03 Reproducible | 04 Evidence-based |
|---|---|---|---|
| 전처리 기준은 Train에서 학습 | Test 전체 통계를 모델 선택에 사용하지 않음 | 고정 설정과 실행 기록을 남김 | 한 번의 점수보다 CV·Public·Private 근거를 함께 확인 |

<p align="center">
  <strong>좋은 점수보다 먼저, 같은 조건에서 다시 확인할 수 있는 결과를 남깁니다.</strong><br />
  <sub>최종 모델 역시 Public 최저값 하나가 아니라 재현 가능한 내부 검증과 Private 결과까지 확인한 뒤 선택했습니다.</sub>
</p>

<details>
<summary><strong>Research & disclosure policy</strong></summary>

- 수치형 결측값, 범주형 인코딩, Winsorization과 Rank 기준은 해당 Train 범위에서만 계산합니다.
- Test 전체 분포나 다른 Test 행의 정보를 이용해 모델이나 하이퍼파라미터를 선택하지 않습니다.
- 주요 모델 설정과 난수 시드를 고정하고 Notebook·GitHub 기록을 남겨 재현 가능성을 확보합니다.
- Public 점수만으로 후보를 승격하지 않고 내부 CV, 안정성, 실제 Public·Private 근거를 구분해 해석합니다.
- 원본 대회 데이터, 제출 CSV와 비공개 학습 산출물은 공개하지 않습니다.
- 공개 코드에는 비밀키와 개인 식별 정보를 포함하지 않습니다.

</details>

<a href="#team" aria-label="팀 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="team"></a>

<a href="#team" aria-label="팀 섹션">
  <img src="./assets/section-team.svg" width="100%" alt="05 Team — Three roles, one final model" />
</a>

<p align="center">
  <a href="#repositories" aria-label="연구 저장소 지도로 이동">
    <img src="./assets/final-team.svg" width="100%" alt="세 연구자가 서로 다른 역할의 연구 흐름을 하나의 공통 근거와 최종 모델로 연결하는 애니메이션" />
  </a>
</p>

| 김지현 · 팀장 | 박빛샘 | 안상균 |
|---|---|---|
| 프로젝트 일정 조율 · 파생변수 · 모델 개선 | 발표 자료 제작 · ExtraTrees · 분위수 조정 | GitHub·Notion 관리 · 대안 모델 · 튜닝 |

<p align="center">
  <strong>가설 공유 → 개별 실험 → 결과 비교 → 효과가 확인된 개선안 축적</strong><br />
  <sub>Notion과 ZEP으로 소통하고, GitHub 저장소를 통해 코드·설정·실험 결과를 공유했습니다.</sub>
</p>

<a href="#repositories" aria-label="연구 저장소 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="repositories"></a>

<a href="#repositories" aria-label="연구 저장소 섹션">
  <img src="./assets/section-repositories.svg" width="100%" alt="06 Repositories — Four research nodes, one shared lineage" />
</a>

<p align="center">
  <a href="#status" aria-label="실험 현황으로 이동">
    <img src="./assets/final-repositories.svg" width="100%" alt="JH, BS, SK의 세 연구 노드가 UNIFIED 공통 계보 허브로 연결되는 애니메이션" />
  </a>
</p>

| Repository | 역할 | 현재 접근 |
|---|---|---|
| `stress_project_JH` | Team V7 · Pair-Neighbor와 팀 기준 계보 | Private |
| `stress_project_BS` | 최종 BS 8/6 · ExtraTrees/Pair 고도화 · 발표자료 | Private |
| `stress_project_SK` | 대안 모델 · 강건성 검증 · 연구 엔진 기록 | Private |
| `stress_project_UNIFIED` | 대표 모델 계보 · 점수 · 팀 공통 허브 | Private |

<p align="center">
  <strong>개별 연구는 분리하고, 확인된 계보와 결과는 UNIFIED에서 연결합니다.</strong><br />
  <sub>네 저장소는 현재 모두 Private이며, 접근 권한이 있는 팀원에게만 표시됩니다. 공개 전환 시점은 이 README에서 미리 약속하지 않습니다.</sub>
</p>

<a href="#status" aria-label="실험 현황 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="status"></a>

<a href="#status" aria-label="실험 현황 섹션">
  <img src="./assets/section-status.svg" width="100%" alt="07 Experiment Status — Final research snapshot" />
</a>

<p align="center">
  <a href="#top" aria-label="페이지 상단으로 이동">
    <img src="./assets/final-status.svg" width="100%" alt="Team V7과 BS V34가 최종 BS 8/6 모델로 이어지고, P56C Gower와 Fresh V6가 별도 판단 분기로 보존되는 최종 연구 상태 애니메이션" />
  </a>
</p>

| 모델 | 내부 검증 | Public MAE | 상태 |
|---|---:|---:|---|
| Team V7 Pair-Neighbor | 0.146644 | 0.1272333333 | 계보 이정표 |
| BS V34 Tree·Pair Joint Tuning | 0.148033 | 0.1271866667 | 계보 이정표 |
| **BS 8/6 Final Integrated Model** | **0.147300** | **0.1266866667** | **최종 채택 · Private 0.1473** |
| P56C MI-weighted Gower | Robust CV 0.149096 | 0.130060 | 독립 모델 · 보존 |
| Fresh V6 | — | **0.1265** | 미채택 · 내부/Private 검증 기록 없음 |

<p align="center">
  <strong>Final research snapshot · 2026-08-08</strong><br />
  <sub>내부 MAE는 모델별 split·seed·검증 계약이 다를 수 있어 작은 차이를 직접 순위화하지 않습니다. 최종 채택은 재현 가능한 내부 검증과 Public·Private 근거를 함께 고려했습니다.</sub>
</p>

<a href="#top" aria-label="페이지 상단으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<p align="center">
  <a href="https://github.com/thisisstress" aria-label="thisisstress organization overview">
    <img src="./assets/brand-footer.gif" width="100%" alt="thisisstress animated brand footer" />
  </a>
</p>

<p align="center">
  <sub>Click the footer to return to the organization overview.</sub>
</p>