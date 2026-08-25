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
