import pandas as pd                 # 판다스를 pd 라는 짧은 이름으로 불러온다

LOGIN_PATH = "baseline_logins.csv"  # 지난 7일의 하루 로그인 실패 횟수 파일 이름


def load_daily_failures(path):      # 파일 경로를 받는 함수
    """지난 7일의 하루 로그인 실패 횟수 파일을 표로 읽는다.
    평소 기준을 만들기 전에 맨 먼저 쓴다.
    """
    daily = pd.read_csv(path)       # CSV 파일을 읽어 표로 만든다 — 한 행이 하루
    return daily                    # 하루가 한 행인 표를 리턴한다


def average_failures(daily):        # 표를 받는 함수
    """지난 7일 표 숫자 7개의 평균을 구한다.
    「평소 하루에 몇 번쯤 실패하는가」를 알고 싶을 때 쓴다.
    """
    counts = daily["failed_logins"]  # failed_logins 열만 꺼낸다 — 하루 실패 횟수 7개가 나열된 열
    average = counts.mean()          # 7개의 평균을 구한다
    return average                  # 평균을 리턴한다


def maximum_failures(daily):        # 표를 받는 함수
    """하루 최대 로그인 실패 횟수를 구한다.
    「평소 가장 많았던 날」이 얼마나 많았는지 알고 싶을 때 쓴다.
    """
    counts = daily["failed_logins"]  # failed_logins 열만 꺼낸다 — 하루 실패 횟수 7개가 나열된 열
    maximum = counts.max()           # 7개 중 가장 큰 값을 구한다
    return maximum                  # 최댓값을 리턴한다


def make_limit(maximum):            # 평소 최댓값을 받는 함수
    """평소 최댓값보다 1 큰 숫자를 알림 기준(임계값)으로 정한다.
    이 숫자 이상이면 평소보다 많다고 보고 알릴 때 쓴다.
    """
    limit = maximum + 1             # 평소 최댓값보다 1 큰 숫자를 기준으로 삼는다
    return limit                    # 알림 기준을 리턴한다
