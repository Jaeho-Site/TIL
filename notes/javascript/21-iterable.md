---
title: for...of와 for...in은 뭐가 다른가
description: 순회 가능하다는 것의 정확한 조건 — 이터러블 프로토콜, 스프레드, 유사 배열
---

# for...of와 for...in은 뭐가 다른가

이름이 한 글자 차이라 초반에 자주 섞어 썼던 두 반복문이다. 배열에 프로퍼티를 하나 붙여서 돌려보면 완전히 다른 물건이라는 게 드러난다.

```javascript
const arr = ['a', 'b', 'c'];
arr.extra = 'd'; // 배열도 객체니까 이런 게 된다

for (const x of arr) console.log(x); // ?
for (const x in arr) console.log(x); // ?
```

`for...of`는 `a b c` — 요소의 **값**을 순회한다. `for...in`은 `0 1 2 extra` — **프로퍼티 키**를 열거한다. 인덱스가 문자열 키로 나오고, 요소도 아닌 `extra`까지 섞여 나온다.

## for...in은 객체용, for...of는 이터러블용

`for...in`의 정체는 **객체의 열거 가능한 프로퍼티 키를 훑는 문**이다. 심지어 [프로토타입 체인](/javascript/11-prototype-chain)을 따라 상속받은 프로퍼티까지 열거 대상이다(`Object.prototype`의 메서드들이 안 나오는 건 열거 불가능(enumerable: false)으로 정의돼 있어서다). 그래서 배열에 쓰면 인덱스가 문자열 키로 나오고 상속·추가 프로퍼티까지 섞이는, 위 문제 같은 일이 생긴다. 배열엔 쓰지 않는 게 원칙이다.

그럼 `for...of`는 어떤 기준으로 도는 걸까. "배열이니까"가 아니다 — 문자열도, Map도, Set도, [arguments](/javascript/14-first-class-function)도, [HTMLCollection](/browser/05-dom-essentials)도 된다. 이들의 공통점은 타입이 아니라 **약속(프로토콜)을 지킨다**는 것이다.

## 이터러블 프로토콜: 순회 가능은 자격증이다

약속의 내용은 놀랄 만큼 단순하다. **`Symbol.iterator`라는 키의 메서드를 가지고 있고, 그 메서드가 이터레이터를 반환하면 이터러블이다.** 직접 확인해 볼 수 있다.

```javascript
const isIterable = v => v !== null && typeof v[Symbol.iterator] === 'function';

isIterable([]);        // true
isIterable('');        // true
isIterable(new Set()); // true
isIterable({});        // false — 일반 객체는 아니다
```

이터레이터는 `next()`를 가진 객체고, `next()`는 `{ value, done }`을 반환한다. `for...of`가 하는 일이 정확히 이것이다 — 수동으로 돌려보면:

```javascript
const iterator = [1, 2, 3][Symbol.iterator]();

console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: 2, done: false }
console.log(iterator.next()); // { value: 3, done: false }
console.log(iterator.next()); // { value: undefined, done: true } — 여기서 for...of가 멈춘다
```

이 프로토콜을 쓰는 소비자가 `for...of`만이 아니라는 게 중요하다. **스프레드(`...`), 배열 구조 분해, `Array.from`, `Promise.all`이 받는 인자** — 전부 이터러블 프로토콜 위에서 동작한다. 그래서 일반 객체는 스프레드로 배열을 만들 수 없다.

```javascript
const obj = { a: 1, b: 2 };

const arr2 = [...obj];   // TypeError: obj is not iterable
const [x, y] = obj;      // TypeError: obj is not iterable

console.log({ ...obj }); // { a: 1, b: 2 } — 어? 이건 되네?
```

마지막 줄이 헷갈리는 지점이다. **객체 리터럴 안의 스프레드는 이터러블 프로토콜과 무관한 별도 문법**(ES2018 스프레드 프로퍼티)으로, 프로퍼티를 복사할 뿐이다. [얕은 복사 글](/javascript/02-shallow-deep-copy)에서 쓰던 그 스프레드는 사실 이터러블과 상관없는 기능이었던 것이다. "배열 스프레드는 이터러블 프로토콜, 객체 스프레드는 프로퍼티 복사" — 이렇게 갈라 두면 안 섞인다.

## "유사 배열이면서 이터러블"의 정확한 의미

[함수 글](/javascript/14-first-class-function)과 [DOM 글](/browser/05-dom-essentials)에서 미뤄둔 표현을 이제 완성할 수 있다. 두 개념은 별개의 축이다.

- **유사 배열 객체** — `length`와 인덱스 프로퍼티를 가져서 `for` 문과 인덱스 접근이 되는 객체. "생김새"의 문제다.
- **이터러블** — `Symbol.iterator`를 구현한 객체. "프로토콜"의 문제다.

`arguments`와 `HTMLCollection`, `NodeList`는 둘 다에 해당해서 인덱스 접근도 되고 스프레드도 된다. 반면 `{ 0: 'a', 1: 'b', length: 2 }` 같은 수제 유사 배열은 이터러블이 아니라서 `for...of`도 스프레드도 안 된다. 이런 것까지 전부 배열로 바꿔주는 도구가 `Array.from`이다 — **유사 배열이든 이터러블이든** 받아서 진짜 배열을 만든다.

덧붙여 Set과 Map도 이터러블이라서, 배열 메서드는 없어도 스프레드 한 번이면 배열 세계로 넘어온다. 중복 제거 관용구가 대표적이다.

```javascript
const unique = [...new Set([1, 2, 2, 3, 3])]; // [1, 2, 3]
```

---

"순회 가능"은 타입이 타고나는 성질이 아니라 **프로토콜 준수 여부**다. `Symbol.iterator`라는 자격증만 있으면 for...of, 스프레드, 구조 분해가 전부 열린다 — 반대로 자격증 없는 일반 객체는 생김새가 어떻든 닫혀 있다.

여기까지가 한 파일 안의 이야기다. 시리즈의 마지막 질문은 파일 경계를 넘는다 — 파일과 파일은 어떻게 이어지고, 왜 `import`와 `require` 두 가지 방식이 존재할까. → [ESM과 CJS는 뭐가 다른가](/javascript/22-esm-vs-cjs)
