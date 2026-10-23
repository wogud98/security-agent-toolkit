# 3과목 Day 3 권한 요청서 · 승인과 반려 · 정책 확인 후 부여 · 오전 (이름 · 2026-10-23(금))

> **쓰는 법**
> - 문제를 풀 때마다 그 문제 제목 아래 질문에 답합니다.
> - 질문마다 `쓸 내용:` 에 무엇을 쓰면 되는지 적혀 있습니다. 그대로 `답:` 뒤에 씁니다.
> - 출력이나 코드를 붙여 넣는 질문은 `답:` 아래 빈 코드 상자에 붙여 넣고, 설명은 `답:` 뒤에 씁니다.
> - 「왜」를 묻는 질문은 한 단어로 끝내지 말고, 내 화면에서 본 값이나 배운 내용을 근거로 이유까지 씁니다.
> - 🔍 는 이 교시에서 꼭 알아야 할 핵심 질문입니다. 답을 못 찾았으면 「모름 — 막힌 곳: …」 이라고 씁니다.

---

## 2교시 · 권한 요청서 만들기

### 문제 2-1 · 요청서를 만들어 목록에 모으고, 접수할 수 없는 요청 걸러 내기

- (가) 실행한 출력 전체를 붙여 넣고, 접수되지 않은 세 건이 각각 `create_request` 의 어느 `if` 조건 때문에 접수되지 않았는지 적어 주세요.
  - 쓸 내용: ① 출력 전체(코드 상자에 붙여 넣기) ② 접수되지 않은 세 건 각각이 걸린 `if` 조건
  - 답:
