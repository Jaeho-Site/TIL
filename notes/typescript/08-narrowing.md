---
title: 타입스크립트는 코드 흐름을 읽는다
description: 좁히기 — 제어 흐름 분석이 동작하는 구문, 실패하는 함정, 사용자 정의 타입 가드
---

# 타입스크립트는 코드 흐름을 읽는다

[지난 글](/typescript/07-widening)에서 변수의 타입은 선언 시점에 정해진다고 했다. 그런데 그 말이 무색하게, 선언 이후에 타입이 바뀌는 것처럼 보이는 코드가 있다. 책을 읽다가 만난 퀴즈로 시작한다.

```typescript
function maybeLogX(x?: number | string | null) {
  if (!x) {
    console.log(x);
    // 여기서 x의 타입은?
  }
}
```

나는 `null | undefined`라고 답했다. `!x`로 걸렀으니 "값이 없는" 경우만 남았을 거라고. 실제 답은 이렇다.

```typescript
console.log(x);
//          ^? (parameter) x: string | number | null | undefined
```

**아무것도 좁혀지지 않았다.** 이유를 따라가려면 먼저 "좁혀진다"는 게 뭔지부터 정리해야 했다.

## 선언된 타입과 그 순간의 타입

타입스크립트는 변수마다 선언된 타입만 기억하는 게 아니라, **코드의 각 지점에서 그 변수가 가질 수 있는 값의 집합**을 따로 추적한다. 조건문·반환·예외 같은 제어 흐름을 따라가면서, 각 분기에서 불가능해진 값들을 집합에서 제외한다. 이걸 **좁히기**(narrowing) 또는 제어 흐름 분석이라고 부른다.

```typescript
const elem = document.getElementById('what-time-is-it');
//    ^? const elem: HTMLElement | null
if (!elem) throw new Error('엘리먼트가 없다');
elem.innerHTML = 'Party Time';
// ^? const elem: HTMLElement — throw 이후 흐름에서 null은 불가능
```


좁히기를 일으키는 구문은 생각보다 다양하다. [런타임 타입 확인](/typescript/02-runtime-types)에서 본 `instanceof`와 `in`, 태그된 유니온의 태그 비교, 그리고 `typeof`, `Array.isArray`, 동등 비교까지 — 전부 자바스크립트의 평범한 런타임 검사인데, 타입 체커가 이 검사들을 읽고 타입 층에 반영해 준다.

```typescript
function contains(text: string, terms: string | string[]) {
  const termList = Array.isArray(terms) ? terms : [terms];
  //    ^? const termList: string[]
}
```
