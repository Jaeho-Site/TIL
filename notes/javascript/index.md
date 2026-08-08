---
title: JavaScript
description: 궁금증을 따라가며 정리한 JavaScript 공부 기록
---

# JavaScript

JavaScript를 공부하며 생긴 궁금증을 하나씩 해결해 나간 기록입니다.

기본서는 모던 자바스크립트 Deep Dive를 바탕으로 했으며, 책의 예제를 하나하나 직접 실행하고 결과를 확인하며 학습 및 정리했습니다.

개념의 'Why'를 고민할수록 이해가 깊어진다고 생각합니다. 그래서 각 노트는 하나의 질문에서 시작해, 그 답을 찾아가는 과정에서 다음 질문으로 자연스럽게 이어지도록 구성했습니다.

정리하다 보니 내용과 예제가 모던 자바스크립트 Deep Dive를 따라갔지만, 단순히 내용을 옮기는 것이 아니라 '왜 이렇게 동작할까?', '왜 이렇게 설계되었을까?'를 고민하며 이해한 과정을 중심으로 기록했습니다.

## 질문 지도

JavaScript는 프론트엔드의 기본이 되는 언어입니다. 처음에는 교재를 따라 공부했고, 이번에 다시 책을 읽으며 개념을 정리했습니다.

언어를 공부하다 보면 하나의 궁금증이 또 다른 질문으로 이어집니다. 그 질문을 하나씩 해결할수록 앞서 배운 개념까지 더 선명해지고, 이해의 깊이도 달라집니다.

JavaScript를 공부하며 중요하거나 헷갈렸던 개념들을 이런 질문의 흐름으로 이어봤습니다.


```
원시 값은 그대로 복사되는데 객체는 왜 같이 바뀌지?
└─ 그럼 객체를 제대로 복사하려면 어떻게 해야 하지?
   └─ 객체끼리 ===로 비교하면 왜 false가 나오지?

변수 선언이 코드보다 먼저 처리된다는 게 무슨 뜻이지?
└─ 그런데 왜 let은 선언 전에 접근하면 에러가 날까?
   └─ 변수는 어디까지 접근할 수 있는 걸까?
      └─ 함수가 끝났는데도 그 안의 변수를 기억할 수 있다고?

this는 함수가 만들어질 때 정해지는 게 아닌가?
└─ 호출할 때마다 달라진다면 어떤 규칙으로 결정되지?
   └─ 그런데 화살표 함수는 왜 그 규칙을 따르지 않을까?

자바스크립트에는 클래스가 없었다는데 상속은 어떻게 했을까?
└─ 프로토타입 체인은 실제로 어떻게 이어질까?
   └─ new를 붙이면 대체 무슨 일이 일어나지?
      └─ 그렇다면 class는 정말 문법만 바꾼 걸까?

함수가 '일급 객체'라는 건 단순히 변수에 담을 수 있다는 뜻인가?
└─ 그렇다면 일반 함수와 화살표 함수는 무엇이 다를까?

자바스크립트는 싱글 스레드인데 비동기 작업은 어떻게 처리하지?
└─ setTimeout과 Promise가 같이 있으면 무엇부터 실행될까?
   └─ Promise는 콜백에서 무엇을 해결한 걸까?
      └─ async/await은 Promise와 완전히 다른 방식일까?
         └─ 여러 비동기 작업을 꼭 하나씩 기다려야 할까?

for...of와 for...in은 이름도 비슷한데 왜 결과가 다르지?
└─ 반복할 수 있다는 건 정확히 무슨 뜻일까?

브라우저에서 JS 파일을 나누려면 원래 어떻게 했을까?
└─ ESM과 CommonJS는 무엇이 다르지?
   └─ ESM이 있는데도 왜 번들러가 필요할까?
```

## 글 목록

### 데이터 타입과 메모리

1. [원시 타입과 객체는 뭐가 다른가](/javascript/01-primitive-vs-object) — 값 vs 참조, 불변성, 래퍼 객체
2. [얕은 복사와 깊은 복사는 뭐가 다른가](/javascript/02-shallow-deep-copy) — 스프레드의 1층 한계, structuredClone
3. [==와 ===는 뭐가 다른가](/javascript/03-equality) — NaN, 0.1+0.2, 참조 비교, Object.is

### 실행 컨텍스트와 스코프

4. [호이스팅은 왜 일어나는가](/javascript/04-hoisting) — 평가/실행 2단계, 함수 선언문 vs 표현식
5. [var와 let/const는 뭐가 다른가](/javascript/05-var-let-const) — TDZ, 블록 스코프, 전역 객체 오염
6. [스코프 체인은 어떻게 만들어지는가](/javascript/06-scope-chain) — 렉시컬 스코프, 섀도잉, [[Environment]]

### 클로저

7. [클로저는 어떻게 가능한가](/javascript/07-closure) — 렉시컬 환경, GC, 자유 변수
8. [클로저는 어디에 쓰는가](/javascript/08-closure-in-practice) — 은닉, 디바운스, var 반복문, stale closure

### this

9. [this는 언제 결정되는가](/javascript/09-this-binding) — 호출 방식별 바인딩 4가지 규칙, strict mode
10. [화살표 함수의 this는 왜 다른가](/javascript/10-arrow-function-this) — 렉시컬 this, call/apply/bind, React의 bind

### 프로토타입과 클래스

11. [자바스크립트의 상속은 어떻게 동작하는가](/javascript/11-prototype-chain) — 프로토타입 체인, __proto__ vs prototype
12. [new는 무슨 일을 하는가](/javascript/12-new-and-constructor) — 인스턴스 생성 4단계, instanceof
13. [class는 문법 설탕인가](/javascript/13-class-sugar) — new 강제, TDZ, strict mode, getter/setter

### 함수

14. [함수가 일급 객체라는 게 무슨 의미인가](/javascript/14-first-class-function) — 콜백, 고차 함수, rest 파라미터
15. [화살표 함수와 일반 함수는 뭐가 다른가](/javascript/15-arrow-vs-normal) — ES6 함수 삼분법, 화살표 함수에 없는 4가지

### 비동기

16. [싱글 스레드인데 어떻게 동시에 처리하나](/javascript/16-event-loop) — 콜 스택, 태스크 큐, 이벤트 루프, 블로킹
17. [Promise.then과 setTimeout, 누가 먼저인가](/javascript/17-micro-macro-task) — 마이크로/매크로태스크, setTimeout(0)의 진실
18. [콜백의 진짜 문제는 무엇이고, 프로미스는 뭘 해결했나](/javascript/18-promise) — 3가지 상태, then 체이닝, catch의 위치
19. [async/await은 어떻게 동작하나](/javascript/19-async-await) — 일시정지와 재개, try/catch 통일, await 누락 함정
20. [Promise.all은 언제 쓰나](/javascript/20-promise-combinators) — 순차 vs 병렬, allSettled·race·any

### 이터러블과 모듈

21. [for...of와 for...in은 뭐가 다른가](/javascript/21-iterable) — 이터러블 프로토콜, 스프레드의 조건, 유사 배열
22. [ESM과 CJS는 뭐가 다른가](/javascript/22-esm-vs-cjs) — IIFE의 시대, 라이브 바인딩, 정적 구조
23. [번들러는 왜 여전히 쓰나](/javascript/23-bundler-babel) — 트리 셰이킹, 바벨 vs 폴리필
