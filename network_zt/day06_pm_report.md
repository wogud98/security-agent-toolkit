# Day 6 Docker ① · nginx 서버 · 오후 (김재형 · 2026-10-19)

> **쓰는 법**
> - 문제를 하나 풀 때마다 그 문제 제목 아래를 채웁니다.
> - 질문마다 `쓸 내용:` 에 **무엇을 쓰면 되는지** 적혀 있습니다. 그 내용대로 `답:` 뒤에 씁니다.
> - 「왜 그럴까요?」 같은 질문은 한 단어로 끝내지 말고, 내 화면에서 본 값이나 배운 내용을 근거로 이유까지 씁니다.
> - 🔍 는 그 교시에 꼭 알아야 할 핵심 질문입니다. 답을 못 찾았으면 「모름 — 막힌 곳: …」 이라고 씁니다.

---

## 5교시 · 왜 도커인가 · 이미지와 컨테이너 · 같이 설치하기

### 문제 5-1 · 설치를 확인하고 첫 컨테이너 실행하기

- (가) `docker --version` 으로 나온 값을 적어 주세요.
  - 쓸 내용: 「Docker version … build …」 한 줄
  - 답:
```bash
Client:
Version:           29.8.2
API version:       1.56
Go version:        go1.26.8
Git commit:        7fc2dff
Built:             Wed Sep 30 19:35:42 2026
OS/Arch:           windows/amd64
Context:           desktop-linux

Server: Docker Desktop 4.95.0 (242831)
Engine:
Version:          29.8.2
API version:      1.56 (minimum version 1.40)
Go version:       go1.26.8
Git commit:       8af9fe3
Built:            Wed Sep 30 19:32:25 2026
OS/Arch:          linux/amd64
Experimental:     false
containerd:
Version:          v2.3.6
GitCommit:        ee2735368117d2eb259779949d5e75cdafec9761
runc:
Version:          1.5.1
GitCommit:        v1.5.1-0-g8f2685a4
docker-init:
Version:          0.19.0
GitCommit:        de40ad0
```
- (나) 🔍 `docker run hello-world` 출력이 말하는 일의 순서를 5.5 그림의 번호(① ~ ④)에 맞춰 설명해 주세요.
  - 쓸 내용: ① ~ ④ 번호마다 한 일 (클라이언트 · 엔진 · Do개념	설명	Python 비유
이미지(Image)	읽기 전용 설계도	클래스
컨테이너(Container)	이미지를 실행한 인스턴스	객체(인스턴스)
컨테이너 내부 파일	컨테이너 삭제 시 같이 사라짐	메모리 변수
볼륨(Volume)	컨테이너 밖에 저장되는 데이터	파일로 저장한 데이터
Dockerfile	이미지를 만드는 레시피	클래스 정의 코드
레이어(Layer)	이미지는 명령어마다 층이 쌓임, 캐시 재사용됨	없음 (빌드 캐시 개념)
네트워크/포트	컨테이너끼리, 외부와 통신하는 방법	소켓 포트
Compose	여러 컨테이너를 한 번에 정의·실행	설정 파일로 묶어 실행cker Hub · 컨테이너)
  - 답:
```bash
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
  
① 클라이언트 → 엔진: Docker 클라이언트가 Docker 데몬에 hello-world 실행을 요청한다. (Python 비유: 객체를 사용하도록 요청)

② 엔진 → Docker Hub: 엔진이 로컬에 이미지가 없어 Docker Hub에서 이미지를 내려받는다. (이미지 = 클래스, Docker Hub = 클래스 설계도를 내려받는 저장소)

③ 엔진 → 컨테이너: 엔진이 이미지로 컨테이너를 생성하고 실행 파일을 실행한다. (컨테이너 = 클래스에서 생성한 객체·인스턴스)

④ 컨테이너 → 엔진 → 클라이언트: 실행 결과가 엔진을 거쳐 클라이언트에 전달되고 터미널에 출력된다. (컨테이너의 실행 결과를 호출한 쪽에 반환하는 과정)
```

- (다) 🔍 `docker images` 에 보인 것과 `docker ps -a` 에 보인 것은 각각 이미지와 컨테이너 중 무엇이고, 어떻게 다른가요?
  - 쓸 내용: ① images 에 보인 것과 그 종류 ② ps -a 에 보인 것과 그 종류 ③ 둘의 차이
  - 답: docker images 에 보인 hello-world 는 이미지입니다. 받아 둔 읽기 전용 묶음이고 컨테이너를 지워도 남습니다. docker ps -a 에서 IMAGE 열이 hello-world 인 줄은 컨테이너입니다. 그 이미지를 실행한 것이고 글자를 출력한 뒤 끝나서 Exited 로 남습니다. NAMES 열의 무작위 이름은 도커가 붙인 컨테이너 이름입니다.

