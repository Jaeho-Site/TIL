---
title: Promise.then과 setTimeout, 누가 먼저인가
description: 마이크로태스크 큐는 매 틱 전부 비워지는 우선 큐다 — 출력 순서 문제와 setTimeout(0)의 진실
---

# Promise.then과 setTimeout, 누가 먼저인가

[지난 글](/javascript/16-event-loop)의 이해를 시험하는 문제로 시작한다.

```javascript
console.log('A');

setTimeout(() => console.log('B'), 0);

Promise.resolve().then(() => console.log('C'));

console.log('D');
```

지난 글대로라면 이렇게 추론하게 된다. 동기 코드인 A와 D가 먼저, 그리고 큐에 등록된 순서대로 B가 C보다 먼저. 그래서 나는 `A D B C`라고 답했다. 실제 출력은 **`A D C B`**다. 나중에 등록된 Promise 콜백이 setTimeout을 앞질렀다.

## 큐가 하나가 아니었다

내 추론이 틀린 이유는 "큐에 등록된 순서대로"라는 전제에 있었다. 콜백이 서는 대기줄은 **두 개**고, 어느 줄에 서는지는 콜백의 출신이 결정한다.

- **매크로태스크 큐**(그냥 "태스크 큐"라고도 한다): `setTimeout`/`setInterval`의 콜백, 클릭 같은 이벤트 핸들러
- **마이크로태스크 큐**: `Promise.then/catch/finally`의 콜백, `queueMicrotask`, `MutationObserver`

그리고 이벤트 루프는 두 줄을 공평하게 처리하지 않는다. 규칙은 이렇다.

<svg viewBox="0 0 680 230" role="img" aria-label="이벤트 루프 한 바퀴: 매크로태스크 하나 실행 후 마이크로태스크 큐를 전부 비우고 렌더링 기회를 거쳐 반복한다" style="max-width:680px;width:100%;height:auto;margin:16px 0">
<defs><marker id="mt-ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-brand-1)"/></marker></defs>
<rect x="20" y="60" width="180" height="64" rx="8" class="mt-box"/>
<text x="110" y="87" text-anchor="middle" class="mt-s">① 매크로태스크</text>
<text x="110" y="107" text-anchor="middle" class="mt-hl">하나만 실행</text>
<rect x="250" y="60" width="200" height="64" rx="8" class="mt-box2"/>
<text x="350" y="87" text-anchor="middle" class="mt-s">② 마이크로태스크 큐</text>
<text x="350" y="107" text-anchor="middle" class="mt-hl">전부 비운다</text>
<rect x="500" y="60" width="160" height="64" rx="8" class="mt-box"/>
<text x="580" y="87" text-anchor="middle" class="mt-s">③ 렌더링 기회</text>
<text x="580" y="107" text-anchor="middle" class="mt-dim">(필요할 때만)</text>
<path d="M204,92 L245,92" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#mt-ah)"/>
<path d="M454,92 L495,92" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#mt-ah)"/>
<path d="M580,128 L580,168 L110,168 L110,132" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#mt-ah)"/>
<text x="345" y="160" text-anchor="middle" class="mt-dim">한 바퀴 = 틱(tick), 무한 반복</text>
<text x="250" y="44" class="mt-dim">Promise.then은 이 줄 — 그래서 항상 먼저다</text>
<text x="20" y="208" class="mt-dim">동기 코드(첫 스크립트 실행)도 하나의 매크로태스크다 — 끝나면 곧장 ②로 간다</text>
</svg>

**매크로태스크는 한 바퀴에 하나만 처리하지만, 마이크로태스크 큐는 그때마다 전부 비운다.** 이 규칙으로 문제를 다시 돌려보면:

1. 스크립트 전체 실행(이것도 하나의 매크로태스크다) — A 출력, B는 매크로 큐로, C는 마이크로 큐로, D 출력
2. 스택이 비었다 → 마이크로태스크 큐부터 전부 비운다 → **C**
3. 다음 매크로태스크 하나 → **B**

