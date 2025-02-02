# Insnugram Backend
![GitHub Open PRs](https://img.shields.io/github/issues-pr/wafflestudio/22-5-team9-web?label=open%20PRs&color=blue&style=flat-square)
![GitHub Closed PRs](https://img.shields.io/github/issues-pr-closed/wafflestudio/22-5-team9-web?label=closed%20PRs&color=green&style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/wafflestudio/22-5-team9-web?color=yellow&style=flat-square)
<p align="center">
    <img src="https://github.com/user-attachments/assets/53c84466-5fbf-4b62-93f5-0eef6af74472" alt="Insugram" width=300/>
</p>
<p align="center">
    <img width="182" alt="image" src="https://github.com/user-attachments/assets/49bbb46f-20f3-47c8-804e-dac8b7124caa"/>
</p>

## 📌 프로젝트 소개

**Insnugram**은 WaffleStudio의 22-5기 9팀의 인스타그램 서버 클론 코딩 프로젝트입니다. 인스타그램이 소셜 네트워크 서비스로서 가지고 있는 역할을 고려하며 재현했습니다. 인스트그램과 같이 주요 기능으로 포스트와 팔로우가 있으며, 추가로 스토리, 하이라이트, 탐색, 검색, DM까지 구현했습니다! 
<br><br>인스누그램만의 유니크한 추가 기능으로 공유 하이라이트와 유저 위치 태그를 개발했습니다. 두 추가 기능은 인스타그램의 Socialize 목적에 맞춰 고안하였습니다. 
- 공유 하이라이트란 말 그대로 하이라이트를 친구와 공유하여 함께 추억 저장소를 만들고, 수정할 수 있는 기능입니다.
- 위치 태그는 스누 캠퍼스에 있는 유저들이 위치를 지정하여 근처에 있는 친구들을 볼 수 있는 기능입니다.

## 🚀 기술 스택

### **백엔드 프레임워크**
<div>
    <a href="https://fastapi.tiangolo.com/">
        <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
    </a>
    <a href="https://www.uvicorn.org/">
        <img src="https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white"/>
    </a>
</div>

### **데이터베이스**
<div>
    <a href="https://www.mysql.com/">
        <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/>
    </a>
</div>

### **인프라**
<div>
    <a href="https://aws.amazon.com/ec2/">
        <img src="https://img.shields.io/badge/AMAZON%20EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white"/>
    </a>
    <a href="https://aws.amazon.com/rds/">
        <img src="https://img.shields.io/badge/AMAZON%20RDS-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white"/>
    </a>
</div>

### **인증**
<div>
    <a href="https://developers.google.com/identity/sign-in/web/sign-in">
        <img src="https://img.shields.io/badge/Google%20OAuth-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
    </a>
</div>

### **커뮤니케이션**
<div>
    <a href="https://slack.com/">
        <img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white"/>
    </a>
    <a href="https://www.notion.so/">
        <img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white"/>
    </a>
</div>

## 

## 📂 프로젝트 구조

```bash
📦 22-5-team9-server
├── 📂 instaclone            # 주요 애플리케이션 코드
│   ├── 📂 app               # FastAPI 엔드포인트
│   │   ├── 📂 auth          # 소셜 로그인
│   │   ├── 📂 comment       # 댓글
│   │   ├── 📂 dm            # 메시지
│   │   ├── 📂 follower      # 팔로우
│   │   ├── 📂 like          # 좋아요
│   │   ├── 📂 location      # 위치 태그 (추가 기능)
│   │   ├── 📂 medium        # 미디어
│   │   ├── 📂 post          # 게시물
│   │   ├── 📂 story         # 스토리 + 하이라이트 + 공유하이라이트 (추가 기능)
│   │   └── 📂 user          # 유저
│   ├── 📂 common            # error + util
│   ├── 📂 database          # DB 설정 및 모델
│   ├── 🐍 api.py
│   ├── 🐍 main.py
│   └── 🐍 settings.py
├── 💲 .env.prod             # 배포환경설정
├── 📜 poetry.lock           # 패키지 관리
└── 📜 pypoetry.toml         # 패키지 관리
```

## 👩🏻‍💻👩🏻‍💻🧑🏻‍💻🧑🏻‍💻 개발진
<div>
    <a href="https://github.com/cloNoey">
        <img src="https://custom-icon-badges.demolab.com/badge/cloNoey-곽승연-F8991D?style=for-the-badge&logo=person-fill&logoColor=white"/>
    </a>
</div>

### 구현 기능
- Initialize Database
- Social Login
- Follow
- Like
- Location Tag (추가기능)
- 각종 오류 해결
<br>
<div>
    <a href="https://github.com/dida0423">
        <img src="https://custom-icon-badges.demolab.com/badge/dida0423-김다인-DEF81D?style=for-the-badge&logo=person-fill&logoColor=white"/>
    </a>
</div>

### 구현 기능
- User
- Post
- Explore
- Integrate Story & Medium
- Highlight
- Shared Highlights (추가기능)
- 각종 오류 해결
<br>
<div>
    <a href="https://github.com/MunJaeyoung">
        <img src="https://custom-icon-badges.demolab.com/badge/MunJaeyoung-문재영-1DC9F8?style=for-the-badge&logo=person-fill&logoColor=white"/>
    </a>
</div>

### 구현 기능
- Initialize Project
- Login
- DM
- Story
- Comment
- 각종 오류 해결
<br>
<div>
    <a href="https://github.com/b1lly13">
        <img src="https://custom-icon-badges.demolab.com/badge/b1lly13-최성환-A81DF8?style=for-the-badge&logo=person-fill&logoColor=white"/>
    </a>
</div>

### 구현 기능
- ER Diagram
- Post
- Medium
- Story Views
- User Search
- 각종 오류 해결
<br>

## 🔗 배포 링크
<div>
    <a href="https://d3l72zsyuz0duc.cloudfront.net/"/>
        <img width="203" alt="image" src="https://github.com/user-attachments/assets/76ff852d-d2a0-493d-aace-485a981ab411" alt="Front"/>
    </a>
</div>
<div>
    <a href="https://waffle-instaclone.kro.kr/docs"/>
        <img width="203" alt="image" src="https://github.com/user-attachments/assets/2be0625f-6238-4101-a535-cfb32f4c9da9" alt="Back"/>
    </a>
</div>