- (라) 🔍 `docker images` 출력을 붙여 넣고, `hello-world` 줄의 `IMAGE` · `ID` · `EXTRA` 값과 각각의 뜻을 적어 주세요.
  - 쓸 내용: ① 출력 ② `IMAGE` · `ID` · `EXTRA` 의 값과 뜻
  - 답: 
IMAGE 는 hello-world:latest 로, 이미지 이름 hello-world 와 태그 latest 입니다. 태그를 안 쓰고 받아서 latest 가 붙었습니다.
ID 는 11a3eb1597e8 처럼 이미지의 고유 번호입니다. 같은 이미지는 어느 PC 에서나 같은 번호입니다.
EXTRA 의 U 는 이 이미지로 만든 컨테이너(꺼진 hello-world 컨테이너)가 있다는 뜻입니다.

```bash
$ docker images
                                                                                          i Info →   U  In Use
IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
hello-world:latest   11a3eb1597e8       25.9kB         9.49kB    U   
```

- (마) 🔍 `docker ps -a` 출력을 붙여 넣고, `hello-world` 줄의 `STATUS` · `PORTS` · `NAMES` · `IMAGE` 값과 각각의 뜻을 적어 주세요.
  - 쓸 내용: ① 출력 ② `STATUS` · `PORTS` · `NAMES` · `IMAGE` 의 값과 뜻
  - 답: 
1 STATUS 는 Exited (0) … 으로, 글자를 출력하고 정상으로 끝났다는 뜻입니다. 괄호 안 0 은 오류 없이 끝났다는 번호입니다.
2 PORTS 는 비어 있습니다. 내 PC 와 연결된 포트가 없다는 뜻입니다.
3 NAMES 는 festive_curie 같은 무작위 이름입니다. --name 을 주지 않아 도커가 붙였습니다. 이 컨테이너를 지울 때 docker rm festive_curie 처럼 이 이름을 씁니다.
4 IMAGE 는 hello-world 로, 이 컨테이너가 hello-world 이미지로 만들어졌다는 뜻입니다.
```bash
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                     PORTS     NAMES
b374084152c3   hello-world   "/hello"   9 minutes ago    Exited (0) 5 minutes ago             pedantic_hoover
ae177fcaf4d8   hello-world   "/hello"   9 minutes ago    Exited (0) 5 minutes ago             sad_jones
0e7b301db008   hello-world   "/hello"   10 minutes ago   Exited (0) 6 minutes ago             boring_khayyam
e3bd3d8ed2cb   hello-world   "/hello"   11 minutes ago   Exited (0) 6 minutes ago             condescending_pasteur
4d61df87b021   hello-world   "/hello"   11 minutes ago   Exited (0) 7 minutes ago             keen_hertz
```


### 문제 5-2 · Docker Hub 에서 이미지 이름 읽고 없는 이미지 받아 보기

- (가) `nginx:1.28` 에서 `nginx` 와 `1.28` 이 각각 무엇을 정하는지 적어 주세요.
  - 쓸 내용: ① nginx 가 정하는 것 ② 1.28 이 정하는 것
  - 답: *nginx 는 이미지 이름(어떤 프로그램인가)을 정하고, 1.28 은 태그(어느 버전인가)를 정합니다. 태그를 안 쓰면 latest(최신)가 선택돼 시기마다 버전이 달라질 수 있어서, 같은 서버를 만들려면 nginx:1.28 처럼 태그를 씁니다.*
  
- (나) 🔍 `docker pull nginxx` 를 쳤을 때 나온 오류 문구와 그 뜻을 적어 주세요.
  - 쓸 내용: ① 오류 문구 ② 뜻 ③ 고치는 방법
  - 답: pull access denied for nginxx, repository does not exist or may require 'docker login' 입니다. 뜻은 「nginxx 라는 이미지는 Docker Hub 에 없거나, 있어도 로그인해야 받을 수 있다」입니다. 이름의 오타이므로 nginx 로 고쳐 씁니다.

```bash
Using default tag: latest
Error response from daemon: pull access denied for nginxx, repository does not exist or may require 'docker login'
```

- (한 줄) 보안 담당에게 보낼 답을 한 문장으로 적어 주세요.
  - 쓸 내용: 보안 담당이 바로 읽을 수 있는 한 문장(도커를 쓰면 무엇이 같아지는지)
  - 답: 도커는 같은 이미지를 받아 실행하므로 어느 PC에서나 같은 서버를 똑같이 띄울 수 있고, 이미지 이름과 태그를 정확히 써야 합니다

- 이 교시에서 새로 알게 된 것 하나를 적어 주세요.
  - 쓸 내용: 자유롭게
  - 답: Docker란ㅡ 기본 사용

## 6교시 · nginx 서버 켜고 접속 기록 읽기

