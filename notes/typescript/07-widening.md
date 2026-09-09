---
title: let은 string인데 const는 왜 'x'인가
description: 넓히기 — 컴파일러가 리터럴에서 타입을 고르는 방식과 as const
---

# let은 string인데 const는 왜 'x'인가

타입 주석을 하나도 안 썼는데 에러가 나는 코드를 만났다.

```typescript
interface Vector3 {
  x: number;
  y: number;
  z: number;
}
function getComponent(vector: Vector3, axis: 'x' | 'y' | 'z') {
  return vector[axis];
}

let x = 'x';
let vec = { x: 10, y: 20, z: 30 };
getComponent(vec, x);
//                ~ Argument of type 'string' is not assignable
//                  to parameter of type '"x" | "y" | "z"'
```

`x`에는 분명 `'x'`가 들어 있다. `'x'`는 `'x' | 'y' | 'z'`의 당당한 원소인데 왜 못 넘길까. 더 이상한 건, `let`을 `const`로 바꾸기만 하면 통과한다는 것이다.

```typescript
const x = 'x'; // 통과. x의 타입: "x"
getComponent(vec, x);
```

값은 똑같은데 선언 키워드 하나로 결과가 갈렸다.

## 추론은 집합 고르기 문제다

에러 메시지를 다시 보면 단서가 있다. `let x = 'x'`에서 `x`의 타입은 `'x'`가 아니라 `string`으로 추론됐다. [타입은 값의 집합](/typescript/05-types-as-sets)이라는 관점을 빌리면, 컴파일러는 `'x'`라는 값 하나를 보고 **이 변수에 앞으로 담길 값들의 집합**을 골라야 한다. 후보는 여럿이다. `'x'`(원소 하나), `string`(모든 문자열), 심하게는 `unknown`까지.

`let`은 재할당이 가능하다. 컴파일러는 "이 사람이 나중에 `x = 'hello'`라고 쓸 수도 있겠지"라고 가정하고, 리터럴보다 넓은 `string`을 고른다. 이 과정을 **넓히기**(widening)라고 부른다. 반면 `const`는 재할당이 불가능하니 값이 `'x'`에서 변할 일이 없고, 원소 하나짜리 리터럴 타입 `"x"`를 유지한다.

즉 이 에러는 컴파일러가 틀린 게 아니라, **내 의도(문자 'x' 하나만 담는다)와 컴파일러의 추측(아무 문자열이나 담을 것이다)이 어긋난** 것이다. 넓히기는 추측이므로, 의도를 알려주면 조절할 수 있다.

## 객체에서는 const로도 부족하다

그럼 `const`면 다 해결되냐면, 객체는 또 다르다.

```typescript
const obj1 = { x: 1, y: 2 };
//    ^? const obj1: { x: number; y: number; }
```

`const`로 선언했는데 `x`는 `1`이 아니라 `number`다. 자바스크립트에서 `const`는 **재할당만** 막을 뿐 속성 변경은 막지 않는다 — `obj1.x = 3`은 합법이다. 그래서 속성은 `let` 변수처럼 넓혀진다. 개인적으로 이 지점이 원시 값/객체의 `const` 동작 차이를 타입 층에서 그대로 재현한 거라 재밌었다.

속성까지 리터럴로 고정하고 싶으면 `as const`를 쓴다.

```typescript
const obj2 = { x: 1 as const, y: 2 };
//    ^? const obj2: { x: 1; y: number; }
const obj3 = { x: 1, y: 2 } as const;
//    ^? const obj3: { readonly x: 1; readonly y: 2; }

const arr1 = [1, 2, 3];
//    ^? const arr1: number[]
const arr2 = [1, 2, 3] as const;
//    ^? const arr2: readonly [1, 2, 3]
```

추론이 선언 시점에 일어난다는 건 객체를 만드는 습관에도 영향을 준다. 자바스크립트에서 하던 대로 빈 객체에 속성을 하나씩 붙이면, 선언 시점의 추론(`{}`)이 그대로 박제되어 이후 속성 추가가 전부 에러가 된다.

```typescript
const pt = {};
pt.x = 3;
// ~ Property 'x' does not exist on type '{}'.
```

객체는 한 번에, 속성을 다 갖춘 리터럴로 만드는 게 타입스크립트와 결이 맞는 방식이다.

`as const`는 "이 값은 최대한 좁게, 변경 없음으로 추론해라"라는 지시다. 배열은 길이까지 고정된 readonly 튜플이 된다. `as`가 붙어 있지만 타입을 속이는 단언과 달리 추론 방식만 바꾸는 것이라 안전하다.

## 넓히기를 다루는 세 번째 길, satisfies

타입 주석을 붙이면 넓히기를 원천 차단할 수 있지만(`const obj: { x: 1 } = ...`), 주석은 추론을 **덮어써** 버린다. 검사는 받고 싶은데 추론된 구체적 타입은 유지하고 싶을 때를 위해 `satisfies`가 있다.

```typescript
type Point = [number, number];

const capitals1 = { ny: [-73.7562, 42.6526], ca: [-121.4944, 38.5816] };
//    ^? const capitals1: { ny: number[]; ca: number[]; }  — 튜플 정보 소실

const capitals2 = {
  ny: [-73.7562, 42.6526],
  ca: [-121.4944, 38.5816],
} satisfies Record<string, Point>;
//    ^? const capitals2: { ny: [number, number]; ca: [number, number]; }
```

`satisfies`는 "이 조건을 만족하는지 **검사만** 하고, 타입은 추론된 걸 그대로 써라"다. `capitals1`처럼 좌표 쌍이 `number[]`로 추론되어 길이 정보를 잃는 걸 막으면서, 요소를 3개 넣는 실수는 에러로 잡아준다.

덧붙이면, 넓히기가 잘 동작하는 평범한 자리에는 타입 주석을 굳이 달 필요가 없다. `let x: string = 'x'`의 주석은 추론과 똑같은 정보를 반복할 뿐이다. 주석이 진짜 필요한 곳은 함수 시그니처처럼 의도를 계약으로 못 박는 자리, 그리고 넓히기가 의도와 어긋나는 자리다.

---

변수의 타입은 초기값에서 기계적으로 나오는 게 아니라, **컴파일러가 "앞으로 담길 값의 집합"을 추측한 결과**고, `const`·`as const`·주석·`satisfies`는 그 추측에 개입하는 도구들이다. 그런데 추론된 타입이 선언 시점에 고정되는 거라면, `if (typeof x === 'string')` 같은 분기 안에서 타입이 바뀌는 것처럼 보이는 건 뭘까. → [타입스크립트는 코드 흐름을 읽는다](/typescript/08-narrowing)
