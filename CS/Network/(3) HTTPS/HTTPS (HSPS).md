## **4. 웹 개발 환경에서의 HTTPS 이슈와 최적화**

TLS를 적용했다고 해서, 웹 서비스 전체가 자동으로 안전해지는 것은 아니다. 실제 문제는 브라우저가 렌더링하는 “문서 내부”에서 발생한다. 하나의 HTML 문서 안에서 HTTPS와 HTTP 리소스가 섞이는 순간, 브라우저는 이를 더 이상 안전한 페이지로 간주하지 않는다. 

이때 발생하는 대표적인 문제가 바로 Mixed Content다.

### **4.1 Mixed Content 에러: HTTPS 페이지에서 HTTP 리소스를 호출할 때 브라우저가 화내는 이유**

Mixed Content는 HTTPS로 로드된 페이지 내부에서 HTTP 리소스를 요청하는 상황을 의미한다. 예를 들면,

- HTML은 `https://`로 로드되었지만 `<script>`, `<img>`, `fetch()` 등이 `http://`로 요청되는 경우

이 상황이 위험한 이유는 명확하다. 페이지 자체는 암호화되어 있지만, 내부에서 불러오는 리소스는 중간자 공격에 그대로 노출되기 때문이다 특히 JavaScript 같은 리소스가 변조될 경우, 해당 스크립트는 부모 페이지와 동일한 권한으로 실행된다.

즉, 공격자는 다음과 같은 행위를 할 수 있다:

- 세션 쿠키 탈취
- 사용자 입력 가로채기
- DOM 조작 및 피싱 UI 삽입

![Group 21.png](attachment:7a9bf6cc-f379-4184-88da-bd8fcd0982ba:Group_21.png)

결과적으로 HTTPS가 제공하는 보안 컨텍스트가 내부에서 무너진다. 브라우저는 이러한 위험도를 기준으로 Mixed Content를 두 가지로 나누어 처리한다.

**1) Active Mixed Content (능동적 콘텐츠)**

- 대상: `<script>`, `<link>`, `<iframe>`, `fetch`, `XHR` 등
- 특징: 페이지 동작 자체를 변경할 수 있음

이 경우 브라우저는 요청 자체를 아예 차단한다. 네트워크로 나가기 전에 막아버리기 때문에, 개발자 콘솔에서 에러로 바로 확인된다.

**2) Passive Mixed Content (수동적 콘텐츠)**

- 대상: `<img>`, `<video>`, `<audio>` 등
- 특징: 직접적인 코드 실행은 없음

최신 브라우저는 이를 단순 경고로 두지 않고, 가능한 경우 HTTP 요청을 HTTPS로 자동 업그레이드한다. 서버가 HTTPS를 지원하면 정상 로드 지원하지 않으면 최종적으로 실패

그렇다면 이 문제는 어떻게 해결하면 좋을까? 사실 가장 확실한 해결책은 단순하다. 모든 리소스를 HTTPS로 통일하는 것이다. 절대 경로를 `https://`로 수정하거나 프로토콜을 생략한 상대 경로(`//example.com/...`) 사용하는 것이다.

문제는 레거시 환경이다. DB나 템플릿에 `http://`가 대량으로 하드코딩되어 있다면, 이를 전부 수정하는 것은 현실적으로 어렵다.이럴 때 사용하는 방법이 CSP의 `upgrade-insecure-requests`다.

```
Content-Security-Policy: upgrade-insecure-requests
```

이 설정을 적용하면 브라우저는 DOM을 파싱하면서 발견하는 모든 모든 HTTP 요청을 자동으로 HTTPS로 변환한 뒤 전송한다. 즉, 코드를 수정하지 않고도 클라이언트 단에서 Mixed Content 문제를 상당 부분 완화할 수 있다.

다만 이 방식에도 전제가 있다. 리소스 서버가 HTTPS를 반드시 지원해야 한다. 그렇지 않으면 업그레이드된 요청은 실패하게 된다. 정리하면 Mixed Content는 HTTPS 보안 모델을 내부에서 무너뜨릴 수 있는 구조적 문제이며 브라우저는 이를 강하게 차단하는 방향으로 진화해왔다.

| Mixed Content 유형 | 대상 리소스 예시 | 보안 위험도 | 최신 브라우저의 처리 정책 (동작 원리) |
| --- | --- | --- | --- |
| **Active Mixed Content** (능동적 / Blockable) | `<script>`, `<link rel="stylesheet">`, `<iframe>`, `fetch()`, `XMLHttpRequest` 등 | **매우 높음**. 악성 코드로 변조될 경우 웹 페이지의 DOM 전체를 조작하거나 세션을 탈취하여 사이트 제어권을 넘겨주게 된다. | 브라우저가 HTTP 요청을 서버로 보내기도 전에 네트워크 계층에서 **즉각적으로 완전 차단(Block)**해 버린다. 프론트엔드 개발 시 API Endpoint를 HTTP로 잘못 설정했을 때 콘솔에 출력되는 붉은색 에러의 원인이다. |
| **Passive Mixed Content** (수동적 / Upgradable) | `<img>`, `<audio>`, `<video>` 등 | **상대적으로 낮음**. DOM의 실행 흐름을 무단 변경하지는 못하나, 해커가 이미지를 위조하여 피싱을 유도하거나 포르노 이미지 등으로 교체(Deface)할 수 있다. | 과거에는 자물쇠 아이콘에 경고 표시만 띄웠으나, 최신 브라우저(Chrome, Firefox 127+)는 HTTP URL을 내부적으로 HTTPS로 **자동 업그레이드(Auto-Upgrade)**하여 요청을 시도한다. 만약 대상 리소스 서버가 HTTPS를 지원하지 않는다면 다운로드는 최종적으로 실패 처리된다. |