### 문제 6-1 · 포트 없이 켜 보고, 포트를 연결해 접속하고, 기록 읽기

- (가) 포트 없이 켠 `web` 에 접속했을 때 어떻게 되었는지 적어 주세요.
  - 쓸 내용: 접속했을 때 나온 화면이나 오류와 `docker ps` 의 PORTS 열
  - 답:
- (나) 🔍 `-p 8080:80` 이 하는 일을 내 PC의 포트와 컨테이너의 포트로 나눠 설명해 주세요.
  - 쓸 내용: ① 내 PC 쪽 포트 ② 컨테이너 쪽 포트 ③ 연결이 하는 일
  - 답:
- (다) 🔍 `docker logs web` 출력에서 `GET /` 줄 하나를 붙여 넣고, 접속자 주소 · 시각 · 요청 · 응답 번호를 찾아 적어 주세요.
  - 쓸 내용: ① `GET /` 줄 ② 접속자 주소 · 시각 · 요청 · 응답 번호 네 가지
  - 답:

### 문제 6-2 · 컨테이너 안을 들여다보고, 끄고, 지우기

- (가) 컨테이너 안에서 `ls /usr/share/nginx/html` 로 본 파일 이름을 모두 적고, 그중 브라우저의 첫 화면이 어느 파일인지 적어 주세요.
  - 쓸 내용: ① 파일 이름 모두 ② 첫 화면 파일
  - 답: 
```bash
# ls /usr/share/nginx/html
50x.html  index.html
```

- (나) 🔍 `docker stop web` 뒤에 `docker ps` 와 `docker ps -a` 에 각각 `web` 이 보이나요? 차이를 설명해 주세요.
  - 쓸 내용: ① stop 뒤 ps 에 보이는지 ② ps -a 에 보이는지 ③ 차이의 이유
  - 답: 
  1. docker ps 는 실행 중인 컨테이너만 보여 주므로 web 이 안 보입니다. 
  2. docker ps -a 는 멈춘 것까지 모두 보여 주므로 web 이 Exited 로 보입니다. 끈 컨테이너는 지워지는 것이 아니라 멈춘 채로 남습니다.
```bash
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

$ docker ps -a
CONTAINER ID   IMAGE         COMMAND                   CREATED          STATUS                      PORTS     NAMES
738c2145ab61   nginx:1.28    "/docker-entrypoint.…"   11 minutes ago   Exited (0) 59 seconds ago             web
b374084152c3   hello-world   "/hello"                  43 minutes ago   Exited (0) 43 minutes ago             pedantic_hoover
ae177fcaf4d8   hello-world   "/hello"                  43 minutes ago   Exited (0) 43 minutes ago             sad_jones
0e7b301db008   hello-world   "/hello"                  44 minutes ago   Exited (0) 44 minutes ago             boring_khayyam
e3bd3d8ed2cb   hello-world   "/hello"                  45 minutes ago   Exited (0) 45 minutes ago             condescending_pasteur
4d61df87b021   hello-world   "/hello"                  45 minutes ago   Exited (0) 45 minutes ago             keen_hertz
```


- (다) 🔍 같은 이름으로 다시 `run` 했을 때 나온 오류 문구와, `docker rm` 이 필요한 이유를 적어 주세요.
  - 쓸 내용: ① 오류 문구 ② rm 이 필요한 이유
  - 답:
```bash
Conflict. The container name "/web" is already in use 처럼 나옵니다. 끈 web 이 Exited 로 남아 있어서 같은 이름을 쓸 수 없다는 뜻입니다. docker rm web 으로 지워야 같은 이름으로 다시 만들 수 있습니다.
```
- (한 줄) 보안 담당에게 보낼 답을 한 문장으로 적어 주세요.
  - 쓸 내용: 보안 담당이 바로 읽을 수 있는 한 문장(켜는 명령 · 기록 보는 명령 · 정리 방법)
  - 답: nginx 서버는 docker run -d --name web -p 8080:80 nginx:1.28 로 켜고, 접속 기록은 docker logs web 으로 확인하고, 끌 때는 stop 뒤 rm 으로 지워야 같은 이름을 다시 쓸 수 있습니다

- 이 교시에서 새로 알게 된 것 하나를 적어 주세요.
  - 쓸 내용: 자유롭게
  - 답: *run -d --name -p로 켜고 → logs로 기록 보고 → stop 후 rm으로 정리*

## 7교시 · 내 페이지 연결 · 두 서버 · 올리기

### 문제 7-1 · 컨테이너 안의 변경이 사라지는 것을 보고, 내 폴더를 연결하기

