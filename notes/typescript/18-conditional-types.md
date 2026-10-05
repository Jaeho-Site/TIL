---
title: 타입에도 조건문이 있다
description: 조건부 타입이 오버로드를 대체하는 이유와 유니온 분배의 원리
---

# 타입에도 조건문이 있다

[지난 글](/typescript/17-mapped-utility-types) 끝의 질문을 실전 문제로 바꿔보자. 숫자를 받으면 숫자를, 문자열을 받으면 문자열을 반환하는 `double` 함수의 타입을 어떻게 선언해야 할까. 처음 떠오르는 건 유니온이다.

```typescript
declare function double(x: string | number): string | number;

const num = double(12);
//    ^? const num: string | number — 숫자를 넣었는데 왜 문자열일지도 모른다는 걸까
```

입력과 출력의 관계가 끊겨 있다. 그럼 오버로드로 관계를 명시하면?

```typescript
declare function double(x: number): number;
declare function double(x: string): string;

const num = double(12);   // number — 좋다
const str = double('x');  // string — 좋다

function f(x: string | number) {
  return double(x);
  //            ~ No overload matches this call.
}
```

개별 호출은 완벽해졌는데, **유니온을 넘기는 순간 무너진다.** 오버로드는 위에서부터 하나씩 대조할 뿐이라 "number거나 string"인 값이 들어갈 자리가 없다. 세 번째 오버로드를 추가하면 되지만, 입력 종류가 늘수록 조합이 폭발한다.

## 조건부 타입 — 타입 층의 삼항 연산자

이 문제의 정답으로 책이 제시하는 게 **조건부 타입**(conditional type)이다.

```typescript
declare function double<T extends string | number>(
  x: T
): T extends string ? string : number;

const num = double(12);   // number
const str = double('x');  // string

function f(x: string | number) {
  return double(x); // string | number — 통과!
}
```

`T extends string ? string : number`는 생김새 그대로 삼항 연산자다 — 조건 자리에 [부분집합 판정](/typescript/05-types-as-sets)(`extends`)이 들어간다는 것만 다르다. "`T`가 `string`의 부분집합이면 `string`, 아니면 `number`."

그런데 잠깐. `f` 안의 호출에서 `T`는 `string | number`다. `string | number`는 `string`의 부분집합이 아니니 조건은 거짓, 그럼 결과는 `number`가 나와야 하는 것 아닌가? 실제 결과는 `string | number`다. 여기에 조건부 타입의 핵심 동작이 숨어 있다.
