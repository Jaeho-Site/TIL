---
title: REST API는 무엇을 약속하나
description: 자원·행위·표현 — URI와 메서드에 역할을 나눠 싣는 설계 규약
---

# REST API는 무엇을 약속하나

API 설계를 처음 해보면 반드시 부딪히는 고민이 있다. 할 일 삭제 API의 주소를 뭐라고 지을까?

```
1. GET  /deleteTodo?id=1
2. POST /todos/delete/1
3. DELETE /todos/1
```

셋 다 "동작하게" 만들 수는 있다. 하지만 1번은 [GET으로 삭제하면 왜 안 되는지](/network/06-method-status)에서 본 크롤러 사고의 재현이고, 2번은 행위를 메서드가 아니라 URI에 실었다. 답은 3번인데 — 왜 3번이 "맞다"고 느껴지는 걸까. 그 감각의 정체가 REST다.

## REST — 역할을 나눠 싣는 설계

REST는 특정 기술이 아니라 **HTTP를 설계된 의도대로 쓰기 위한 아키텍처 스타일**이다(HTTP 명세 작업에 참여한 로이 필딩의 논문에서 나왔다). 핵심은 API의 구성 요소를 세 자리에 나눠 싣는 것이다.

| 구성 요소 | 실리는 곳 | 예 |
|---|---|---|
| **자원(Resource)** | URI | `/todos/1` — 1번 할 일 |
| **행위(Verb)** | HTTP 메서드 | `GET` `POST` `PUT` `PATCH` `DELETE` |
| **표현(Representation)** | 본문(페이로드) | `{ "content": "HTTP 공부", "completed": true }` |

이 분담이 지켜지면 URI에는 **명사**만 남는다. `/deleteTodo`처럼 URI에 동사가 들어가는 순간 행위가 두 곳에 실리는 것이고, 그게 1·2번 설계가 어긋나 보이는 이유다.

```
GET    /todos      → 목록 조회
GET    /todos/1    → 1번 조회
POST   /todos      → 생성 (서버가 id를 정한다)
PUT    /todos/1    → 1번 전체 교체
PATCH  /todos/1    → 1번 부분 수정
DELETE /todos/1    → 1번 삭제
```

같은 URI(`/todos/1`)가 메서드에 따라 다른 일을 한다 — 자원은 하나고, 행위만 다르기 때문이다.
