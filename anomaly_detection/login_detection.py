import pandas as pd                               # 판다스를 pd 라는 짧은 이름으로 불러온다

EVENTS_PATH = "normalized_events.json"            # 읽을 정규화 이벤트 파일 이름
LOGIN_LIMIT = 5                                   # 알림 기준: 평소 하루 최대가 4번이라 5번 이상이면 알린다


def load_events(path):                            # 파일 경로를 받는 함수
    """이벤트 파일을 표로 읽는다.
    분석을 시작할 때 맨 먼저 쓴다.
    """
    events = pd.read_json(path)                   # 파일 속 이벤트를 표 한 개로 읽는다
    return events                                 # 이벤트 표를 리턴한다


def pick_login_failures(events):                  # 이벤트 표를 받는 함수
    """로그인 요청이 실패한 이벤트만 골라 새 표로 만든다.
    로그인 실패가 많은 주소를 조사하기 전에 쓴다.
    """
    actions = events["action"]           # action 열만 꺼낸다 — 무엇을 했는지가 57개 나열된 열
    is_login = actions == "POST /login"  # 행마다 로그인 요청인지 비교해 True 또는 False 를 만든다
    results = events["result"]           # result 열만 꺼낸다 — 성공 · 실패가 57개 나열된 열
    is_fail = results == "실패"          # 행마다 실패인지 비교해 True 또는 False 를 만든다
    both_true = is_login & is_fail       # is_login & is_fail 로 두 조건을 합친다 (둘 다 True 인 행만 True)
    login_failures = events[both_true]   # events 에서 both_true 가 True 인 행만 고른다
    return login_failures                         # 로그인 실패 이벤트만 담은 표를 리턴한다


def count_by_ip(login_failures):                  # 로그인 실패 표를 받는 함수
    """로그인 실패를 접속 주소별로 센다.
    같은 주소가 반복해서 실패했는지 볼 때 쓴다.
    """
    counts = login_failures.groupby("ip").size()  # ip 가 같은 행끼리 그룹으로 만들고(groupby) 바로 그룹마다 행이 몇 개인지 센다(size)
    return counts                                 # 주소별 실패 횟수를 리턴한다


def pick_alert_ips(counts, limit):                # 주소별 횟수와 알림 기준을 받는 함수
    """실패 횟수가 알림 기준 이상인 주소만 골라 리턴한다.
    알림을 보낼 주소를 가릴 때 쓴다.
    """
    is_many = counts >= limit    # 주소마다 「횟수가 기준 이상인가?」를 물어 True 또는 False 를 만든다
    alert_ips = counts[is_many]  # True 인 주소만 남긴다
    return alert_ips                              # 알림 기준 이상인 주소와 횟수를 리턴한다
