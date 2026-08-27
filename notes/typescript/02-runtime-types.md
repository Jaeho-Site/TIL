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

![컴파일 전에는 타입 층의 interface들과 값 층의 함수가 함께 있지만, 빌드가 타입을 지우면 런타임에는 값 층만 남아 instanceof Rectangle이 참조할 값이 없는 구조](/images/typescript/02-type-erasure.png)

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

## 방법 3 — class로 만든다

`interface` 대신 `class`로 선언하면 처음의 `instanceof` 코드가 그대로 동작한다.

```typescript
class Square {
  constructor(public width: number) {}
}
class Rectangle extends Square {
  constructor(width: number, public height: number) {
    super(width);
  }
}
type Shape = Square | Rectangle;

function calculateArea(shape: Shape) {
  if (shape instanceof Rectangle) {
    return shape.width * shape.height; // 통과. shape: Rectangle
  } else {
    return shape.width * shape.width;
  }
}
```

왜 클래스는 될까? `class Rectangle`은 **타입도 만들고 값도 만들기** 때문이다. 타입 층에는 인스턴스의 형태가 등록되고, 런타임에는 생성자 함수가 실재한다. `instanceof Rectangle`이 참조하는 건 그 생성자 함수 쪽이다. 하나의 이름이 두 층에 동시에 존재한다는 이 사실은 생각보다 자주 헷갈림을 만드는 주제라, 이것도 별도 노트에서 다룬다.

다만 `instanceof`는 프로토타입 체인을 타는 검사라는 함정이 있다. `JSON.parse`로 복원한 값이나 서버 응답은 생긴 게 똑같아도 `Rectangle`의 프로토타입을 갖고 있지 않아서 `instanceof`가 항상 `false`다. 즉 class 방식은 **내 코드가 직접 생성한 값**에만 통한다.

## 그럼 서버에서 온 값은 누가 검사하나

여기까지 정리하고 나니 더 무서운 질문이 남았다. `fetch`로 받은 응답에 타입을 붙이는 코드, 다들 이렇게 쓴다.

```typescript
function setLightSwitch(value: boolean) { /* 조명 on/off */ }

interface LightApiResponse {
  lightSwitchValue: boolean;
}
async function setLight() {
  const response = await fetch('/light');
  const result: LightApiResponse = await response.json();
  setLightSwitch(result.lightSwitchValue);
}
```

타입 체크는 통과한다. 하지만 이 타입 선언은 **희망 사항**일 뿐이다. 서버가 `lightSwitchValue`를 문자열로 보내면? 타입은 지워졌으니 아무도 검사하지 않고, 잘못된 값이 프로그램 깊숙이 흘러 들어간다. 런타임 경계(네트워크, 로컬 스토리지, 사용자 입력)를 넘어오는 값은 타입 시스템의 보호 밖에 있다.

그래서 경계에서는 결국 런타임 검증 코드가 필요하다. `typeof`와 `in`으로 손수 검사하거나, Zod처럼 **런타임 검증기에서 정적 타입을 뽑아내는** 라이브러리를 쓴다. 개인적으로 이 구도가 재밌었는데, 타입스크립트가 지운 타입을 결국 값의 세계에서 다시 지어 올리는 셈이기 때문이다.

---

런타임에 타입을 확인한다는 건 타입을 조회하는 게 아니라, **런타임까지 살아남는 값(속성, 태그, 생성자)에 타입 정보를 미리 실어두는 것**이다. 타입과 값이 서로 다른 층에 산다는 감각만 있으면 세 가지 방법 모두 같은 원리의 변주라는 게 보인다.
