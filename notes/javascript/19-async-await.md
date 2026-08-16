---
title: async/await은 어떻게 동작하나
description: await은 멈추는 게 아니라 비켜주는 것 — 그리고 try/catch가 비동기를 잡게 된 이유
---

# async/await은 어떻게 동작하나

[지난 글](/javascript/18-promise) 끝에서 "then 체인을 동기 코드 모양으로 되돌려 준 문법"이라고 했다. 정말 동기처럼 동작하는지 확인하는 문제부터.

```javascript
async function foo() {
  console.log('A');
  const x = await Promise.resolve('B');
  console.log(x);
}

foo();
console.log('C');
// 출력 순서는?
```

`await`이 "기다린다"는 뜻이니 `A B C`일 것 같지만, 답은 **`A C B`**다. 애초에 진짜로 기다린다면 이상하다 — [싱글 스레드](/javascript/16-event-loop)에서 함수 하나가 기다리며 버티고 있으면 프로그램 전체가 멈춰야 한다.

## await은 멈추는 게 아니라 비켜주는 것이다

`await`이 하는 일을 정확히 쓰면 이렇다. **함수를 그 지점에서 일시정지하고, 제어권을 호출자에게 돌려준다.** 그리고 기다리던 프로미스가 settled되면, 함수의 나머지 부분이 [마이크로태스크](/javascript/17-micro-macro-task)로 재개된다.

문제를 이 규칙으로 다시 읽으면: `foo()`가 A를 찍고 `await`에서 일시정지 → 제어권이 돌아와 C가 찍힘 → 스택이 비고 마이크로태스크로 나머지(`console.log(x)`)가 재개되어 B. "함수 안에서는 기다리는 것처럼 보이고, 함수 밖에서는 아무도 기다리지 않는다" — 이 두 관점의 동시 성립이 async/await의 전부다.

이게 가능한 건 함수를 중간에 멈췄다 재개하는 능력 덕분인데, 그 능력의 원형이 제너레이터다. async/await은 "제너레이터(멈춤/재개) + 프로미스(재개 시점 결정)"를 언어가 묶어 준 문법이라고 정리할 수 있다. 실제로 ES2017 이전에는 이 조합을 라이브러리(co 등)로 손수 만들어 썼다.

`async` 키워드 쪽 규칙은 하나만 기억하면 된다. **async 함수는 무조건 프로미스를 반환한다.**

```javascript
async function foo(n) { return n; } // return 값이 resolve 값이 된다

foo(1).then(v => console.log(v)); // 1
```

값을 return하면 그 값으로 fulfilled된 프로미스가, 에러를 throw하면 rejected 프로미스가 반환된다. 호출자 입장에서 async 함수는 그냥 "프로미스를 돌려주는 함수"다.

## try/catch가 드디어 비동기를 잡는다

개인적으로 async/await의 진짜 가치는 가독성보다 이쪽이라고 생각한다. [지난 글](/javascript/18-promise) 도입에서 setTimeout의 에러를 try/catch가 못 잡는 걸 봤다 — 콜백이 새로운 실행 흐름에서 시작되기 때문이었다. 그런데 await은 이 구도를 되돌린다.

```javascript
async function fetchTodo() {
  try {
    const res = await fetch('https://wrong.url.example');
    const todo = await res.json();
    return todo;
  } catch (err) {
    console.error(err); // 네트워크 실패가 여기서 잡힌다
  }
}
```

프로미스가 reject되면, `await`은 그 rejection을 **그 자리에서 throw된 에러로 변환**한다. 함수가 await 지점에서 재개될 때 에러도 같은 자리에서 다시 던져지는 셈이라, 동기 코드용 도구였던 try/catch가 비동기 실패를 잡을 수 있게 된다. 에러 처리의 두 세계 — 동기의 throw/try-catch와 비동기의 rejection/catch — 가 await 한 지점에서 통일된다.

물론 함수 안에서 잡지 않고 호출자에게 미루는 선택도 된다. async 함수 안에서 잡히지 않은 에러는 반환 프로미스의 rejection이 되므로, 호출부에서 `.catch`(또는 바깥 async 함수의 try/catch)로 받으면 된다.

## 함정: await을 빼먹으면 다시 샌다

이 통일에는 조건이 있다. **try 블록 안에서 프로미스를 await해야** 한다는 것이다.

```javascript
try {
  const p = fetchTodo(); // await을 빼먹었다 — 프로미스를 만들기만 했다
} catch (err) {
  // 실패해도 여기 안 온다. try는 "프로미스 생성"까지만 지켜봤다
}
```

`fetchTodo()` 호출 자체는 성공적으로 프로미스를 반환하고 try 블록은 끝난다. 실패는 나중에 프로미스 안에서 일어나므로, await으로 그 결과를 현재 흐름에 되돌려 놓지 않는 한 try/catch는 구경꾼이다. 잡히지 않은 rejection은 브라우저에서는 unhandled rejection 경고로 남고, Node.js에서는 아예 프로세스가 종료된다(v15부터 기본 동작). 콘솔에서 이 경고를 봤다면 어딘가에서 rejection이 주인 없이 떠돌고 있다는 뜻이다.

---

async/await은 새로운 능력이 아니라 **프로미스의 문법 포장**이다. 다만 두 가지를 동기 세계의 모양으로 되돌려 줬다 — 결과는 반환값처럼(`const x = await p`), 실패는 예외처럼(try/catch).

그런데 이 편안함에는 부작용이 하나 있다. await이 너무 자연스러워서, **기다릴 필요가 없는 것까지 줄 세워 기다리게 된다.** 1초짜리 요청 세 개가 3초가 되는 함정 — 다음 글에서 다룬다. → [Promise.all은 언제 쓰나](/javascript/20-promise-combinators)
