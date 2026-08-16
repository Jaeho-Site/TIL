---
title: 싱글 스레드인데 어떻게 동시에 처리하나
description: 이벤트 루프는 자바스크립트가 아니라 브라우저의 것이다 — 콜 스택, 태스크 큐, 블로킹
---

# 싱글 스레드인데 어떻게 동시에 처리하나

이번엔 코드보다 질문 하나가 먼저다. 아래 코드에서 `bar`가 먼저 실행되고 3초 뒤 `foo`가 실행된다는 건 이제 놀랍지 않다.

```javascript
function foo() { console.log('foo'); }
function bar() { console.log('bar'); }

setTimeout(foo, 3 * 1000);
bar(); // bar → (3초 후) foo
```

내가 걸린 지점은 이거였다. **자바스크립트는 싱글 스레드라서 한 번에 한 가지 일만 한다고 했다.** 그런데 `bar`가 실행되는 동안, 그리고 그 뒤로 3초 동안 — **타이머는 누가 재고 있었을까?** 엔진이 한 번에 하나만 할 수 있다면 시간을 재는 일과 코드 실행을 동시에 할 수 없어야 한다. 모순처럼 보였다.

## 답: 자바스크립트는 시간을 재지 않는다

모순이 풀리는 지점은 의외였다. **타이머를 재는 건 자바스크립트 엔진이 아니라 브라우저다.**

엔진이 가진 건 [실행 컨텍스트 스택](/javascript/04-hoisting), 즉 **콜 스택** 하나뿐이다. "싱글 스레드"의 정확한 의미가 이것이다 — 콜 스택이 하나라서 실행 중인 코드가 끝나야 다음 코드를 실행할 수 있다. 여기까지만 보면 3초를 기다리는 동안 아무것도 못 해야 맞다.

그런데 `setTimeout`은 사실 자바스크립트 언어(ECMAScript)의 함수가 아니다. 브라우저가 제공하는 **호스트 API**다. `setTimeout(foo, 3000)`을 호출하면 엔진은 "3초 뒤에 이 함수를 부탁해"라고 브라우저에 **외주를 주고 즉시 다음 줄로 넘어간다.** 시간은 브라우저가 엔진 바깥에서 잰다. 브라우저 자체는 멀티 스레드라서 타이머를 재면서 렌더링도 하고 네트워크 요청도 받는다.

3초가 지나면 브라우저는 `foo`를 콜 스택에 바로 밀어 넣을까? 그러면 실행 중이던 코드 한복판에 끼어들게 되니 안 된다. 대신 **태스크 큐**라는 대기줄에 등록한다. 그리고 **이벤트 루프**가 단순한 규칙을 무한 반복한다 — *콜 스택이 비어 있나? 큐에 대기 중인 콜백이 있나? 있으면 스택으로 올린다.*

<svg viewBox="0 0 680 360" role="img" aria-label="setTimeout 콜백이 브라우저 Web API로 위임되고, 만료 후 태스크 큐에 등록되며, 콜 스택이 비면 이벤트 루프가 스택으로 올리는 순환 구조" style="max-width:680px;width:100%;height:auto;margin:16px 0">
<defs><marker id="el-ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-brand-1)"/></marker></defs>
<text x="40" y="34" class="el-t">자바스크립트 엔진</text>
<text x="640" y="34" text-anchor="end" class="el-t">브라우저 (호스트 환경)</text>
<line x1="335" y1="20" x2="335" y2="330" class="el-ln"/>
<rect x="40" y="70" width="180" height="140" rx="8" class="el-box"/>
<text x="56" y="94" class="el-s">콜 스택</text>
<rect x="56" y="110" width="148" height="30" rx="5" class="el-frame"/>
<text x="130" y="130" text-anchor="middle" class="el-c">bar() 실행 중</text>
<text x="56" y="196" class="el-dim2">한 번에 하나만</text>
<rect x="460" y="70" width="180" height="140" rx="8" class="el-box"/>
<text x="476" y="94" class="el-s">Web API</text>
<rect x="476" y="110" width="148" height="30" rx="5" class="el-frame"/>
<text x="550" y="130" text-anchor="middle" class="el-c">타이머: 3초 재는 중</text>
<text x="476" y="164" class="el-dim2">fetch, 클릭 감시도</text>
<text x="476" y="182" class="el-dim2">전부 여기서 대기한다</text>
<path d="M224,100 L455,100" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#el-ah)"/>
<text x="340" y="88" text-anchor="middle" class="el-hl">① setTimeout — 위임</text>
<rect x="460" y="250" width="180" height="52" rx="8" class="el-box"/>
<text x="476" y="272" class="el-s">태스크 큐</text>
<rect x="546" y="280" width="40" height="18" rx="4" class="el-frame"/>
<text x="566" y="293" text-anchor="middle" class="el-c">foo</text>
<path d="M550,214 L550,245" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#el-ah)"/>
<text x="562" y="236" class="el-hl">② 만료 → 큐에 등록</text>
<path d="M455,286 L130,286 L130,218" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#el-ah)"/>
<text x="292" y="278" text-anchor="middle" class="el-hl">이벤트 루프</text>
<text x="292" y="306" text-anchor="middle" class="el-s">③ 스택이 비면 콜백을 올린다</text>
<text x="40" y="345" class="el-dim2">엔진은 실행만 한다 — 기다리는 일은 전부 브라우저의 몫이다</text>
</svg>

