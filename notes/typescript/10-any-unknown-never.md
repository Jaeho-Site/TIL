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

## unknown — "모른다"를 타입답게 말하기

그런데 `parseYAML`의 사정도 이해는 된다. 정말로 뭐가 나올지 모르니까. "모른다"를 표현하고 싶었던 것뿐인데, `any`는 "모르니까 검사도 하지 마"가 돼버렸다. 타입답게 "모른다"를 말하는 타입이 따로 있다 — `unknown`, 모든 값을 담는 전체집합이다.

```typescript
function safeParseYAML(yaml: string): unknown {
  return parseYAML(yaml);
}

const book = safeParseYAML(`
  name: Villette
  author: Charlotte Brontë
`);
console.log(book.title);
//          ~~~~~ 'book' is of type 'unknown'
book('read');
// ~~~~ 'book' is of type 'unknown'
```

`any`와 똑같이 아무 값이나 받지만, 방향이 하나 막혀 있다. `unknown`은 **거의 어디에도 할당할 수 없고, 어떤 속성에도 접근할 수 없다.** 모든 값의 집합이니 어떤 구체적 타입의 부분집합도 아니기 때문이다 — 집합 규칙이 그대로 살아 있다.

쓰려면 어떻게 해야 하나? [좁혀야](/typescript/08-narrowing) 한다. `instanceof`, 타입 서술어, 손수 만든 검증 함수 — 뭐든 컴파일러가 읽을 수 있는 증거를 대야 접근이 열린다.

```typescript
interface Book {
  name: string;
  author: string;
}

function isBook(value: unknown): value is Book {
  return (
    typeof value === 'object' && value !== null &&
    'name' in value && 'author' in value
  );
}

const book = safeParseYAML(input);
if (isBook(book)) {
  book.name; // 통과 — 검증을 거쳤다
}
```

`any`가 "검사 생략"이라면 `unknown`은 "검사 유예"다. 값의 정체를 모르는 채로 받되, 쓰는 시점에 반드시 증명을 요구한다. 외부에서 들어오는 값([런타임 경계](/typescript/02-runtime-types)를 넘는 값)의 기본 타입으로 `unknown`이 정답인 이유다.

한 가지 함정도 책에서 배웠다. `function safeParseYAML<T>(yaml: string): T`처럼 **반환에만 쓰이는 제네릭**은 안전해 보이지만, 호출자가 `T`를 마음대로 정하는 순간 검증 없는 단언과 같아진다. `unknown`을 반환하고 호출자가 명시적으로 좁히게 하는 쪽이 정직하다.

## 반대쪽 끝의 never

`unknown`의 정반대 극단이 `never`(공집합)다. 둘을 나란히 놓으면 대칭이 깨끗하게 보인다.

- `unknown` — 모든 값이 **들어올 수 있지만**, 좁히기 전엔 **아무것도 할 수 없다**
- `never` — 어떤 값도 **들어올 수 없지만**, 모든 타입에 **할당할 수 있다** (공집합은 모든 집합의 부분집합)
- `any` — `never`로 들어가는 방향만 빼고 양방향 다 통과. 집합 규칙 밖의 스위치

![unknown부터 never까지 집합 크기 순으로 놓인 사다리에서 할당은 작은 집합에서 큰 집합 방향으로만 흐르고, any만 never로 들어가는 것을 제외한 모든 방향을 통과하는 예외로 표시된 구조](/images/typescript/10-assignability-ladder.png)

`never`가 어디에 쓰이는지는 타입 설계를 다룰 때 제대로 나온다 — 도달할 수 없는 코드와 빠뜨린 분기를 컴파일러가 잡게 만드는 재료다.

---

`any`와 `unknown`은 "아무 값이나"라는 점에서 같아 보이지만, **any는 타입 시스템의 스위치를 끄고 unknown은 켠 채로 모름을 표현한다**. 그런데 unknown을 쓰다 보면 결국 `as`로 단언하는 자리가 생기는데, 그 단언은 대체 언제 정당한 걸까. → [as는 언제 써야 하는가](/typescript/11-type-assertions)
