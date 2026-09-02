---
title: 타입은 값의 집합이다
description: never부터 unknown까지 — 할당 가능성, 유니온, 인터섹션, extends를 관통하는 하나의 관점
---

# 타입은 값의 집합이다

[지난 글](/typescript/04-excess-property-checking)까지 "구조가 맞으면 할당된다"는 감각으로 버텨왔는데, 인터섹션 타입을 만난 날 그 감각이 무너졌다.

```typescript
interface Person {
  name: string;
}
interface Lifespan {
  birth: Date;
  death?: Date;
}
type PersonSpan = Person & Lifespan;
```

`&`는 인터섹션, 즉 교집합이라고 배웠다. `Person`과 `Lifespan`의 교집합이라면... 두 타입의 공통 속성? 공통 속성은 없으니 `PersonSpan`은 빈 타입일까? 퀴즈: 아래 코드는 컴파일될까?

```typescript
const ps: PersonSpan = {
  name: 'Alan Turing',
  birth: new Date('1912/06/23'),
};
```

**통과한다.** `PersonSpan`은 빈 타입이 아니라 `name`과 `birth`를 **모두** 요구하는 타입이다. 교집합이라더니 속성은 합집합처럼 불어났다. 여기서 뭘 놓치고 있는 걸까.

## 타입이 담고 있는 건 속성이 아니라 값이다

내 착각은 `&`가 **속성 목록**에 적용된다고 생각한 것이었다. 타입스크립트 공식 문서와 책이 공통으로 미는 관점은 이렇다. **타입은 할당 가능한 값들의 집합이다.**

- `Person`은 "name이 문자열인 모든 객체"의 집합이다. 지난 글에서 본 대로 타입은 열려 있으니, `birth`가 더 있는 값도 이 집합의 원소다.
- `Lifespan`은 "birth가 Date인 모든 객체"의 집합이다.
- `Person & Lifespan`은 이 **값 집합의 교집합** — 양쪽 모두에 속하는 값들이다.

양쪽 모두에 속하려면 `name`도 있어야 하고 `birth`도 있어야 한다. 그래서 값의 교집합을 구했더니 속성 요구 조건은 합쳐진 것이다. 교집합인데 속성이 늘어나는 게 아니라, **집합이 좁아질수록 조건이 늘어나는** 것이다.


이 관점으로 지금까지의 개념을 다시 쓰면 전부 집합 용어로 번역된다.

| 타입스크립트 용어 | 집합 용어 |
|---|---|
| `A`에 할당 가능하다 | `A`의 부분집합이다 (원소다) |
| `A \| B` | 합집합 |
| `A & B` | 교집합 |
| `A extends B` | `A ⊂ B` |
| `never` | 공집합 |
| `unknown` | 전체집합 |