`A D C B`. Promise가 이긴 게 아니라, 애초에 우선 처리되는 줄에 서 있었던 것이다.

## "전부 비운다"는 말의 무게

두 큐의 진짜 차이는 "먼저"가 아니라 **하나 vs 전부**에 있다. 확인하는 문제:

```javascript
setTimeout(() => console.log('매크로 1'), 0);
setTimeout(() => console.log('매크로 2'), 0);

Promise.resolve()
  .then(() => console.log('마이크로 1'))
  .then(() => console.log('마이크로 2'));

// 마이크로 1 → 마이크로 2 → 매크로 1 → 매크로 2
```

`마이크로 2`는 `마이크로 1`이 실행되면서 **새로 생긴** 마이크로태스크인데도 매크로태스크들보다 먼저 실행된다. 큐를 비우는 도중에 추가된 마이크로태스크까지 같은 틱에서 전부 처리하기 때문이다.

그럼 이런 생각이 든다 — 마이크로태스크가 계속 마이크로태스크를 낳으면?

```javascript
function loop() {
  Promise.resolve().then(loop);
}
loop();

// 이 뒤로 setTimeout 콜백도, 렌더링도 영원히 실행되지 않는다
```

②에서 빠져나갈 수 없으니 매크로태스크와 렌더링이 **영원히 굶는다**(starvation). 무한 재귀를 `setTimeout`으로 돌리면 한 바퀴에 하나씩이라 화면이 살아있지만, Promise로 돌리면 탭이 멈춘다. 마이크로태스크의 우선권은 공짜가 아니라, 남용하면 렌더링을 볼모로 잡는 권력이다.

## setTimeout(fn, 0)의 진실

이제 "0초"의 의미를 정확히 말할 수 있다. `setTimeout(fn, 0)`의 0은 "즉시"가 아니다.

1. **다음 매크로태스크 차례**라는 뜻이다 — 현재 코드가 끝나고, 마이크로태스크 큐가 다 비워진 다음이다
2. 스펙상 타이머 **중첩이 5회를 넘으면 최소 4ms**로 강제된다(오래된 "setTimeout은 4ms" 속설의 출처 — 항상 4ms인 게 아니라 중첩 시의 하한이다)
3. [지난 글](/javascript/16-event-loop)에서 봤듯 스택이 점유되면 무한정 밀린다

그래서 `setTimeout(fn, 0)`의 정확한 번역은 "지금 하던 일과 급한 일(마이크로태스크)을 다 끝내면, 최대한 빨리"다.

## async/await도 결국 이 줄에 선다

미리 한 스푼만 맛보면, `async/await`도 새로운 메커니즘이 아니다.

```javascript
async function foo() {
  console.log('1');
  await Promise.resolve();
  console.log('2'); // await 뒤의 코드는 마이크로태스크로 밀린다
}

foo();
console.log('3');
// 1 → 3 → 2
```

`await` 뒷부분은 `.then` 콜백과 똑같이 마이크로태스크 큐에 들어간다. async/await이 어떻게 이걸 동기 코드처럼 보이게 만드는지는 프로미스 글에서 이어서 다룬다.

---

**마이크로태스크 큐는 매 틱마다 완전히 비워지는 우선 큐다.** Promise가 setTimeout을 항상 이기는 이유이자, Promise를 잘못 쓰면 렌더링을 굶길 수 있는 이유가 같은 한 문장에서 나온다.

다음 궁금증은 그 Promise 자체다. 콜백을 그냥 쓰면 되는데 왜 굳이 Promise라는 객체를 만들었을까 — 가독성 문제라고들 하지만, 사실 진짜 문제는 따로 있다. → [콜백의 진짜 문제는 무엇이고, 프로미스는 뭘 해결했나](/javascript/18-promise)

<style>
.mt-s{font:600 13px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.mt-hl{font:600 12.5px var(--vp-font-family-base);fill:var(--vp-c-brand-1)}
.mt-dim{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.mt-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.mt-box2{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-brand-1);stroke-width:1.5}
</style>
