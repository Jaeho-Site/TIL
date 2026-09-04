---
title: 같은 이름이 타입도 되고 값도 된다
description: 타입 공간과 값 공간 — typeof의 두 얼굴, class와 enum이 특별한 이유
---

# 같은 이름이 타입도 되고 값도 된다

[지난 글](/typescript/05-types-as-sets)을 정리하면서 계속 "타입의 세계"와 "값의 세계"라는 말을 썼는데, 이 경계를 정면으로 시험하는 코드를 책에서 만났다.

```typescript
interface Cylinder {
  radius: number;
  height: number;
}

const Cylinder = (radius: number, height: number) => ({ radius, height });

function calculateVolume(shape: unknown) {
  if (shape instanceof Cylinder) {
    shape.radius;
    //    ~~~~~~ Property 'radius' does not exist on type '{}'
  }
}
```

우선 `interface Cylinder`와 `const Cylinder`가 같은 파일에 공존하는 것부터 놀랍다. 이름 충돌 에러가 안 난다. 그리고 `instanceof Cylinder` 검사는 통과시켜 놓고, 정작 블록 안에서 `shape.radius`를 막는다. 에러 메시지의 `'{}'`는 또 뭘까.

## 두 개의 공간, 두 개의 명부

타입스크립트의 심벌은 **타입 공간**과 **값 공간** 중 한 곳에, 또는 양쪽 모두에 산다. 두 공간은 명부가 따로라서 같은 이름이 각각 등록될 수 있다. 위 코드에서 `Cylinder`는 타입 공간에는 인터페이스로, 값 공간에는 화살표 함수로 등록돼 있다.

그럼 `shape instanceof Cylinder`의 `Cylinder`는 어느 쪽일까? [두 번째 글](/typescript/02-runtime-types)에서 본 대로 `instanceof`는 런타임 연산자다. 런타임은 값의 세계이므로, 여기서 `Cylinder`는 **화살표 함수**를 가리킨다. 인터페이스로 좁혀지길 기대했지만 실제로는 "이 값이 저 화살표 함수의 인스턴스인가"라는, 의도와 전혀 다른 검사를 한 것이다. 타입 체커는 그 함수의 인스턴스 타입을 `{}`로 추론했고, 그래서 `radius`가 없다고 한 것이다. 에러는 정확했다 — 내 코드가 두 공간을 헷갈렸을 뿐이다.

어떤 이름이 어느 공간에 있는지 구분하는 감각은 자리에서 나온다. `type`과 `interface` 선언 뒤, 콜론(`:`) 뒤, `as` 뒤의 이름은 타입 공간이다. `const`·`let` 선언 뒤, `=` 뒤의 이름은 값 공간이다.

```typescript
const jane: Person = { first: 'Jane', last: 'Jacobs' };
//    ――――  ↑타입    ――――――――――――――――――――――――――――――― 값
```

## typeof의 두 얼굴

이 구분이 제일 실감 나는 게 `typeof` 연산자다. 같은 키워드가 **어느 공간에서 평가되느냐에 따라 완전히 다른 일**을 한다.

```typescript
type T1 = typeof jane; // 타입 공간: Person — 정적 타입을 가져온다
const v1 = typeof jane; // 값 공간: "object" — JS의 typeof, 8가지 문자열 중 하나
```

타입 공간의 `typeof`는 타입스크립트가 추론해둔 정적 타입을 꺼내오고, 값 공간의 `typeof`는 우리가 아는 자바스크립트 런타임 연산자 그대로다. 사실 처음 `type T = typeof someObject`를 봤을 때 `T`가 `"object"`인 줄 알았다. 같은 글자가 층에 따라 다른 언어라는 걸 받아들여야 이 코드가 읽힌다.
