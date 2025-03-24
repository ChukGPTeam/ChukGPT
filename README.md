| 목적 | 명령어 | 설명 |
|------|--------|------|
| 로컬 브랜치 보기 | `git branch` | 로컬 브랜치 목록 확인 |
| 원격 브랜치 보기 | `git branch -r` | origin/* 목록 확인 |
| 브랜치 이동 | `git switch dev` | checkout과 같지만 이거 쓰셈 |
| 브랜치 생성 + 이동 | `git switch -c feature/name` | -c는 create |
| 브랜치 삭제 | `git branch -d feature/name` | 병합된 브랜치 삭제 |
| 원격 브랜치 삭제 | `git push origin --delete feature/name` | 이거 쓸바에 사이트에서 지우는게 편함 |
