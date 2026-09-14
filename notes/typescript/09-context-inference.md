---
title: 인라인은 되는데 변수로 빼면 왜 에러인가
description: 문맥 추론 — 값이 놓인 자리가 타입을 결정한다, 그리고 함수 표현식 타입
---

# 인라인은 되는데 변수로 빼면 왜 에러인가

리팩터링을 하다 보면 인라인으로 쓰던 값을 변수로 뽑는 일이 흔하다. 동작이 바뀔 리 없는 기계적인 정리인데, 타입스크립트에서는 이 정리가 에러를 만든다.

```typescript
type Language = 'JavaScript' | 'TypeScript' | 'Python';
function setLanguage(language: Language) { /* ... */ }

setLanguage('JavaScript'); // 통과

let language = 'JavaScript';
setLanguage(language);
//          ~~~~~~~~ Argument of type 'string' is not assignable
//                   to parameter of type 'Language'
```

같은 `'JavaScript'`인데 인라인이면 되고 변수면 안 된다. [넓히기](/typescript/07-widening)를 읽었다면 절반은 설명할 수 있다 — `let language`는 `string`으로 넓혀졌으니까. 그런데 그 설명은 곧바로 다음 질문을 부른다. **인라인일 때는 왜 안 넓혀졌을까?**

## 추론은 값만 보지 않고 자리를 본다

타입스크립트는 값의 타입을 추론할 때 값 자체만 보는 게 아니라, **그 값이 놓인 문맥**(context)을 함께 본다. `setLanguage('JavaScript')`에서 리터럴은 `Language` 타입의 매개변수 자리에 놓여 있다. 컴파일러는 이 기대 타입을 보고 "아, 여기서는 `string`으로 넓힐 게 아니라 리터럴 그대로 두는 게 맞겠다"고 판단한다.

변수로 빼는 순간 이 문맥이 끊긴다. `let language = 'JavaScript'`가 평가되는 시점에 컴파일러는 이 값이 나중에 `setLanguage`로 들어갈 거라는 걸 알 수 없다. 문맥 없이 홀로 선 리터럴은 기본 규칙대로 넓혀지고, 그 결과가 호출부에서 어긋난다. 해결은 끊긴 문맥을 이어주는 것이다 — 주석으로 의도를 밝히거나(`let language: Language`), `const`로 리터럴 타입을 유지한다.

튜플에서는 이 어긋남이 더 아프게 온다.

```typescript
function panTo(where: [number, number]) { /* ... */ }

panTo([10, 20]); // 통과

const loc = [10, 20];
//    ^? const loc: number[]
panTo(loc);
//    ~~~ Argument of type 'number[]' is not assignable to
//        parameter of type '[number, number]'
```

`const`인데도 실패한다. 배열 리터럴은 문맥이 없으면 애초에 튜플이 아니라 `number[]`로 추론되기 때문이다 — 길이 정보는 처음부터 기록되지 않는다. `as const`를 붙이면 이번엔 `readonly [10, 20]`이 돼서 mutable 튜플 자리에 못 들어간다 — 받는 쪽 시그니처를 `readonly [number, number]`로 고치는 게 제일 깔끔했다. 개인적으로 이 사례에서 배운 건, 문맥에서 떼어낸 값이 만드는 에러는 **선언 지점이 아니라 사용 지점에서 터진다**는 점이다. 에러가 난 줄이 아니라 몇 줄 위의 선언이 진범인 경우가 많다.
