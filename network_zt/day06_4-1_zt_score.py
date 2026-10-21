STAFF = [                                                                      # A사 직원 12명(120명 중 일부)의 정보
    {"name": "u01", "mfa": 개념	설명	Python 비유
이미지(Image)	읽기 전용 설계도	클래스
컨테이너(Container)	이미지를 실행한 인스턴스	객체(인스턴스)
컨테이너 내부 파일	컨테이너 삭제 시 같이 사라짐	메모리 변수
볼륨(Volume)	컨테이너 밖에 저장되는 데이터	파일로 저장한 데이터
Dockerfile	이미지를 만드는 레시피	클래스 정의 코드
레이어(Layer)	이미지는 명령어마다 층이 쌓임, 캐시 재사용됨	없음 (빌드 캐시 개념)
네트워크/포트	컨테이너끼리, 외부와 통신하는 방법	소켓 포트
Compose	여러 컨테이너를 한 번에 정의·실행	설정 파일로 묶어 실행,  "device_ok": True,  "extra_perms": 0},       # MFA 사용, 기기 점검 통과, 초과 권한 0개
    {"name": "u02", "mfa": True,  "device_ok": True,  "extra_perms": 0},       # MFA 사용, 기기 점검 통과, 초과 권한 0개
    {"name": "u03", "mfa": True,  "device_ok": True,  "extra_perms": 0},       # MFA 사용, 기기 점검 통과, 초과 권한 0개
    {"name": "u04", "mfa": True,  "device_ok": False, "extra_perms": 0},       # MFA 사용, 기기 점검 안 받음, 초과 권한 0개
    {"name": "u05", "mfa": True,  "device_ok": False, "extra_perms": 2},       # MFA 사용, 기기 점검 안 받음, 초과 권한 2개
    {"name": "u06", "mfa": True,  "device_ok": False, "extra_perms": 0},       # MFA 사용, 기기 점검 안 받음, 초과 권한 0개
    {"name": "u07", "mfa": False, "device_ok": False, "extra_perms": 0},       # MFA 안 씀, 기기 점검 안 받음, 초과 권한 0개
    {"name": "u08", "mfa": False, "device_ok": False, "extra_perms": 0},       # MFA 안 씀, 기기 점검 안 받음, 초과 권한 0개
    {"name": "u09", "mfa": False, "device_ok": False, "extra_perms": 1},       # MFA 안 씀, 기기 점검 안 받음, 초과 권한 1개
    {"name": "u10", "mfa": False, "device_ok": False, "extra_perms": 0},       # MFA 안 씀, 기기 점검 안 받음, 초과 권한 0개
    {"name": "u11", "mfa": False, "device_ok": False, "extra_perms": 0},       # MFA 안 씀, 기기 점검 안 받음, 초과 권한 0개
    {"name": "u12", "mfa": False, "device_ok": False, "extra_perms": 3},       # MFA 안 씀, 기기 점검 안 받음, 초과 권한 3개
]
SEGMENTED = False                                            # 네트워크를 작은 구역으로 나누었는가(마이크로 세그멘테이션). 아직 아니다
RISK_AUTH = False                                            # 위험 기반 인증을 쓰는가. 아직 아니다

mfa_count = 0                                                # MFA 를 쓰는 직원 수를 세는 변수
device_count = 0                                             # 기기 점검을 통과한 직원 수를 세는 변수
least_count = 0                                              # 초과 권한이 없는 직원 수를 세는 변수
for person in STAFF:                                         # 직원을 한 명씩 꺼낸다
    if person["mfa"] == True:                                # MFA 를 쓰는 직원이면
        mfa_count = mfa_count + 1                            # 1명 늘린다
    if person["device_ok"] == True:                          # 기기 점검을 통과한 직원이면
        device_count = device_count + 1                      # 1명 늘린다
    if person["extra_perms"] == 0:                           # 초과 권한이 없는 직원이면
        least_count = least_count + 1                        # 1명 늘린다

mfa_score = round(mfa_count/12 *20)                                                # MFA 적용률 점수. 0 을 계산식으로 바꾼다 (1줄)   # ←

device_score = round(device_count / 12 * 20)                                             # 기기 보안 점검 비율 점수. 0 을 계산식으로 바꾼다 (1줄)   # ←

least_score = round(least_count / 12 * 20)                                              # 최소권한 준수율 점수. 0 을 계산식으로 바꾼다 (1줄)   # ←

seg_score = 0                                                # 세그멘테이션 점수는 0 점에서 시작한다

if SEGMENTED:                                                # 세그멘테이션을 적용했으면
    seg_score = 20                                           # 20 점을 준다
risk_score = 0                                               # 위험 기반 인증 점수는 0 점에서 시작한다
if RISK_AUTH:                                                # 위험 기반 인증을 적용했으면
    risk_score = 20                                          # 20 점을 준다
total = mfa_score+device_score+least_score+seg_score+risk_score                                                    # 총점. 0 을 다섯 점수의 합으로 바꾼다 (1줄)   # ←

print("MFA", mfa_score, "/ 기기", device_score, "/ 최소권한", least_score, "/ 세그멘테이션", seg_score, "/ 위험기반인증", risk_score)   # 항목별 점수를 출력한다
print("총점", total, "/ 100")                                 # 총점을 출력한다
