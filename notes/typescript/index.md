---
title: TypeScript
description: 궁금증을 따라가며 정리한 TypeScript 공부 기록
---

# TypeScript

TypeScript를 공부하며 생긴 궁금증을 하나씩 해결해 나간 기록입니다.

기본서는 이펙티브 타입스크립트(2판)를 바탕으로 했으며, 책의 예제를 하나하나 직접 컴파일러에 돌려(TypeScript 5.9 기준) 에러 메시지와 추론된 타입을 확인하며 학습 및 정리했습니다.

이 책은 "이렇게 하라"는 조언 83개로 이루어져 있지만, 조언을 그대로 옮기는 대신 그 조언이 나온 이유 — 타입스크립트가 왜 그렇게 동작하는지 — 를 중심으로 재구성했습니다. 각 노트는 하나의 궁금증에서 시작해, 답을 찾는 과정에서 다음 질문으로 자연스럽게 이어지도록 구성했습니다.

## 질문 지도

타입스크립트는 자바스크립트 위에 타입이라는 다른 층을 얹은 언어입니다. 공부해 보니 헷갈리는 지점 대부분이 "이 코드는 어느 층에서 실행되는가"를 놓치는 데서 나왔고, 질문도 그 경계를 따라 이어졌습니다.

```
타입 에러가 있는데 왜 컴파일은 될까?
└─ 타입이 빌드 때 지워진다면, 런타임에 타입 확인은 어떻게 하지?

선언한 적 없는 타입인데 왜 할당이 될까?
└─ 그럼 왜 객체 리터럴을 바로 넘기면 에러가 날까?
   └─ "구조가 맞으면 할당된다"를 더 정확히 말하면?  (타입 = 집합)
      └─ 그 '타입'이라는 이름은 어느 공간에 존재할까?

let으로 선언하면 string인데 const면 왜 'x'일까?
└─ 선언한 뒤에 타입이 바뀌는 것처럼 보이는 건 뭘까?
   └─ 인라인 콜백은 되는데 변수로 빼면 왜 에러일까?

any를 쓰면 정확히 뭐가 위험해질까?
└─ 컴파일러가 모르는 걸 내가 알 때는 어떻게 하지?
   └─ 그런데 타입 체크를 통과하면 정말 안전한 걸까?

type과 interface 중 뭘 써야 할까?
└─ 도구보다 중요한 질문: 잘못된 상태를 타입으로 막을 수 있을까?
   └─ null은 타입의 어디에 둬야 할까?

Partial<T> 같은 유틸리티 타입은 어떻게 만들어진 걸까?
└─ 제네릭이 타입의 함수라면, 조건문도 있을까?
```

## 글 목록

### 타입스크립트라는 언어

1. [타입 에러가 있는데 왜 컴파일은 되는가](/typescript/01-ts-js-relationship) — 상위집합, 타입 체크와 컴파일의 독립, 타입 소거
2. [런타임에 타입은 어떻게 확인하나](/typescript/02-runtime-types) — instanceof의 한계, in 연산자, 태그, class

### 구조적 타입 시스템

3. [선언한 적 없는 타입인데 왜 할당이 되는가](/typescript/03-structural-typing) — 덕 타이핑, 봉인되지 않은 타입
4. [객체 리터럴만 더 엄격하게 검사되는 이유](/typescript/04-excess-property-checking) — 잉여 속성 검사 vs 할당 가능성
5. [타입은 값의 집합이다](/typescript/05-types-as-sets) — never~unknown, 유니온과 인터섹션, 부분집합
6. [같은 이름이 타입도 되고 값도 된다](/typescript/06-type-value-space) — 타입 공간과 값 공간, typeof의 두 얼굴

### 타입 추론

7. [let은 string인데 const는 왜 'x'인가](/typescript/07-widening) — 넓히기, as const
8. [타입스크립트는 코드 흐름을 읽는다](/typescript/08-narrowing) — 좁히기, 타입 가드
9. [인라인은 되는데 변수로 빼면 왜 에러인가](/typescript/09-context-inference) — 문맥 추론, 함수 표현식 타입

### any와 타입 안전성

10. [any 대신 unknown을 쓰라는 이유](/typescript/10-any-unknown-never) — any의 전염성, unknown, never
11. [as는 언제 써야 하는가](/typescript/11-type-assertions) — 단언 vs 선언, non-null 단언
12. [타입 체크를 통과했는데 왜 런타임 에러가 나는가](/typescript/12-unsoundness) — 건전성의 구멍들

### 타입 설계

13. [type과 interface, 뭘 써야 하나](/typescript/13-type-vs-interface) — 유니온, 선언 병합, 확장
14. [잘못된 상태를 표현할 수 없게 만들기](/typescript/14-discriminated-union) — 태그된 유니온, never 완전성 검사
15. [null은 타입의 어디에 둬야 하나](/typescript/15-null-handling) — strictNullChecks, null을 껍데기로 밀기

### 제네릭과 타입 연산

16. [제네릭은 타입의 함수다](/typescript/16-generics-as-functions) — extends 제약, 불필요한 타입 파라미터
17. [Partial은 어떻게 만들어지는가](/typescript/17-mapped-utility-types) — keyof, 매핑된 타입, Object.keys의 진실
18. [타입에도 조건문이 있다](/typescript/18-conditional-types) — 조건부 타입, 유니온 분배, 템플릿 리터럴
