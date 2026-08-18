---
title: script 태그는 어디에 둬야 하나
description: 파서 블로킹의 이유, body 끝 국룰의 역사, 그리고 async vs defer
---

# script 태그는 어디에 둬야 하나

"옛날에 script는 `</body>` 직전에 두라"는 말을 국룰처럼 따라 해 왔는데, 왜 그래야 하는지를 공부해본 적이 있다. 그렇다면 반대로 `</head>`에 두면 실제로 무슨 일이 일어나는지 확인해서 Why에 대해 답해보도록 하자.

```html
<!DOCTYPE html>
<html>
  <head>
    <script>
      const $apple = document.getElementById('apple');
      $apple.style.color = 'red';
      // TypeError: Cannot read properties of null (reading 'style')
    </script>
  </head>
  <body>
    <ul>
      <li id="apple">Apple</li>
    </ul>
  </body>
</html>
```

에러가 난다. 이유는 [렌더링 파이프라인](/browser/01-rendering-pipeline)에서 배운 것과 지금 배울 것 하나가 합쳐진 결과다 — HTML 파싱은 위에서 아래로 진행되는데, **파서는 `<script>`를 만나면 파싱을 멈추고 그 자리에서 스크립트를 실행한다.** 실행 시점에 `<li id="apple">`은 아직 파싱 전이라 DOM에 없고, `getElementById`는 null을 돌려준다.

## 왜 파싱을 멈추면서까지 실행하나

파서 입장에서는 멈추고 싶어서가 아니라 **멈춰야 안전해서**다. 자바스크립트는 `document.write`로 파싱 중인 문서에 끼어들 수도 있고, DOM을 마음대로 바꿀 수도 있다. 스크립트가 문서 구조를 바꿀지 모르는데 파싱을 계속 진행하면 결과를 보장할 수 없으니, 브라우저는 보수적으로 "일단 멈추고 실행부터"를 택했다. 그래서 script는 **파서 차단(parser-blocking)** 리소스라고 부른다 — CSSOM 완성까지 렌더링을 미루는 CSS보다 한층 과격하다.

외부 스크립트라면 문제가 더 커진다. 다운로드가 끝날 때까지도 파싱이 멈추므로, head에 큰 스크립트가 있으면 그 시간 동안 사용자는 흰 화면을 본다.

`</body>` 직전에 두라는 국룰은 이 두 문제를 한 번에 피하는 소박한 해법이었다. DOM이 다 만들어진 뒤라 null 사고가 없고, 화면이 먼저 그려진 뒤에 스크립트가 돈다. 다만 아쉬움이 남는다 — 실행이 문서 맨 끝까지 밀리는 데다, 이 국룰이 생긴 옛 브라우저에서는 파서가 거기 도달해야 다운로드도 시작됐다. 요즘 브라우저는 프리로드 스캐너가 마크업을 앞서 훑어 미리 받아두지만, 실행이 늦는 건 그대로다.

## 그래서 나온 것이 async와 defer

`<script>`의 두 속성은 "다운로드는 파싱과 병렬로 하되, 실행을 언제 하느냐"로 갈린다.

```html
<script defer src="app.js"></script>
<script async src="analytics.js"></script>
```

![일반·defer·async 스크립트의 다운로드와 실행이 HTML 파싱을 언제 멈추는지 시간축으로 비교한 다이어그램](/images/browser/03-script-defer-async-timing.png)

- **defer** — 다운로드는 파싱과 병렬로 하고, 실행은 **파싱이 완전히 끝난 뒤** 한다. 여러 개면 선언 순서대로 실행된다. DOM이 완성된 뒤 실행되니 null 사고도 없다. body 끝 국룰이 하던 일을 네트워크 낭비 없이 해내는, 사실상의 기본 선택지다.
- **async** — 다운로드는 병렬로 하되, **도착하는 순간** 파싱을 멈추고 실행한다. 도착 순서에 따라 실행 순서가 뒤바뀔 수 있고, DOM 완성도 보장되지 않는다. 다른 코드나 DOM에 의존하지 않는 독립 스크립트 — 애널리틱스, 광고 — 에 맞는 옵션이다.

기억을 위한 한 줄 정리는 이렇다. **defer는 "미뤄서(deferred) 순서대로", async는 "비동기로 오는 대로".** 참고로 `type="module"` 스크립트는 기본 동작이 defer와 같다 — [모듈 글](/javascript/22-esm-vs-cjs)에서 다시 만난다.

## DOMContentLoaded는 언제 울리나

이 글의 내용을 알고 나면 자주 쓰던 이벤트 하나도 정확해진다. `DOMContentLoaded`는 **HTML 파싱이 끝나 DOM이 완성된 순간** 발생한다(이미지 같은 리소스까지 다 로드된 `load`와 다르다). defer 스크립트는 정의상 이 이벤트 **전에**, 파싱 완료 직후 실행된다. 예전 코드에서 흔히 보이는 `DOMContentLoaded` 콜백으로 감싸는 패턴은, DOM 완성을 기다린다는 점에서 defer와 같은 문제를 푸는 다른 방법이었던 셈이다.

---

script 로딩 문제의 본질은 하나다. **파서는 script 앞에서 멈춘다.** body 끝 국룰도, defer도, async도 전부 그 멈춤을 언제로 옮기느냐에 대한 답이고, 지금의 정답은 대부분의 경우 "head에서 defer"다.

이것으로 브라우저가 화면을 만들고(파이프라인), 다시 그리고(리플로우), 그 사이에 스크립트를 끼워 넣는(로딩 전략) 이야기가 한 바퀴 돌았다. 다음 포스팅은 화면 위에서 벌어지는 일이다. 버튼 하나를 클릭했을 뿐인데 브라우저 안에서는 이벤트가 문서 꼭대기부터 내려왔다 다시 올라간다. → [이벤트 위임은 왜 쓰는가](/browser/04-event-flow-delegation)

<style>
.sl-c{font:600 13px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.sl-dim{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.sl-parse{fill:var(--vp-c-default-soft);stroke:var(--vp-c-divider)}
.sl-dl{fill:var(--vp-c-brand-soft);stroke:var(--vp-c-brand-1)}
.sl-ex{fill:var(--vp-c-danger-soft);stroke:var(--vp-c-danger-1)}
</style>
