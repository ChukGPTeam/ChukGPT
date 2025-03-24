| 목적 | 명령어 | 설명 |
|------|--------|------|
| 브랜치 목록 보기 | `git branch` | 로컬 브랜치 목록 확인 |
| 원격 브랜치 보기 | `git branch -r` | origin/* 목록 확인 |
| 브랜치 전환 | `git switch dev` | dev 브랜치로 이동 (Git 2.23+) |
| 브랜치 생성 + 이동 | `git switch -c feature/name` | 새 브랜치 생성 후 이동 |
| 브랜치 삭제 | `git branch -d feature/name` | 병합된 브랜치 삭제 |
| 원격 브랜치 삭제 | `git push origin --delete feature/name` | GitHub 브랜치 삭제 |
