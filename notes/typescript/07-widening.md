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
