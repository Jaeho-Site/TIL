---
title: 콜백의 진짜 문제는 무엇이고, 프로미스는 뭘 해결했나
description: 비동기 결과를 값으로 만들다 — 3가지 상태, then 체이닝, catch의 위치
---

# 콜백의 진짜 문제는 무엇이고, 프로미스는 뭘 해결했나

[이벤트 루프](/javascript/16-event-loop)를 이해했다면 답할 수 있는 문제부터.

```javascript
let g = 0;

setTimeout(() => { g = 100; }, 0);
console.log(g); // ?
```

답은 `0`이다. 콜백은 현재 코드가 다 끝난 뒤에야 실행되니, 비동기 처리의 결과는 **반환값으로 받을 수도, 변수에 담아 쓸 수도 없다.** 결과가 필요한 후속 처리를 전부 콜백 안으로 밀어 넣는 수밖에 없다.

그런데 후속 처리가 또 비동기라면? 콜백 안에 콜백이 들어간다. "post를 받아서 → 그 userId로 user를 받아서 → …"처럼 의존 관계가 이어지면 이렇게 된다.

```javascript
get('/step1', a => {
  get(`/step2/${a}`, b => {
    get(`/step3/${b}`, c => {
      get(`/step4/${c}`, d => {
        console.log(d);
      });
    });
  });
});
```

콜백 헬(callback hell)이다. 그런데 정리하면서 알게 됐는데, 사실 들여쓰기는 **부차적인 문제**다.

## 진짜 문제는 에러가 샌다는 것

콜백 방식의 치명타는 이쪽이다.

```javascript
try {
  setTimeout(() => { throw new Error('Error!'); }, 1000);
} catch (e) {
  console.error('캐치한 에러', e); // 영원히 실행되지 않는다
}
```

에러가 절대 잡히지 않는다. [이벤트 루프 글](/javascript/16-event-loop)의 지식으로 설명하면 — 콜백이 실행되는 시점에 `try` 블록은 이미 콜 스택에서 사라진 지 오래다. 콜백은 태스크 큐를 거쳐 **완전히 새로운 실행 흐름**에서 시작되므로, 그 안에서 던진 에러를 바깥의 try/catch가 잡을 길이 없다. 콜백 헬에서는 단계마다 에러 콜백을 따로 받는 식으로 수습해야 하는데, 4단계 중첩이면 에러 처리도 4벌이다.

한 가지 더, 콜백은 **제어권을 넘기는 방식**이다. 내 후속 처리를 남의 함수에 인자로 맡기면, 그 함수가 콜백을 한 번 부를지 두 번 부를지 안 부를지 보장할 방법이 없다.

## 프로미스: 미래의 결과를 담는 객체

ES6의 프로미스는 발상을 뒤집는다. 후속 처리를 넘기는 대신, **비동기 처리의 미래 결과를 담을 객체를 먼저 돌려준다.**

```javascript
const promiseGet = url => {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.send();

    xhr.onload = () => {
      if (xhr.status === 200) {
        resolve(JSON.parse(xhr.response)); // 성공 — 결과를 담는다
      } else {
        reject(new Error(xhr.status));     // 실패 — 이유를 담는다
      }
    };
  });
};

const promise = promiseGet('/posts/1'); // 결과를 "담을 그릇"이 즉시 반환된다
```

(참고로 이 예제는 상태 코드 실패만 처리한다. 네트워크 자체가 끊기면 `onload`가 아예 호출되지 않아 프로미스가 영원히 대기 상태로 남으므로, 실전에서는 `onerror`에서도 reject해야 한다.)

이 객체는 세 가지 상태 중 하나에 있다.