### **4.2 HSTS : 브라우저가 HTTP 요청 자체를 차단하는 원리**

과거 웹에서는 사용자가 `example.com`을 입력하면 브라우저가 먼저 `http://`로 요청을 보내고, 서버가 이를 HTTPS로 리디렉션하는 방식이 일반적이었다. 이 구조는 최초 요청이 평문으로 노출된다는 점에서 SSL Stripping 공격에 취약했다.

최근에는 주소창 탐색에서 HTTPS 우선 시도를 점점 강화하고 있다. Chrome등 최신 브라우저들은 HTTPS-First 정책을 기본값으로 채택하여, 사용자가 도메인만 입력하더라도 처음부터 HTTPS로 연결을 시도한다. 

즉, 과거처럼 “무조건 HTTP → HTTPS 리디렉션” 흐름은 더 이상 기본 전제는 아니다.

그럼에도 불구하고, 이 방식만으로는 보안이 완전히 해결되지 않는다.  HTTPS-First는 어디까지나 “우선 HTTPS로 시도”하는 정책일 뿐, 서버가 HTTPS를 지원하지 않거나 연결이 실패할 경우 브라우저는 여전히 HTTP로 fallback을 시도할 수 있다. fallback이 허용되는 환경에서는, 공격자가 HTTPS 연결 실패를 유도할 경우 HTTP로 downgrade될 가능성이 남는다.

이 문제를 근본적으로 차단하는 메커니즘이 바로 HSTS다. 서버는 HTTPS 응답에 다음과 같은 헤더를 포함시킨다.

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

이 헤더를 한 번이라도 수신한 브라우저는 해당 도메인에 대해 다음과 같이 동작한다:

- HTTPS 연결이 실패하더라도→ HTTP로 fallback하지 않음
- 사용자가 `http://`를 명시적으로 입력해도→ 네트워크로 보내지 않고 내부에서 HTTPS로 강제 변환
- 인증서가 유효하지 않은 경우→ 예외 없이 연결 차단 (우회 불가)

즉, “HTTPS를 시도한다”가 아니라 “HTTPS만 허용한다”로 정책이 강화된다.

#### HTTPS-First vs HSTS의 역할 차이

- HTTPS-First: 기본 연결을 HTTPS로 “우선 시도”, 실패 시 경고 후 사용자 선택으로 HTTP 가능
- HSTS: HTTP 자체를 금지, fallback 경로까지 완전히 제거

#### HSTS의 한계와 Preload

여전히 한 가지 문제가 남는다. 브라우저가 HSTS 정책을 알기 위해서는 최소 한 번은 HTTPS 응답을 받아야 한다. 이 TOFU(Trust On First Use) 문제를 해결하기 위해 브라우저는 HSTS Preload List를 사용한다.

이 리스트에 포함된 도메인은 첫 접속부터 HTTPS만 허용, fallback 자체가 불가능하다. 특히 `.dev`, `.app` 같은 TLD는 이 리스트에 포함되어 있어 처음 접속부터 강제 HTTPS가 적용된다. 그래서 실수로 보안에 문제되는 요청을 차단할 수 있다는 장점이 있다.

정리하자면 이제 브라우저는 기본적으로 HTTPS로 먼저 연결하지만 fallback이 존재하는 한 완전한 방어는 아니다. HSTS는 이 fallback 경로를 제거하는 역할을 하고, Preload까지 적용하면 “첫 요청” 단계까지 완전히 보호된다.

마지막으로 블로그를 쓰면서 읽게된 기사가 있다. 크롬이 최신에 발표한 기사인데 이에 따르면 첫 요청에 보낸 `http://` 요청이든, 첫요청에 실패하고 `http://` 로 fallback하던 과거의(현재까지의) 동작에서 이젠 "'조용히 HTTP로 넘어가 주는 동작'을 아예 없애버리고, 강력한 경고창으로 일단 연결을 차단하여 사용자 모르게 평문 통신이 이루어지는 것을 원천 봉쇄하겠다는 뜻이다.

https://www.infosecurity-magazine.com/news/chrome-https-mandatory-2026/

<Reference>
https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/MITM
https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Mixed_content
https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security
https://web.dev/articles/what-is-mixed-content

https://certera.com/blog/tls-1-3-everything-you-need-to-know/

https://velog.io/@sejinkim/HTTP-Strict-Transport-Security