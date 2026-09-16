---
title: any 대신 unknown을 쓰라는 이유
description: any의 전염성, unknown의 안전장치, 그리고 never까지 — 세 극단 타입의 정확한 차이
---

# any 대신 unknown을 쓰라는 이유

YAML 파서의 타입 선언이 `(yaml: string) => any`로 되어 있는 코드를 봤다. 파싱 결과는 뭐가 나올지 모르니 `any`가 자연스러워 보였다. 퀴즈: 이 코드는 어디까지 컴파일될까?

```typescript
declare function parseYAML(yaml: string): any;

const book = parseYAML(`
  name: Jane Eyre
  author: Charlotte Brontë
`);
console.log(book.title); // (1) 존재하지 않는 속성 접근
book('read');            // (2) 객체를 함수로 호출
```

답: **끝까지 전부 통과한다.** (1)은 런타임에 `undefined`를 찍고, (2)는 `book is not a function`으로 터진다. 타입 에러는 한 건도 없다.

## any는 타입이 아니라 스위치다

[타입은 값의 집합](/typescript/05-types-as-sets)이라고 했는데, `any`는 그 세계관의 바깥에 있다. `any`는 **모든 타입에 할당 가능하면서 동시에 모든 타입을 할당받는다.** 부분집합 관계로는 성립할 수 없는 조합이다(그게 가능한 건 공집합뿐인데, `any`는 모든 값을 받는다). 재밌게도 컴파일러가 이 논리를 정확히 알고 있어서, 유일한 예외로 `any`조차 `never`에는 할당하지 못한다 — 공집합에는 그 무엇도 넣을 수 없으니까. 즉 `any`는 집합이 아니라 "이 값에 대해서는 검사를 하지 마라"는 스위치다.

문제는 이 스위치가 **전염**된다는 것이다.

```typescript
let ageInYears: number;
ageInYears = '12' as any; // 통과
ageInYears += 1;          // 통과. 런타임에 ageInYears는 "121"
```

`any`는 `number` 자리에 조용히 들어가고, 그 순간부터 `ageInYears: number`라는 선언은 거짓말이 된다. 이후의 코드는 전부 그 거짓말 위에서 검사받는다. 함수 반환 타입이 `any`면 호출부 전체로, 그 반환값을 담은 변수를 넘긴 곳으로 계속 번진다. 처음 `any`를 쓴 자리에서 멀리 떨어진 곳에서 사고가 나기 때문에 원인 추적도 어렵다.

타입을 안 적어도 같은 일이 생긴다. 컴파일러가 추론에 실패하면 **암시적 any**가 되는데, `noImplicitAny` 옵션(strict에 포함)이 이걸 에러로 승격시킨다. 이 옵션 없이는 매개변수 타입을 깜빡한 함수 하나가 검사망의 구멍이 된다 — 개인적으로 strict를 못 켠 프로젝트라면 이 옵션 하나라도 먼저 켜는 게 맞다고 생각한다.
