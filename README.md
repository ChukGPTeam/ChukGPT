| 목적 | 명령어 | 설명 |
|------|--------|------|
| 로컬 브랜치 보기 | `git branch` | 로컬 브랜치 목록 확인 |
| 원격 브랜치 보기 | `git branch -r` | origin/* 목록 확인 |
| 브랜치 이동 | `git switch 브랜치명` | checkout과 같지만 이거 쓰셈 |
| 브랜치 생성 + 이동 | `git switch -c feature/xxx` | -c는 create |
| 로컬 브랜치 삭제 | `git branch -d feature/xxx` | 병합된 브랜치 삭제 |
| 원격 브랜치 삭제 | `git push origin --delete feature/xxx` | 이거 쓸바에 사이트에서 지우는게 편함 |
