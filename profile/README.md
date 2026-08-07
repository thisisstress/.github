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
  <a href="#baseline"><img src="./assets/nav-baseline.svg" width="112" alt="Current result" /></a><br />
  <a href="#workflow"><img src="./assets/nav-workflow.svg" width="112" alt="Workflow" /></a>
  <a href="#principles"><img src="./assets/nav-principles.svg" width="112" alt="Principles" /></a>
  <a href="#team"><img src="./assets/nav-team.svg" width="112" alt="Team" /></a><br />
  <a href="#repositories"><img src="./assets/nav-repositories.svg" width="112" alt="Repositories" /></a>
  <a href="#status"><img src="./assets/nav-status.svg" width="112" alt="Experiment status" /></a>
</p>

<a href="#baseline" aria-label="최종 모델 결과로 이동">
  <img src="./assets/metrics-current.svg" width="100%" alt="animated ExtraTrees and Pair-Neighbor metrics" />
</a>

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
  <a href="#baseline" aria-label="현재 확인 결과로 이동">
    <img src="./assets/research-visual.svg" width="100%" alt="animated flow from health signals to hybrid modeling and shared evidence" />
  </a>
</p>

| Health signals | Hybrid modeling | Shared evidence |
|---|---|---|
| BMI, 맥압, 평균동맥압, 콜레스테롤·혈당 비율과 결측 패턴처럼 원본 건강 데이터를 더 의미 있게 표현합니다. | ExtraTrees가 전역 비선형 패턴을, Pair-Neighbor가 국소 유사 프로필을 보완하는 구조를 검증합니다. | Fold-local 전처리와 재현 가능한 실험 기록을 바탕으로 개인 실험을 팀의 공통 근거로 축적합니다. |

<p align="center">
  <sub>이미지는 연구 흐름만 표현하고, 모델명·수치·설명은 README 텍스트로 분리해 이후 결과 변경에도 재사용할 수 있도록 구성했습니다.</sub>
</p>

<a href="#baseline" aria-label="현재 결과 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="baseline"></a>

<a href="#baseline" aria-label="현재 확인된 모델 결과 섹션">
  <img src="./assets/section-baseline.svg" width="100%" alt="02 Current Result — ExtraTrees and Pair-Neighbor" />
</a>

<p align="center">
  <a href="#workflow" aria-label="연구 워크플로로 이동">
    <img src="./assets/baseline-architecture.gif" width="100%" alt="animated ExtraTrees and Pair-Neighbor architecture" />
  </a>
</p>

<p align="center">
  <strong>Current verified public result · final publication pending</strong><br />
  <code>ExtraTrees × 1,200</code> · <code>Pair-Neighbor 8 features / 28 pairs</code><br />
  <code>Tree Q=0.54</code> · <code>Pair Q=0.48</code> · <code>Blend 76:24</code><br />
  <strong>Public MAE 0.1266866667</strong>
</p>

<a href="#workflow" aria-label="워크플로 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="workflow"></a>

<a href="#workflow" aria-label="워크플로 섹션">
  <img src="./assets/section-workflow.svg" width="100%" alt="03 Workflow — From data to validated evidence" />
</a>

<p align="center">
  <a href="#principles" aria-label="연구 원칙으로 이동">
    <img src="./assets/pipeline.gif" width="100%" alt="animated research workflow" />
  </a>
</p>

<details>
<summary><strong>5-step workflow details</strong></summary>

1. **Data** — Train에서만 결측치 처리와 인코딩 기준을 학습합니다.
2. **Features** — BMI, 맥압, 평균동맥압, 대사 비율과 결측 패턴을 구성합니다.
3. **Models** — ExtraTrees는 전역 비선형 패턴을, Pair-Neighbor는 국소 유사 프로필을 학습합니다.
4. **Aggregation** — Tree 54% 분위수와 Pair 48% 분위수를 `76:24`로 결합합니다.
5. **Validation** — Fold-local 처리와 반복 검증으로 개선의 재현성을 확인합니다.

</details>

<a href="#principles" aria-label="연구 원칙 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="principles"></a>

<a href="#principles" aria-label="연구 원칙 섹션">
  <img src="./assets/section-principles.svg" width="100%" alt="04 Principles — Rules that protect reproducibility" />
</a>

<a href="#team" aria-label="팀 섹션으로 이동">
  <img src="./assets/principles.gif" width="100%" alt="animated research principles" />
</a>

<details>
<summary><strong>Public profile policy</strong></summary>

이 프로필에는 **재현 가능한 연구 방법, 모델 구조, 검증 원칙과 공개 가능한 결과**만 게시합니다.

- 원본 대회 데이터는 공개하지 않습니다.
- 제출 CSV와 학습 산출물은 공개하지 않습니다.
- 공개가 허용된 성능 기록만 게시합니다.
- 공개 코드에는 비밀키와 개인 식별 정보를 포함하지 않습니다.

</details>

<a href="#team" aria-label="팀 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="team"></a>

<a href="#team" aria-label="팀 섹션">
  <img src="./assets/section-team.svg" width="100%" alt="05 Team — Three researchers, one shared model" />
</a>

<p align="center">
  <a href="#repositories" aria-label="연구 저장소 지도로 이동">
    <img src="./assets/team-network.gif" width="100%" alt="animated thisisstress team network" />
  </a>
</p>

<p align="center">
  <strong>김지현 · 박빛샘 · 안상균</strong><br />
  <sub>3 researchers · shared evidence · final publication pending</sub>
</p>

<a href="#repositories" aria-label="연구 저장소 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="repositories"></a>

<a href="#repositories" aria-label="연구 저장소 섹션">
  <img src="./assets/section-repositories.svg" width="100%" alt="06 Repositories — Research workspace map" />
</a>

<p align="center">
  <a href="#status" aria-label="실험 현황으로 이동">
    <img src="./assets/repository-map.gif" width="100%" alt="animated private research repository map" />
  </a>
</p>

<p align="center">
  <sub>Research repositories remain private until the competition and disclosure policy allow a public release.</sub>
</p>

<a href="#status" aria-label="실험 현황 섹션으로 이동">
  <img src="./assets/section-spacer.svg" width="100%" alt="" />
</a>

<a id="status"></a>

<a href="#status" aria-label="실험 현황 섹션">
  <img src="./assets/section-status.svg" width="100%" alt="07 Experiment Status — Current research snapshot" />
</a>

<p align="center">
  <a href="#top" aria-label="페이지 상단으로 이동">
    <img src="./assets/experiment-status.gif" width="100%" alt="animated experiment registry snapshot" />
  </a>
</p>

<p align="center">
  <sub>
    Current result snapshot: 2026-08-07 ·
    update <code>profile/content.json</code> and regenerate assets when the final publication is fixed.
  </sub>
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