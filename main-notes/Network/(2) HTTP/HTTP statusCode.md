### 2.2 상태 코드의 체계적 이해.

HTTP 상태 코드는 서버가 요청을 어떻게 처리했는지를 가장 빠르고 명확하게 전달하는 신호다. 상태코드를 신경쓰지 않는다면, 개발자는 에러를 디버깅함에 있어 큰 어려움이 생길것이다. 팀플을 하다보면 뜻하지 않게자주 보이는 대표적인 안티 패턴이 있다. 

에러가 발생했음에도 불구하고 항상 `200 OK`를 반환하고, 응답 본문에 `{"error": true}` 같은 자체 규약을 담는 방식이다. 브라우저나 CDN이 해당 응답을 정상으로 인식해 캐싱해버리는 캐시 포이즈닝을 유발할 수 있고, `fetch`나 `axios` 인터셉터 역시 이를 성공 응답으로 처리하게 된다. 결국 에러는 숨겨지고, 디버깅은 훨씬 어려워진다. 

상태코드에 대한 모든 정리를 하기보단 대표적인 특징들과 자주 만나게 되는 코드들을 위주로 정리했고, 모든 상태코드와 각각의 특성이 궁금하다면 글을 작성할 때 많이 참고한 링크를 가져와봤다. [https://inpa.tistory.com/entry/HTTP-🌐-상태-코드-1XX-5XX-총정리판-📖](https://inpa.tistory.com/entry/HTTP-%F0%9F%8C%90-%EC%83%81%ED%83%9C-%EC%BD%94%EB%93%9C-1XX-5XX-%EC%B4%9D%EC%A0%95%EB%A6%AC%ED%8C%90-%F0%9F%93%96)  

![image.png](attachment:d9ce5d7e-788f-489a-b0ee-db8bde817919:image.png)

> **성공과 우회의 대응 (2xx, 3xx)**
> 

**2xx는 “성공”이라는 공통점**을 가지지만, 그 결과의 의미는 꽤 다르다. 일반적인 조회나 수정 성공은 `200 OK`로 충분하다. ****하지만 `POST`로 새로운 리소스를 생성했다면, 단순 성공이 아니라 생성이 완료되었다는 사실 자체가 중요하다. 이때는 `201 Created`를 사용하고, 보통 생성된 리소스의 URI를 `Location` 헤더로 함께 전달한다. `204 No Content`는 종종 간과되지만 꽤 유용하다. ****삭제 요청이 정상적으로 처리되었거나, UI를 바꿀 필요 없는 백그라운드 작업이 성공했을 때 “보낼 데이터는 없지만 작업은 끝났다”는 의도를 명확하게 표현할 수 있다.

**3xx는 “성공했지만, 다른 곳을 보라”는 신호다.** 과거 `301`, `302`는 리다이렉션 과정에서 HTTP 메서드를 `GET`으로 바꿔버리는 문제가 있었다. 이 때문에 `POST` 요청의 바디가 유실되는 일이 발생했다. 이를 해결하기 위해 등장한 것이 `307 Temporary Redirect`와 `308 Permanent Redirect`다. 이들은 원래의 메서드와 바디를 그대로 유지한 채 이동한다. 그리고 `304 Not Modified`는 캐시 최적화의 핵심이다. 서버가 “이미 가지고 있는 데이터 그대로 써도 된다”고 확인해주는 순간, 클라이언트는 네트워크 전송 없이 즉시 응답을 완료한다.

> **에러의 책임은? Client vs Server (4xx, 5xx)**
> 

**4xx는 문제의 원인이 클라이언트에 있음을 의미한다.** 문법 오류나 필수 값 누락 같은 기본적인 문제는 `400 Bad Request`로 표현할 수 있다. 실제로 가장 자주 마주치는 상태 코드는 아래 세 가지이다.

- `401 Unauthorized`는 **인증이 필요하지만, 아직 인증되지 않은 상태**를 의미한다. 보통 로그인이 되어 있지 않거나, 토큰이 없거나 만료된 경우에 발생한다.
- `403 Forbidden`은 **인증은 되었지만 권한이 없는 경우**다. 로그인은 했지만 접근할 수 없는 리소스에 접근하려 할 때 반환된다.
- `404 Not Found`는 **요청한 리소스 자체가 존재하지 않는 경우**다. 잘못된 URL이거나, 이미 삭제된 리소스를 조회할 때 발생한다.

이 세 코드는 사용자 경험과도 직결되기 때문에, 프론트엔드에서 명확하게 구분해 처리하는 것이 중요하다. 단순히 “에러 발생”으로 묶어버리면 UX가 크게 저하된다. 한편, 평소에는 잘 드러나지 않지만 반드시 이해하고 있어야 하는 상태 코드도 있다. API Gateway, CDN, WAF, 혹은 프론트 단의 사전 검증 로직에 의해 실제로는 자주 노출되지 않을 뿐이다.

`409 Conflict`는 동시성 문제가 발생했을 때 사용된다. 이미 존재하는 데이터로 생성 요청을 하거나, 동일 자원을 동시에 수정하려 할 때 대표적으로 등장한다. 이 경우 단순 에러 처리로 끝내는 것이 아니라, 사용자에게 충돌 상황을 알리고 재시도를 유도하는 UX가 필요하다. 또한 `429 Too Many Requests`는 서버가 보내는 명확한 속도 제한 신호다. “지금은 요청이 너무 많으니 잠시 멈춰라”는 의미이며, 클라이언트는 이에 맞춰 요청 간격을 조절하거나 재시도를 지연해야 한다.

**5xx는 반대로, 클라이언트의 요청은 정상이지만 서버가 이를 처리하지 못한 상황이다.** `500 Internal Server Error`는 가장 일반적인 서버 측 예외다. 반면 `502 Bad Gateway`나 `504 Gateway Timeout`은 MSA 환경에서 특히 자주 보인다. 앞단의 리버스 프록시(Nginx 등)나 로드 밸런서가 뒷단의 애플리케이션 서버(WAS)로부터 유효한 응답을 제때 받지 못했거나 지연되었을 때 발생한다. 프론트엔드는 이 코드를 통해 백엔드 인프라의 일시적 병목 현상을 인지하고, 즉각적인 재요청보다는 점진적으로 요청 간격을 늘려가는 지수 백오프 기반의 지연 재시도 로직을 설계해야 시스템의 연쇄적인 붕괴를 막을 수 있다.

아래 이미지는 [Mohith Gupta](https://mohithgupta.medium.com/?source=post_page---byline--fee26d3706b4---------------------------------------) 님의 글을 읽다가 HTTP 상태 코드를 화장실로 재밌게 비유한 짤이 있어서 넣어보았다. 

![스크린샷 2026-03-23 164938.png](attachment:2fa8782c-37bd-493e-8a84-f67df799fab6:스크린샷_2026-03-23_164938.png)

<reference>

image made by claude, gemini

https://calendar.perfplanet.com/2020/head-of-line-blocking-in-quic-and-http-3-the-details/

[https://velog.io/@yesbb/HTTP3까지-버전별-변천사](https://velog.io/@yesbb/HTTP3%EA%B9%8C%EC%A7%80-%EB%B2%84%EC%A0%84%EB%B3%84-%EB%B3%80%EC%B2%9C%EC%82%AC)

[https://developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Evolution_of_HTTP)

https://code-lab1.tistory.com/34

https://bbo-blog.tistory.com/87

https://hahahoho5915.tistory.com/55

https://javascript.plainenglish.io/all-the-http-response-status-codes-you-will-ever-need-as-a-web-developer-fee26d3706b4