---
title: 런타임에 타입은 어떻게 확인하나
description: instanceof로 인터페이스를 검사할 수 없는 이유 — 속성 검사, 태그, class
---

# 런타임에 타입은 어떻게 확인하나

[지난 글](/typescript/01-ts-js-relationship)에서 타입은 빌드 때 전부 지워진다고 했다. 그 말을 듣자마자 걱정된 상황이 있다. 값의 타입에 따라 분기해야 하는 함수는 어떻게 짜지? 마침 책에서 정확히 그 상황을 다루는 코드를 만났다.

```typescript
interface Square {
  width: number;
}
interface Rectangle extends Square {
  height: number;
}
type Shape = Square | Rectangle;

function calculateArea(shape: Shape) {
  if (shape instanceof Rectangle) {
    return shape.width * shape.height;
  } else {
    return shape.width * shape.width;
  }
}
```

이 코드는 컴파일될까? 나는 된다고 생각했다. `instanceof`는 자바스크립트에서 늘 쓰던 연산자니까. 그런데 컴파일러의 답은 이랬다.

```
error TS2693: 'Rectangle' only refers to a type, but is being used as a value here.
```

그 아래로 `Property 'height' does not exist on type 'Shape'.`까지 하나 더 딸려 나온다. 분기가 무효가 되니 좁히기도 실패한 것이다. "Rectangle은 타입일 뿐인데 값으로 쓰고 있다"는 첫 에러가 원인이다. 처음엔 에러 메시지 자체가 수수께끼였다.

## 층이 어긋난 코드

곰곰이 보면 이 코드는 두 개의 층을 무단으로 넘나들고 있다. `instanceof`는 **런타임에 실행되는** 자바스크립트 연산자다. 그런데 `Rectangle`은 인터페이스, 즉 **빌드 때 지워지는** 타입이다. 런타임 시점에 `Rectangle`이라는 이름은 이 세상에 존재하지 않는다. 존재하지 않는 것과 비교할 수는 없다.


지난 글의 결론을 여기에 적용하면 이렇게 된다. **런타임에 타입을 확인하고 싶다면, 런타임까지 살아남는 무언가에 타입 정보를 실어 보내야 한다.** 방법은 세 가지다.

## 방법 1 — 값에 이미 있는 속성을 검사한다

`Rectangle`이라는 이름은 지워져도, 사각형 객체가 들고 있는 `height` 속성은 런타임에 실재한다.

```typescript
function calculateArea(shape: Shape) {
  if ('height' in shape) {
    return shape.width * shape.height; // 여기서 shape는 Rectangle
  } else {
    return shape.width * shape.width; // 여기서 shape는 Square
  }
}
```

흥미로운 건 타입 체커의 반응이다. `if` 블록 안에서 `shape`에 마우스를 올리면 `Rectangle`로 좁혀져 있다. 런타임 검사는 자바스크립트가 하는데, 타입 체커가 그 검사를 읽고 타입 층에 반영해 주는 것이다. 이 "좁히기"가 어디까지 똑똑한지는 나중에 따로 파본다.

## 방법 2 — 태그를 붙인다

속성 유무로 구분하는 게 우연에 기대는 느낌이라면, 아예 구분용 값을 명시적으로 넣을 수 있다.

```typescript
interface Square {
  kind: 'square';
  width: number;
}
interface Rectangle {
  kind: 'rectangle';
  width: number;
  height: number;
}
type Shape = Square | Rectangle;

function calculateArea(shape: Shape) {
  if (shape.kind === 'rectangle') {
    return shape.width * shape.height;
  } else {
    return shape.width * shape.width;
  }
}
```

`kind`는 평범한 문자열 속성이라 런타임에 존재하고, 타입 체커도 `kind` 비교로 타입을 정확히 좁힌다. 이 패턴을 **태그된 유니온**(tagged union)이라고 부르는데, 사실 타입스크립트 설계 전반에서 제일 중요한 패턴 중 하나라 뒤에서 한 편을 통째로 쓸 예정이다.
