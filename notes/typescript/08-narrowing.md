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

![getElementById 직후에는 HTMLElement | null이던 elem의 타입이 throw 분기에서 null 경로가 차단된 뒤 HTMLElement로 좁혀지는 제어 흐름](/images/typescript/08-flow-narrowing.png)

좁히기를 일으키는 구문은 생각보다 다양하다. [런타임 타입 확인](/typescript/02-runtime-types)에서 본 `instanceof`와 `in`, 태그된 유니온의 태그 비교, 그리고 `typeof`, `Array.isArray`, 동등 비교까지 — 전부 자바스크립트의 평범한 런타임 검사인데, 타입 체커가 이 검사들을 읽고 타입 층에 반영해 준다.

```typescript
function contains(text: string, terms: string | string[]) {
  const termList = Array.isArray(terms) ? terms : [terms];
  //    ^? const termList: string[]
}
```

## 그럼 !x는 왜 실패했나

집합의 관점으로 돌아가면 도입 퀴즈가 풀린다. `!x`가 참이 되는 값의 집합은 뭘까? `null`과 `undefined`만이 아니다. **`0`도 `''`도 falsy다.** 즉 `!x` 분기 안에서 가능한 값은 `null`, `undefined`, `0`(그리고 `NaN`), `''` — 타입으로 표현하면 여전히 `string | number | null | undefined` 전부다. 컴파일러는 게으른 게 아니라 정확했고, 틀린 건 "falsy = 값 없음"이라는 내 어림짐작이었다.

`typeof`에도 비슷한 함정이 있다. 자바스크립트에서 `typeof null`은 역사적인 이유로 `'object'`라서, 객체를 거르려고 `typeof x === 'object'`를 쓰면 `null`이 **같이 살아남는다**. 타입 체커는 이 기괴한 사양까지 그대로 모델링한다.

```typescript
const elem = document.getElementById('what-time-is-it');
if (typeof elem === 'object') {
  elem;
  // ^? const elem: HTMLElement | null — null이 안 걸러졌다
}
```

## 컴파일러가 못 읽는 흐름도 있다

좁히기는 강력하지만 전지적이지 않다. 실무에서 제일 자주 부딪히는 두 가지가 있다.

**API 사이의 의미 관계는 모른다.** `Map`의 `has`와 `get`이 대표적이다.

```typescript
const nameToNickname = new Map<string, string>();
declare let yourName: string;

let nameToUse: string;
if (nameToNickname.has(yourName)) {
  nameToUse = nameToNickname.get(yourName);
  // ~~~~~~ Type 'string | undefined' is not assignable to type 'string'.
}
```

`has`가 참이면 `get`이 값을 준다는 건 사람의 지식이지 타입의 지식이 아니다. 이럴 땐 검사 순서를 컴파일러가 읽을 수 있는 모양으로 바꾸는 게 정석이다.

```typescript
const nameToUse = nameToNickname.get(yourName) ?? yourName;
```

**콜백 안에서는 좁히기가 풀린다.**

```typescript
function logLaterIfNumber(obj: { value: string | number }) {
  if (typeof obj.value === 'number') {
    setTimeout(() => console.log(obj.value.toFixed()));
    //                                     ~~~~~~~
    // Property 'toFixed' does not exist on type 'string | number'.
  }
}
```

검사한 시점과 콜백이 **실행되는** 시점 사이에 `obj.value`가 바뀔 수 있다. 실제로 `logLaterIfNumber(obj)` 호출 직후 `obj.value = 'Cookie Monster'`를 실행하면, 콜백은 문자열에 `toFixed`를 부르게 된다. 컴파일러는 이 시간차를 알기에 속성에 대한 좁히기를 콜백 경계에서 무효화한다. 사실 [클로저가 변수를 "값의 복사본"이 아니라 살아있는 참조로 기억한다](/javascript/07-closure)는 이야기의 타입 버전인 셈이다. 검사 시점의 값을 지역 `const`에 담아 콜백에서 그 지역 변수를 쓰면 좁히기가 유지된다.

## 내가 만든 함수도 좁히기에 참여시키기

검사 로직을 함수로 뽑아내면 좁히기가 끊긴다는 문제도 있다. `function isString(x) { return typeof x === 'string' }`을 호출해봤자 반환 타입은 그냥 `boolean`이라, 호출부에서는 아무 일도 일어나지 않는다. 이럴 때 반환 타입 자리에 **타입 서술어**(type predicate)를 쓴다.

```typescript
function isInputElement(el: Element): el is HTMLInputElement {
  return 'value' in el;
}

function getElementContent(el: HTMLElement) {
  if (isInputElement(el)) {
    return el.value; // el: HTMLInputElement
  }
  return el.textContent;
}
```

`el is HTMLInputElement`는 "이 함수가 true를 반환하면 `el`을 그 타입으로 좁혀도 된다"는 선언이다. `filter` 같은 고차 함수와 조합하면 배열 타입까지 걸러진다.

```typescript
const formEls = document.querySelectorAll('.my-form *');
const formInputEls = [...formEls].filter(isInputElement);
//    ^? const formInputEls: HTMLInputElement[]
```

다만 서술어의 **본문이 정말 그 타입을 보장하는지는 컴파일러가 검증하지 않는다.** `'value' in el`이 어설픈 검사라면 거짓 보장이 되고, 그 책임은 내게 있다.

---

변수의 타입은 선언에 박제된 하나의 값이 아니라, **제어 흐름의 지점마다 다시 계산되는 값의 집합**이다. 좁히기가 안 될 때는 컴파일러를 탓하기 전에 "이 흐름을 컴파일러가 읽을 수 있는 모양인가"를 먼저 묻게 됐다. 그런데 흐름을 읽는다는 얘기를 하고 나니, 반대 방향의 미스터리가 남는다. 콜백을 인라인으로 쓰면 통과하는 코드가, 변수로 빼는 순간 에러가 나는 건 왜일까. → [인라인은 되는데 변수로 빼면 왜 에러인가](/typescript/09-context-inference)
