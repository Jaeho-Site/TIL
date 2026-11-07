---
title: 브라우저는 왜 내 요청을 막나
description: SOP와 CORS, preflight — 서버는 멀쩡한데 fetch가 실패하는 이유
---

# 브라우저는 왜 내 요청을 막나

프론트엔드 개발을 하다 보면 반드시 만나는 에러가 있다. `localhost:3000`에서 개발 중인 앱이 API 서버로 fetch를 보냈더니 콘솔이 빨갛게 물든다.

```
Access to fetch at 'https://api.example.com/posts' from origin
'http://localhost:3000' has been blocked by CORS policy: ...
```

여기서 퀴즈. **같은 URL로 Postman이나 curl에서 요청하면 어떻게 될까?**

답: **멀쩡히 성공한다.** 처음 이걸 겪었을 때 혼란 그 자체였다 — 서버가 막는 거라면 Postman도 실패해야 하는 것 아닌가? 이 역설이 CORS 이해의 출발점이다. **막는 주체는 서버가 아니라 브라우저다.**

## 브라우저는 왜 스스로 막나 — SOP

브라우저에는 **동일 출처 정책**(Same-Origin Policy, SOP)이라는 기본 규칙이 있다. 스크립트가 **다른 출처**(origin)의 리소스에 접근하는 것을 제한하는 정책이다. 출처는 세 가지의 조합이다.

```
https   ://   api.example.com   :443    /posts
(스킴)        (호스트)           (포트)   (경로 — 출처에는 포함되지 않는다)

→ 스킴·호스트·포트 셋이 모두 같아야 같은 출처
```

`http://localhost:3000`과 `https://api.example.com`은 호스트도 스킴도 다르니 다른 출처다. 참고로 `localhost:3000`과 `localhost:5173`도 포트가 달라 다른 출처다.

왜 이런 정책이 필요할까. [쿠키 편](/network/08-cookie-session)의 핵심 성질을 떠올려 보자 — **쿠키는 해당 사이트로 가는 요청에 자동으로 붙는다.** 내가 은행에 로그인해 둔 상태로 악성 사이트를 방문했다고 하자. SOP가 없다면 그 사이트의 스크립트는 내 브라우저에서 은행 API로 요청을 보낼 수 있고, **그 요청에는 내 은행 쿠키가 자동으로 실린다** — [쿠키 편](/network/08-cookie-session)에서 본 SameSite 같은 방어가 아직 없던 시절엔 정말 그랬다. 악성 스크립트가 내 명의로 잔액을 조회하고 응답을 읽어가는 것이다. SOP는 이 시나리오를 원천 차단하는 첫 번째이자 가장 오래된 방어막이다 — 다른 출처의 응답은 스크립트가 읽을 수 없다.

즉 CORS 에러는 브라우저가 심술을 부리는 게 아니라, **사용자(나)를 보호하는 방어막이 내 개발 환경에도 똑같이 적용된 것**이다. Postman이 성공하는 이유도 명확해진다 — Postman에는 보호할 "로그인된 사용자의 브라우저"가 없다.

## CORS — 막힌 문을 여는 공식 절차

그런데 현실의 웹은 출처를 넘나드는 요청 위에 서 있다. 프론트엔드와 API 서버가 도메인이 다른 건 기본이고, 외부 API 호출도 일상이다. 그래서 "**서버가 명시적으로 허락하면 예외로 열어주는**" 프로토콜이 생겼다. 그게 **CORS**(Cross-Origin Resource Sharing)다.

동작은 헤더의 문답이다. 브라우저는 교차 출처 요청에 `Origin` 헤더를 붙여 보내고, 서버 응답의 허가 헤더를 확인한다.

```
요청:  Origin: http://localhost:3000
응답:  Access-Control-Allow-Origin: http://localhost:3000   → 통과
```

