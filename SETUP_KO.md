# thisisstress 조직 프로필 설치 방법

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

## 3. 압축 내용 복사

이 압축파일의 내용을 Clone한 `.github` 폴더에 그대로 복사합니다.

최종 구조:

```text
.github/
├─ profile/
│  ├─ README.md
│  ├─ content.json
│  └─ assets/
├─ scripts/
├─ .github/
│  └─ workflows/
├─ requirements.txt
└─ SETUP_KO.md
```

## 4. 확인 및 Push

```powershell
git status --short
git add .
git commit -m "feat: launch animated organization profile"
git push -u origin main
```

이후 `https://github.com/thisisstress`의 **Overview** 탭에서 공개 프로필을 확인합니다.

## 문구와 수치 수정

`profile/content.json`을 수정합니다.

```json
{
  "public_mae": "0.1282776667",
  "team": ["김지현", "박빛샘", "안상균"]
}
```

수정 후 Push하면 GitHub Actions가 애니메이션을 다시 생성하고 검증합니다.

> `content.json`은 GIF·SVG 생성 데이터입니다. README에 직접 적힌 문구나
> 공개 리포 링크를 바꿀 때에는 `profile/README.md`도 함께 수정하세요.

## 로컬에서 애니메이션 다시 만들기

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\render_assets.py
```

## 비용 방지 원칙

- `.github` 리포는 반드시 Public으로 둡니다.
- Workflow는 소스·설정 변경 때만 실행됩니다.
- Scheduled workflow를 사용하지 않습니다.
- 외부 유료 API, 호스팅, 이미지 CDN을 사용하지 않습니다.
- GIF와 SVG는 모두 리포 자체에서 제공됩니다.

## 공개 리포 Pin

조직 프로필에는 최대 6개의 공개 리포를 Pin할 수 있습니다.
공개 쇼케이스 리포가 생기면 조직 Settings에서 직접 선택하세요.


## 업로드 전 최종 검증

Windows PowerShell:

```powershell
python -m py_compile scripts\render_assets.py scripts\validate_profile.py
python scripts\render_assets.py
python scripts\validate_profile.py
```

정상이라면 다음과 비슷한 결과가 나옵니다.

```text
Profile assets regenerated.
PASS: ... README assets, 8 anchors, ... SVGs, 10 GIFs
```

## 권장 Git 명령어

```powershell
git status --short
git add .
git commit -m "feat: launch thisisstress organization profile"
git push -u origin main
```
