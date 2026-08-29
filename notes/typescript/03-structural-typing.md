---
title: 선언한 적 없는 타입인데 왜 할당이 되는가
description: 구조적 타이핑 — 타입스크립트가 이름이 아니라 구조를 보는 이유
---

# 선언한 적 없는 타입인데 왜 할당이 되는가

타입스크립트의 타입 시스템이 본격적으로 낯설어진 건 이 코드부터였다.

```typescript
interface Vector2D {
  x: number;
  y: number;
}
function calculateLength(v: Vector2D) {
  return Math.sqrt(v.x ** 2 + v.y ** 2);
}

interface NamedVector {
  name: string;
  x: number;
  y: number;
}
const v: NamedVector = { x: 3, y: 4, name: 'Pythagoras' };
calculateLength(v); // 이 호출은 컴파일될까?
```

`NamedVector`는 `Vector2D`와 아무 관계도 선언하지 않았다. `extends`도 없고 `implements`도 없다. 다른 언어의 감각으로는 당연히 에러다. 그런데 타입스크립트는 **통과**시키고, 실행하면 5가 나온다.

## 이름이 아니라 구조를 본다

자바에서 타입 호환은 이름으로 맺은 관계를 따라간다. `NamedVector`가 `Vector2D`가 되려면 그렇게 **선언**해야 한다. 이런 방식을 명목적 타이핑(nominal typing)이라고 부른다.

타입스크립트는 반대다. `NamedVector`의 값은 `x: number`와 `y: number`를 갖고 있다. `Vector2D`가 요구하는 구조를 이미 만족하니까, 선언 여부와 무관하게 `Vector2D`다. 이걸 **구조적 타이핑**(structural typing)이라고 한다.

왜 이렇게 설계했을까? 자바스크립트가 원래 이렇게 동작하기 때문이다. 자바스크립트의 함수는 인자가 어떤 "타입 이름"을 갖는지 물어본 적이 없다. `x`와 `y`만 있으면 어떤 객체든 받아서 잘 굴러간다 — 오리처럼 걷고 오리처럼 꽥꽥대면 오리로 취급하는 **덕 타이핑**(duck typing)이다. [첫 글](/typescript/01-ts-js-relationship)에서 타입스크립트의 목표는 자바스크립트의 런타임 동작을 모델링하는 것이라고 했는데, 덕 타이핑을 모델링한 결과가 구조적 타이핑인 셈이다.

## 타입은 봉인되지 않았다

여기서 사고를 한 번 뒤집어야 했다. 나는 `Vector2D`라고 선언하면 "x와 y**만** 있는 객체"라고 생각했다. 그런데 방금 본 것처럼 `name`이 더 있는 값도 `Vector2D`다. 즉 타입 선언은 **최소 요구 조건**이지 전체 명세가 아니다. 어떤 타입의 값은 선언에 없는 속성을 얼마든지 더 들고 있을 수 있다 — 타입은 열려(open) 있고, 봉인(sealed)되어 있지 않다.

이 사실을 잊으면 이런 코드에서 뒤통수를 맞는다.

```typescript
interface Vector3D {
  x: number;
  y: number;
  z: number;
}
function calculateLengthL1(v: Vector3D) {
  let length = 0;
  for (const axis of Object.keys(v)) {
    const coord = v[axis];
    //            ~~~~~~~ Element implicitly has an 'any' type because ...
    //                    'string' can't be used to index type 'Vector3D'
    length += Math.abs(coord);
  }
  return length;
}
```

"`Vector3D`의 키는 x, y, z 셋뿐이니 `v[axis]`는 당연히 number"라고 생각했는데 에러가 난다. 처음엔 컴파일러가 융통성이 없다고 생각했다. 하지만 타입이 열려 있다는 걸 받아들이면 컴파일러가 맞다. `{x: 3, y: 4, z: 1, address: '123 Broadway'}` 같은 값도 완벽한 `Vector3D`고, 이 값이 들어오면 `v[axis]`는 문자열일 수 있다. `Object.keys`로 타입을 순회하려는 시도가 왜 자꾸 막히는지는 뒤에서 keyof를 다룰 때 다시 만난다.
