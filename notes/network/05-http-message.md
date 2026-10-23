---
title: HTTP 메시지는 어떻게 생겼나
description: 요청/응답 메시지의 구조와 무상태 설계 — 브라우저와 서버가 주고받는 대화의 문법
---

# HTTP 메시지는 어떻게 생겼나

[지난 글](/network/04-tcp-vs-udp)까지 데이터를 실어 나르는 전송 계층을 봤다. 이제 그 위에서 오가는 내용물 차례다. 터미널에서 `curl -v`로 요청 한 번을 떠보면, 브라우저가 매일 하는 대화를 날것으로 볼 수 있다.

```
> GET / HTTP/1.1
> Host: example.com
> User-Agent: curl/8.7.1
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Wed, 02 Sep 2026 12:30:48 GMT
< Content-Type: text/html
< Connection: keep-alive
< Age: 12155
< cf-cache-status: HIT
<
<!doctype html> ...
```

보기 전에 하나만 짚고 가자. 위 출력에서 **요청과 응답이 공유하는 구조**는 무엇일까? 사실 처음 이 출력을 봤을 때 나는 구조보다 다른 것에 놀랐다 — HTTP 메시지의 실체가 **그냥 몇 줄의 텍스트**라는 것. 개발자 도구에서 예쁘게 정리된 테이블로만 보다가 원문을 보니, 오히려 공통의 뼈대가 한눈에 들어왔다.

## 요청과 응답, 각각 세 부분

HTTP는 요청(request)과 응답(response)이 짝을 이루는 프로토콜이고, 두 메시지 모두 같은 뼈대를 가진다. **시작 줄, 헤더, (빈 줄 하나 건너) 본문.**

**요청 메시지**의 시작 줄은 `GET / HTTP/1.1` — 메서드, 경로, 프로토콜 버전이다. "무엇을(경로), 어떻게(메서드) 해달라"는 문장의 골격이다. 그 아래 헤더들은 요청의 부가 정보다.

- `Host`: 같은 IP의 서버 한 대가 여러 도메인을 서비스할 수 있어서, 어느 도메인에 온 요청인지 반드시 밝혀야 한다 (HTTP/1.1부터 필수 헤더다)
- `Accept`: 어떤 형식의 응답을 이해할 수 있는지
- `User-Agent`: 요청을 보내는 클라이언트의 정체

GET 요청은 보통 본문이 없다. POST라면 빈 줄 아래에 JSON 같은 본문이 붙고, `Content-Type` 헤더가 그 형식을 알려준다.

**응답 메시지**의 시작 줄은 `HTTP/1.1 200 OK` — 버전, 상태 코드, 상태 문구다. 요청의 결과를 숫자 하나로 요약한다. 헤더에는 응답 본문에 대한 설명(`Content-Type`, `Content-Length`)과 연결·캐시에 대한 지시가 실리고, 빈 줄 아래에 실제 내용물 — HTML, JSON, 이미지 바이트 — 이 온다.

`fetch` 코드와 겹쳐 보면 이 구조가 그대로 API에 반영되어 있다.

```javascript
const res = await fetch('/api/posts', {
  method: 'POST',                                  // 시작 줄의 메서드
  headers: { 'Content-Type': 'application/json' }, // 헤더
  body: JSON.stringify({ title: '...' }),          // 빈 줄 아래 본문
});
res.status;      // 응답 시작 줄의 상태 코드
res.headers;     // 응답 헤더
await res.json(); // 응답 본문
```

fetch의 옵션 객체는 사실 HTTP 요청 메시지의 구조를 자바스크립트 문법으로 옮겨 적은 것에 가깝다.