응답에 이 헤더가 없거나 값이 다르면, 브라우저는 **응답을 받아놓고도 스크립트에게 주지 않는다.** 중요한 지점이다 — 단순한 GET의 경우 요청은 이미 서버에 도착해 처리됐고, 응답도 브라우저까지 왔다. 차단되는 건 마지막 한 걸음, "자바스크립트가 그 응답을 읽는 것"이다.

## preflight — 위험한 요청은 보내기 전에 물어본다

그런데 DELETE를 보내거나 `Content-Type: application/json`으로 POST를 보내면, Network 탭에 내가 보낸 적 없는 **OPTIONS 요청**이 먼저 찍혀 있는 걸 볼 수 있다. 이게 **preflight**(사전 요청)다.

읽기만 차단하는 방식은 "요청이 서버에 도달해 실행되는 것" 자체는 못 막는다. 조회면 몰라도 삭제·수정 요청이라면 실행 자체가 피해다. 그래서 브라우저는 **단순 요청의 범위를 넘는 요청** — 커스텀 헤더를 쓰거나, `application/json` 본문을 보내거나, PUT/DELETE를 쓰는 경우 — 은 본 요청을 보내기 전에 OPTIONS로 먼저 물어본다.

![CORS preflight 시퀀스 — 브라우저가 OPTIONS로 메서드·헤더 허용 여부를 먼저 묻고, 서버가 허가 헤더로 응답하면 그제야 본 요청이 전송되는 흐름](/images/network/11-cors-preflight.png)

```
OPTIONS /posts HTTP/1.1
Origin: http://localhost:3000
Access-Control-Request-Method: DELETE

HTTP/1.1 204 No Content
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, DELETE
Access-Control-Max-Age: 86400
```

허가가 떨어져야 본 요청이 나간다. `Access-Control-Max-Age`는 이 허가를 캐시하는 시간이다 — 매 요청마다 왕복을 두 번 할 수는 없으니까. [캐싱 편](/network/09-http-caching)에서 본 "왕복을 줄이는" 발상이 여기에도 있다.

쿠키가 걸린 요청은 한 단계 더 엄격하다. 위의 은행 시나리오가 무서웠던 만큼, fetch의 교차 출처 요청에는 **기본값부터 쿠키가 실리지 않도록** 정해졌다. 실으려면 클라이언트가 `credentials: 'include'`를 명시하고 서버도 `Access-Control-Allow-Credentials: true`로 응답해야 한다. 이때는 `Allow-Origin: *`(전체 허용)도 금지된다 — 쿠키가 걸린 응답을 아무 출처에나 열어주는 것을 스펙 차원에서 막아둔 것이다.

## 그래서 CORS 에러는 어디서 고치나

이 구조를 이해하면 결론이 자연스럽다. CORS 에러는 **프론트엔드 코드로는 고칠 수 없다.** 허가 헤더는 서버가 보내는 것이기 때문이다. 할 수 있는 일은 둘 중 하나다 — 서버(또는 게이트웨이)에 허용 출처를 설정하거나, 개발 중이라면 dev 서버의 프록시를 써서 브라우저 입장에서 같은 출처로 보이게 우회하는 것(Vite의 `server.proxy`, Next.js의 `rewrites`). 사실 프록시 설정이 하는 일도 "브라우저를 속이는" 게 아니라, 교차 출처 요청 자체를 없애는 것에 가깝다.

---

CORS 에러는 고장이 아니라 **SOP라는 방어막이 정상 동작한 흔적**이다 — 브라우저는 사용자의 쿠키를 지키기 위해 교차 출처 응답을 기본 차단하고, 서버가 허가 헤더로 명시적으로 열어줄 때만 통과시킨다.

여기까지로 요청이 안전하게 오가는 조건은 갖춰졌다. 그런데 아직 그 요청이 **어디로 가야 하는지**를 다루지 않았다. 주소창의 도메인은 어느 시점에 IP 주소가 되는 걸까. → [도메인은 어떻게 IP가 되나](/network/12-dns)