<svg viewBox="0 0 680 240" role="img" aria-label="pending 상태에서 resolve하면 fulfilled, reject하면 rejected로 전이하고, 한 번 settled되면 바뀌지 않는 프로미스 상태 다이어그램" style="max-width:680px;width:100%;height:auto;margin:16px 0">
<defs><marker id="pm-ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-brand-1)"/></marker></defs>
<rect x="30" y="88" width="160" height="54" rx="8" class="pm-box"/>
<text x="110" y="110" text-anchor="middle" class="pm-s">pending</text>
<text x="110" y="130" text-anchor="middle" class="pm-dim">아직 결과 없음</text>
<rect x="430" y="34" width="220" height="54" rx="8" class="pm-ok"/>
<text x="540" y="56" text-anchor="middle" class="pm-s">fulfilled — 성공, 값 보유</text>
<text x="540" y="76" text-anchor="middle" class="pm-dim">then 콜백이 실행된다</text>
<rect x="430" y="152" width="220" height="54" rx="8" class="pm-bad"/>
<text x="540" y="174" text-anchor="middle" class="pm-s">rejected — 실패, 에러 보유</text>
<text x="540" y="194" text-anchor="middle" class="pm-dim">catch 콜백이 실행된다</text>
<path d="M194,100 C300,90 340,72 425,64" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#pm-ah)"/>
<text x="300" y="66" text-anchor="middle" class="pm-hl">resolve(value)</text>
<path d="M194,130 C300,140 340,168 425,176" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#pm-ah)"/>
<text x="300" y="180" text-anchor="middle" class="pm-hl">reject(error)</text>
<text x="30" y="230" class="pm-dim">fulfilled나 rejected가 되면 settled(결정됨) — 이후 상태는 다시 바뀌지 않는다</text>
</svg>

이 구조가 콜백의 문제들을 어떻게 푸는지가 핵심이다. **결과가 객체에 저장되므로 값처럼 다룰 수 있다** — 반환할 수 있고, 변수에 담을 수 있고, 나중에 `then`을 걸어도 저장된 결과를 받는다. 상태는 한 번 정해지면 불변이라 콜백이 두 번 불리는 사고도 없다. 그리고 에러는 —

## 에러는 체인을 타고 흐른다

`then`은 항상 **새 프로미스를 반환한다.** 콜백이 값을 반환하면 그 값으로 fulfilled된 프로미스가, 프로미스를 반환하면 그 프로미스를 그대로 따르는 프로미스가, 에러를 던지면 rejected 프로미스가 나온다. 그래서 중첩 대신 평평하게 이어 쓸 수 있다.

```javascript
promiseGet('/posts/1')
  .then(post => promiseGet(`/users/${post.userId}`)) // 프로미스를 반환하면 이어진다
  .then(user => console.log(user.name))
  .catch(err => console.error(err)); // 위 어디서 실패해도 여기로 온다
```

콜백 헬과 비교해 보면 들여쓰기보다 중요한 변화가 보인다. **어느 단계에서 실패하든 rejection이 체인을 타고 내려와 마지막 `catch` 한 곳에 모인다.** 에러 처리 4벌이 1벌이 됐다. `catch(fn)`는 사실 `then(undefined, fn)`의 축약인데, 두 번째 인자 방식과 달리 **자기 앞 then 콜백에서 던진 에러까지** 잡아주므로 체인 끝의 catch가 관례가 됐다. 성공/실패와 무관하게 실행할 마무리는 `finally`에 건다.

덧붙이면, 이 콜백들이 실행되는 곳이 [지난 글](/javascript/17-micro-macro-task)의 **마이크로태스크 큐**다. 프로미스가 이미 settled여도 then 콜백은 동기로 실행되지 않고 반드시 큐를 거친다.

---

프로미스는 콜백을 없앤 게 아니다. `then`에 넘기는 것도 여전히 콜백이니까. 바뀐 것은 **비동기 결과가 "값"이 됐다**는 것이다 — 담을 수 있고, 돌려줄 수 있고, 이어 붙일 수 있고, 에러를 한곳에 모을 수 있는.

그래도 아쉬움은 남는다. then 체인은 여전히 "다음에 할 일"을 콜백으로 쓰는 문법이라, 동기 코드처럼 위에서 아래로 읽히지는 않는다. 이걸 동기 코드의 모양으로 되돌려 준 것이 async/await이다. → [async/await은 어떻게 동작하나](/javascript/19-async-await)

<style>
.pm-s{font:600 13px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.pm-dim{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.pm-hl{font:600 12px var(--vp-font-family-mono);fill:var(--vp-c-brand-1)}
.pm-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.pm-ok{fill:var(--vp-c-green-soft);stroke:var(--vp-c-green-1)}
.pm-bad{fill:var(--vp-c-danger-soft);stroke:var(--vp-c-danger-1)}
</style>