그래서 이벤트 루프와 태스크 큐는 ECMAScript 스펙을 뒤져도 안 나온다. **HTML 스펙에 정의되어 있고, 브라우저(Node.js라면 libuv)가 제공한다.** "자바스크립트는 싱글 스레드"라는 말의 실체는 이렇다 — 엔진의 콜 스택이 하나일 뿐, 동시성은 브라우저와의 협업으로 만들어진다.

## 그럼 3초는 보장되나?

아니다. 여기서 이벤트 루프 이해가 실전과 만난다. 규칙을 다시 보면 콜백은 "3초 뒤"가 아니라 **3초 뒤 + 콜 스택이 빈 다음**에 실행된다. 스택이 안 비면?

```javascript
setTimeout(() => console.log('1초 뒤에 실행되길 바랐다'), 1000);

const start = Date.now();
while (Date.now() - start < 3000); // 3초 동안 콜 스택을 점유

// 콜백은 1초가 아니라 3초 후에야 실행된다
```

타이머는 정확히 1초 뒤에 만료되어 콜백을 큐에 넣었다. 하지만 while 루프가 스택을 점유하고 있는 동안 이벤트 루프는 손을 못 댄다. `setTimeout`의 delay는 보장 시간이 아니라 **최소 지연 시간**이다.

이게 브라우저에서 벌어지면 사용자가 직접 겪는다. 클릭 이벤트의 콜백도 같은 큐에서 기다리기 때문에, 무거운 동기 코드가 스택을 점유하는 동안 **버튼은 눌리지 않고 화면은 멈춘다.** 프론트엔드에서 "메인 스레드를 막지 마라"는 조언이 전부 이 구조에서 나온다. 해법의 방향도 구조가 알려준다 — 작업을 잘게 쪼개 큐에 나눠 넣거나(스택을 자주 비워주거나), 아예 다른 스레드(Web Worker)로 보내는 것이다. 렌더링이 정확히 무엇을 하고 언제 끼어드는지는 [브라우저 렌더링 글](/browser/01-rendering-pipeline)에서 다룬다.

---

자바스크립트가 동시에 여러 일을 하는 게 아니었다. **엔진은 한 번에 하나만 실행하고, 기다리는 일은 전부 브라우저에 외주를 준다.** 이벤트 루프는 그 외주 결과를 돌려받는 유일한 창구다.

그런데 이 대기줄, 사실 하나가 아니다. Promise의 콜백은 setTimeout과 **다른 줄**에 서고, 그 줄은 언제나 먼저 처리된다. 다음 글에서 새치기의 규칙을 다룬다. → [Promise.then과 setTimeout, 누가 먼저인가](/javascript/17-micro-macro-task)

<style>
.el-t{font:600 13.5px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.el-s{font:600 13px var(--vp-font-family-base);fill:var(--vp-c-text-2)}
.el-c{font:12px var(--vp-font-family-mono);fill:var(--vp-c-text-1)}
.el-dim2{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.el-hl{font:600 12px var(--vp-font-family-base);fill:var(--vp-c-brand-1)}
.el-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.el-frame{fill:var(--vp-c-default-soft);stroke:var(--vp-c-divider)}
.el-ln{stroke:var(--vp-c-divider);stroke-dasharray:4 4}
</style>