- (가) 컨테이너 안에서 바꾼 뒤 `docker rm -f web` 으로 지우고 다시 켰을 때 화면이 어떻게 되었는지 적어 주세요.
  - 쓸 내용: ① 바꾼 뒤 화면 ② 지우고 다시 켠 뒤 화면
  - 답: *바꾸기 전에는 Welcome to nginx! 와 영어 안내 문장이, 컨테이너 안에서 바꾼 뒤에는 inside 한 단어가 보였습니다. docker rm -f web 으로 지우고 같은 명령으로 다시 켜면, 화면이 inside 에서 원래의 Welcome to nginx! 로 돌아갑니다.* ->> 반영이 되지 않아요

- (나) 🔍 컨테이너 안에서 바꾼 내용이 사라진 이유와, `-v` 로 폴더를 연결하면 무엇이 달라지는지 적어 주세요.
  - 쓸 내용: ① 사라진 이유 ② -v 로 연결하면 달라지는 점
  - 답: 컨테이너는 이미지에서 새로 만들어지고, 지우면 컨테이너 안에서 바꾼 파일도 같이 사라지기 때문.
  다시 켜지면 이미지에 들어있는 원본 파일로 시작함. -v로 내 pc 폴더를 연결하면 파일은 내 pc에 있고, 컨테이너는 그것을 읽기만함! ->> 내 pc에서 고쳐야 반영됨

- (다) 🔍 `MSYS_NO_PATHCONV=1` 없이 `-v` 를 실행했을 때 화면에 무엇이 나왔고 왜 그랬는지 적어 주세요.
  - 쓸 내용: ① 화면에 나온 것 ② 그렇게 된 이유
  - 답:  
  MSYS_NO_PATHCONV=1 없이 실행하면 오류는 나지 않고 Welcome to nginx! 기본 화면이 나옴. 
  Git Bash 가 -v 뒤의 컨테이너 쪽 경로(/usr/share/nginx/html)를 윈도 경로(C:/Program Files/Git/usr/share/nginx/html)로 바꿔서 연결이 엉뚱한 곳에 됐기 때문. 
  ->>앞에 MSYS_NO_PATHCONV=1 을 붙이면 경로를 바꾸지 않아 내 폴더가 연결됨.

### 문제 7-2 · 서버 두 대를 띄워 포트로 구분하고, 파일을 고쳐 바로 반영되는지 보기

- (가) 두 주소(`8080` · `8081`)에서 보이는 화면을 각각 적어 주세요.
  - 쓸 내용: 두 주소의 화면 문구
  - 답:
- (나) 🔍 `docker ps` 의 PORTS 열에서 두 서버를 구분해 주는 것은 무엇인가요?
  - 쓸 내용: PORTS 열에서 서버를 구분하는 값
  - 답:
```bash
CONTAINER ID   IMAGE        COMMAND                   CREATED          STATUS          PORTS                                     NAMES
2b8e5bb3d62f   nginx:1.28   "/docker-entrypoint.…"   6 minutes ago    Up 6 minutes    0.0.0.0:8081->80/tcp, [::]:8081->80/tcp   web-two
6e00ce465388   nginx:1.28   "/docker-entrypoint.…"   14 minutes ago   Up 14 minutes   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   web-one
```
- (다) 🔍 `:ro` 는 무슨 뜻이고, 왜 읽기 전용으로 연결하나요?
  - 쓸 내용: ① :ro 의 뜻 ② 읽기 전용으로 연결하는 이유
  - 답: *:ro 는 read-only(읽기 전용)입니다. 컨테이너가 연결된 폴더를 읽기만 하고 바꾸지 못하게 합니다. 서버에 문제가 생기거나 공격을 받아도 내 PC의 원본 파일을 지우거나 바꿀 수 없어서, 필요한 권한(읽기)만 주는 최소권한과 같은 생각입니다.*

- (한 줄) 보안 담당에게 보낼 답을 한 문장으로 적어 주세요.
  - 쓸 내용: 보안 담당이 바로 읽을 수 있는 한 문장(두 서버를 어떻게 띄웠는지)
  - 답:*안내 웹 페이지 파일은 내 PC에 두고 -v ... :ro 로 연결해 서버 두 대를 8080 · 8081 포트로 띄웠고, 파일을 고치면 서버를 다시 켜지 않아도 반영됩니다.*

- 이 교시에서 새로 알게 된 것 하나를 적어 주세요.
  - 쓸 내용: 자유롭게
  - 답: 내 페이지 연결. 여러 서버는 포트 번호를 구분하여 서버 구분. 읽기모드를 최소권한처럼 활용.

### 문제 7-3 · 오늘 만든 것을 깃허브에 올리기

- (가) `git status` 를 쳤을 때 빨간 목록에 줄이 몇 개였는지, 그 가운데 `.env` · `.venv` 가 있었는지 적어 주세요.
  - 쓸 내용: ① 줄 수 ② .env · .venv 가 있었는지
  - 답: 12개. 없음.