hana(user not in USERS 조건에 걸림, 사용자 파일에 없는 이름), 
seoyeon 의 ACCOUNT:QUERY(reason == "" 조건에 걸림, 이유가 비어 있음), 
gaeun 의 ACCOUNT:QUERY(until <= received_at 조건
```bash
--- 단계 1: 접수 - 요청 일곱 건을 하나씩 넣는다
seoyeon SETTLE QUERY -> 접수됨, 요청 번호 1
gaeun SALES QUERY -> 접수됨, 요청 번호 2
dami SALES QUERY -> 접수됨, 요청 번호 3
junho SETTLE QUERY -> 접수됨, 요청 번호 4
hana SALES QUERY -> 접수 안 됨: 등록되지 않은 사용자
seoyeon ACCOUNT QUERY -> 접수 안 됨: 이유가 없음
gaeun ACCOUNT QUERY -> 접수 안 됨: 만료 시각이 이미 지났음
--- 단계 2: 점검 - 요청서 목록
1 seoyeon SETTLE:QUERY reviewing
2 seoyeon SALES:QUERY reviewing
3 seoyeon SALES:QUERY reviewing
4 seoyeon SETTLE:QUERY reviewing
(.venv) 
```
```python
    # 1. user 가 USERS 에 없으면 False, "등록되지 않은 사용자" 를 리턴한다
    if user not in USERS:
        return False, "등록되지 않은 사용자"
    # 2. reason 이 빈 글자("")이면 False, "이유가 없음" 을 리턴한다
    if reason == "":
        return False, "이유가 없음"
    # 3. until 이 received_at 과 같거나 앞서면(until <= received_at) False, "만료 시각이 이미 지났음" 을 리턴한다
    if until <= received_at:
        return False, "만료 시각이 이미 지났음"
    # 4. 딕셔너리 request 를 만든다. 칸 아홉 개의 이름은 2.1 의 표와 같고, 값은 이렇게 정한다:
    #    "id" 는 REQUESTS 의 개수 + 1, "permission" 은 f"{resource}:{action}", "requested_at" 은 received_at,
    #    "status" 는 "reviewing", 나머지 다섯 칸(user · resource · action · until · reason)은 같은 이름의 값을 그대로 넣는다
    request = {"id":len(REQUESTS)+1, "user":"seoyeon", "resource":"SETTLE", "action":"QUERY", "permission":f"{resource}:{action}", "until":"2026-10-27 18:00", "reason":"정산 대조 지원", "requested_at":"2026-10-23 08:30", "status":"reviewing"}

    # 5. REQUESTS 목록 끝에 request 를 더한다
    #print(request)
    REQUESTS.append(request)

    # 6. True, request 를 리턴한다
    return True, request
```

- (나) 🔍 요청서의 `until`(희망 만료 시각)은 요청자가 직접 적습니다. 요청자가 적은 기간을 그대로 믿고 승인해도 될까요? 승인하기 전에 확인할 것을 두 가지 이상 적어 주세요.
  - 쓸 내용: ① 그대로 믿어도 되는지 ② 승인 전에 확인할 것 두 가지 이상
  - 답: NO. 
1 이유에 적힌 일이 실제로 언제 끝나는지, 그 일에 필요한 가장 짧은 기간인지 
2 요청자가 이 권한을 받는 것이 업무에 맞는지(영업이 정산을 보려는 이유가 분명한지) 
3 만료 시각이 너무 먼 미래는 아닌지

## 3교시 · 승인과 반려

### 문제 3-1 · 승인 · 반려 함수 만들고, 두 번째 처리가 막히는지 확인하기

- (가) 실행한 출력 전체를 붙여 넣고, 막힌 세 줄이 각각 왜 막혔는지 적어 주세요.
  - 쓸 내용: ① 출력 전체(코드 상자에 붙여 넣기) ② 막힌 세 줄 각각의 이유
  - 답:
```
1 본인 승인 은 요청자 seoyeon 이 자기 1번 요청을 승인하려 해서 본인 요청은 처리할 수 없음 
처리 여섯 건 중 1 승인 이 두 번째 나온 줄은 이미 승인된 1번
2 승인 은 이미 반려된 2번이라 둘 다 검토 중이 아님 
```
```bash
--- 단계 1: 처리 - 본인 요청 시험 한 건, 승인 · 반려 여섯 건을 처리한다
1 본인 승인 -> False 본인 요청은 처리할 수 없음
1 승인 -> True 승인
2 반려 -> True 반려
3 승인 -> True 승인
4 승인 -> True 승인
1 승인 -> False 검토 중이 아님
2 승인 -> False 검토 중이 아님
--- 단계 2: 점검 - 요청서 목록
1 seoyeon approved security_manager
2 seoyeon rejected security_manager
3 seoyeon approved security_manager
4 seoyeon approved security_manager
```

- (나) 🔍 이미 승인한 요청서를 다시 승인하지 못하게 막는 이유는 무엇인가요? 막지 않으면 어떤 일이 생길 수 있나요?
  - 쓸 내용: ① 막는 이유 ② 막지 않을 때 생길 수 있는 일
  - 답: *처리가 끝난 요청이 다시 처리되면 같은 요청이 두 번 부여되거나(예외가 중복으로 생김), 승인한 기록이 나중에 바뀌어 감사 기록을 믿을 수 없게 되기 때문입니다. 반려한 요청서를 나중에 승인으로 바꿀 수 있으면 「반려」라는 결정의 의미가 없어집니다. 번복이 필요하면 상태를 고치지 말고 새 요청서를 접수합니다.*

- (다) 🔍 `approve_request` 에서 `request["user"] == approver` 검사를 뺀다면 어떤 위험이 생길까요? 요청자가 친구에게 대신 승인해 달라고 부탁하면 이 검사로는 막을 수 없습니다. 이런 경우를 막으려면 무엇이 더 필요할까요?
  - 쓸 내용: ① 검사를 뺐을 때의 위험 ② 더 필요한 장치 한 가지 이상
  - 답: 
        1:*요청자가 자기 요청을 스스로 승인해, 아무도 확인하지 않은 요청이 통과*
        2:*요청자가 친구 계정이나 다른 사람에게 부탁해 대신 승인하게 하는 것을 막지 못함.* 
        ㄴ더 필요한 장치의 예: 계정 관리처럼 위험한 권한은 승인자를 두 명으로 하고(이중 승인), 
          승인자를 요청자와 다른 부서의 정해진 사람으로 두고, 승인 이력을 정기적으로 대조*

## 4교시 · 정책 확인 후 예외 권한 부여

### 문제 4-1 · 승인된 요청서를 정책으로 확인하고 예외 권한 부여하기

- (가) 실행한 출력 전체를 붙여 넣고, 부여를 시도한 네 건이 각각 어떻게 됐는지 적어 주세요.
  - 쓸 내용: ① 출력 전체(코드 상자에 붙여 넣기) ② 네 건 각각의 결과
  - 답:
```
부여를 시도 네 건 결과
  (부여된 예외 번호: 6 줄은 1번 요청서에 적힌 예외 번호입니다). 
  1번 seoyeon 은 부여됨(예외 6번)
  2번 gaeun 은 부여 안 함(반려된 요청서라 「승인되지 않음」)
  3번 dami 는 부여 안 함(퇴사한 계정)
  4번 junho 는 부여 안 함(이미 허용된 권한).
```

```bash
--- 단계 1: 판정 - 부여 전
1 seoyeon SETTLE:QUERY -> False 권한 없음
2 gaeun SALES:QUERY -> False 권한 없음
3 dami SALES:QUERY -> False 퇴사한 계정
4 junho SETTLE:QUERY -> True 역할 권한
--- 단계 2: 부여 - 요청서마다 부여를 시도한다
1 seoyeon granted -> True 부여
2 gaeun rejected -> False 승인되지 않음
3 dami approved -> False 부여하지 않음(퇴사한 계정)
4 junho approved -> False 부여하지 않음(허용)
부여된 예외 번호: 6
--- 단계 3: 점검 - 부여 후
1 seoyeon SETTLE:QUERY -> True 예외 6번
2 gaeun SALES:QUERY -> False 권한 없음
3 dami SALES:QUERY -> False 퇴사한 계정
4 junho SETTLE:QUERY -> True 역할 권한
```

- (나) 🔍 승인자가 승인한 3번 요청(`dami`)을 코드가 부여하지 않았습니다. 코드의 이 확인이 없었다면 어떤 일이 생겼을까요? 승인자가 이 문제를 미리 막기 어려운 이유도 적어 주세요.
  - 쓸 내용: ① 확인이 없을 때 생기는 일 ② 승인자가 미리 막기 어려운 이유
  - 답:
```
승인자는 사람이라서 요청자가 이미 퇴사했는지를 모르고 승인할 수 있습니다. 
코드는 지금 사용자 파일과 역할 파일로 판정하므로 퇴사한 계정을 확실히 거릅니다. 

승인자의 확인은 「이 요청이 업무에 맞는가」를 판단하고, 
코드의 확인은 「이 사람이 지금 정책상 부여를 받을 수 있는 사람인가」를 판단합니다. 

둘은 보는 것이 다르므로 함께 써야 합니다. 이 확인이 없으면 퇴사자에게 예외가 만들어져 목록에 남습니다.
```

- (다) 🔍 부여한 예외의 만료 시각에는 요청서의 희망 만료 시각을 그대로 썼습니다. 그 시각이 지나면 이 예외는 어떻게 될까요? 만료된 예외를 정리하는 점검은 누가 얼마나 자주 하면 좋을까요?
  - 쓸 내용: ① 만료 뒤 예외가 어떻게 되는지 ② 점검을 누가 얼마나 자주 할지
  - 답:
```
요청서의 until(2026-10-27 18:00)이 그대로 예외의 expires 가 되었습니다. 
그 시각이 지나면 어제의 find_exception 이 now < expires 를 거짓으로 판정해 예외를 쓰지 않으므로 요청자는 다시 「권한 없음」으로 거부됩니다. 

다만 만료된 예외가 EXCEPTIONS 에 계속 남으므로, 어제 만든 회수 점검(만료됨 · 퇴사자)을 매일 돌려 목록에서 정리 대상으로 뽑고 회수 이력을 남깁니다. 점검 담당과 주기(예: 보안 담당이 매일 아침)를 정해 두면 맞습니다.
```
