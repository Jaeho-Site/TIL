---
title: 화살표 함수와 일반 함수는 뭐가 다른가
description: ES6가 함수를 세 종류로 나눈 이유 — this, arguments, super, new.target의 부재
---

# 화살표 함수와 일반 함수는 뭐가 다른가

거의 똑같아 보이는 아래 두 메서드를 보자.

```javascript
const obj = {
  x: 10,
  foo() { return this.x; },              // 축약 메서드
  bar: function () { return this.x; }    // 프로퍼티에 함수 할당
};

console.log(obj.foo()); // 10
console.log(obj.bar()); // 10 — 호출 결과는 같다. 그런데,

new obj.foo(); // ?
new obj.bar(); // ?
```

`new obj.bar()`는 멀쩡히 `bar {}`를 만들어내는데, `new obj.foo()`는 **`TypeError: obj.foo is not a constructor`**다. 똑같이 동작하던 두 함수가 new 앞에서 갈라진다. 함수라고 다 같은 함수가 아니었던 것이다.

## ES6는 함수를 세 종류로 나눴다

ES6 이전의 함수는 만능이었다. 모든 함수가 호출도 되고(`callable`), `new`로 인스턴스도 만들 수 있었다(`constructor`).

```javascript
var foo = function () {};

foo();     // 일반 호출 — 된다
new foo(); // 생성자 호출 — 이것도 된다
```

편해 보이지만 비용이 있었다. 콜백으로 쓸 함수도, 메서드로 쓸 함수도 생성자가 "될 수 있는" 함수라서, 쓰지도 않을 `prototype` 객체를 전부 달고 다녔고, `new obj.bar()`처럼 의도가 있을 리 없는 호출도 조용히 성공했다. 그래서 ES6는 함수를 **목적별로** 나눴다.

- **일반 함수** — 예전 그대로. constructor라서 new가 되고 `prototype`을 가진다.
- **메서드**(축약 표현으로 정의한 것만) — non-constructor. new 불가, `prototype` 없음. 대신 `super`를 쓸 수 있다.
- **화살표 함수** — non-constructor에 더해, 자기만의 this조차 없다.

도입 문제의 답이 이것이다. `foo()`는 축약 표현으로 정의된 진짜 "메서드"라 non-constructor이고, `bar`는 프로퍼티에 일반 함수를 할당한 것이라 constructor다. 겉모양이 아니라 **정의 방식**이 함수의 종류를 정한다. 참고로 빌트인 메서드들도 전부 non-constructor다 — `[].map.prototype`을 확인해 보면 `undefined`가 나온다.

## 화살표 함수에 없는 것 4가지

이 관점에서 화살표 함수를 다시 보면, "짧은 함수"가 아니라 **가장 많이 덜어낸 함수**다. 자기 것이 없는 게 넷이다: **this, arguments, super, new.target.** 넷 다 규칙은 하나 — 자기 것이 없으니 [스코프 체인을 따라 상위 스코프의 것](/javascript/06-scope-chain)을 쓴다.

**① this가 없다.** 넷 중 제일 중요해서 [별도 글](/javascript/10-arrow-function-this)로 이미 다뤘다. 호출 방식과 무관하게 상위 스코프의 this를 쓰고, call/apply/bind로도 바꿀 수 없다.

**② constructor가 아니다.** new가 안 되고, `prototype` 프로퍼티도 없다.

```javascript
const Foo = () => {};

new Foo(); // TypeError: Foo is not a constructor
console.log(Foo.hasOwnProperty('prototype')); // false
```

[new의 4단계](/javascript/12-new-and-constructor)를 떠올리면 당연한 결과다 — 2단계에서 인스턴스와 이어줄 `prototype`도 없고, 3단계에서 바인딩할 자기 this도 없다. 생성자가 되기 위한 부품 자체가 없는 것이다.

**③ arguments가 없다.** [지난 글](/javascript/14-first-class-function)에서 본 그 유사 배열 객체가 화살표 함수 안에는 만들어지지 않는다. 참조하면 상위 스코프의 arguments가 잡힌다. 가변 인자가 필요하면 rest 파라미터를 쓰라는 뜻이다.

```javascript
const sum = (...args) => args.reduce((pre, cur) => pre + cur, 0);
```

**④ super와 new.target도 없다.** 마찬가지로 상위 스코프의 것을 참조한다.

정리하면 화살표 함수는 함수에서 **객체 생성 능력과 자기 컨텍스트를 전부 뺀, 순수한 "동작"만 남긴 함수**다. 콜백이 원하는 게 정확히 그것이라서 콜백의 기본형이 됐다.

## 그래서 언제 뭘 쓰나

세 종류의 용도는 아래와 같다.

```javascript
const counter = {
  count: 0,
  increase() {                    // 메서드 → 축약 표현
    this.timer = setTimeout(() => {  // 콜백 → 화살표 (상위 this를 이어받는다)
      this.count += 1;
    }, 100);
  }
};
```

- **메서드는 축약 표현으로.** this가 호출한 객체에 바인딩되고, 실수로 new 하는 것도 막아준다. [화살표 함수로 메서드를 정의하면 this가 전역을 보는 사고](/javascript/10-arrow-function-this)는 이미 봤다.
- **콜백은 화살표 함수로.** 감싸는 문맥의 this를 그대로 쓰는 게 콜백에서 원하는 동작이다.
- **생성자가 필요하면 class로.** [class 글](/javascript/13-class-sugar)에서 봤듯, new를 강제까지 해준다.

---

ES6의 함수 삼분법?은 결국 **함수의 만능을 회수하고, 각자 목적에 필요한 것만 남긴 것**이다. 화살표 함수가 일반 함수의 축약이 아니라는 것 — 없는 네 가지(this·arguments·super·new.target)와 그래서 생성자가 될 수 없다는 것까지 답할 수 있으면 이 주제는 끝난다.

이것으로 함수 이야기도 회고했다. 남은 의문은 이전에본 "배열처럼 생겼는데 배열이 아닌 것"이다. for...of는 되는데 왜 배열 메서드는 안 될까? 순회 가능하다는 것의 정확한 조건, 이터러블 프로토콜로 이야기해보겠다. → [for...of와 for...in은 뭐가 다른가](/javascript/21-iterable)
