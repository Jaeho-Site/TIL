---
title: new는 무슨 일을 하는가
description: 만들고, 잇고, 채우고, 돌려준다 — 인스턴스 생성 4단계와 instanceof의 동작 원리
---

# new는 무슨 일을 하는가

[this 글](/javascript/09-this-binding)에서 한 번, [지난 글](/javascript/11-prototype-chain)에서 또 한 번 미뤄둔 질문이다. 코드를 보면 이상한 점이 있다.

```javascript
function Circle(radius) {
  this.radius = radius;
}

const circle = new Circle(5);
console.log(circle); // Circle { radius: 5 }
```

`Circle` 본문 어디에도 **객체를 만드는 코드가 없고, return도 없다.** 프로퍼티를 채우는 코드뿐이다. 그런데 `new`와 함께 호출하면 완성된 인스턴스가 나온다. 누가 만들고, 누가 반환했을까?

## new가 뒤에서 하는 4단계

전부 `new`가 암묵적으로 대신한다. `new Circle(5)`가 실행되면 엔진은 이 순서로 움직인다.

1. **만들고** — 빈 객체를 하나 생성한다. 이게 인스턴스가 된다.
2. **잇고** — 그 객체의 `[[Prototype]]`을 `Circle.prototype`으로 연결한다. [지난 글](/javascript/11-prototype-chain)에서 "누가 연결했나" 했던 그 링크가 바로 이 단계에서 걸린다.
3. **채우고** — 그 객체를 this에 바인딩한 채 함수 본문을 실행한다. `this.radius = radius`는 새 객체에 프로퍼티를 채우는 초기화 코드였던 것이다.
4. **돌려준다** — 완성된 this를 암묵적으로 반환한다.

1단계 직후를 함수 안에서 직접 확인할 수 있다.

```javascript
function Circle(radius) {
  console.log(this); // Circle {} — 이미 만들어져서 this에 바인딩되어 있다

  this.radius = radius;
  // return이 없어도 this가 반환된다
}
```

그러니까 생성자 함수는 "객체를 만드는 함수"가 아니라 정확히는 **new가 만들어 준 객체를 초기화하는 함수**다. 생성은 new의 일, 초기화만 함수의 일이다. [this의 규칙 ③](/javascript/09-this-binding)에서 "this는 새로 만들어질 인스턴스"라고 했던 것도 3단계를 가리키는 말이었다.

한 가지 예외가 있다. 4단계에서 개발자가 **객체를** 명시적으로 return하면 this 대신 그 객체가 반환된다(원시 값을 return하면 무시되고 this가 반환된다). 생성자 안에서는 return을 쓰지 않는 게 기본인 이유다.

## new를 빼먹으면 어떻게 되나

[this 글](/javascript/09-this-binding)에서 본 사고를 이제 단계별로 설명할 수 있다.

```javascript
const circle3 = Circle(15); // new가 없다

console.log(circle3); // undefined
console.log(radius);  // 15 — 전역이 오염됐다
```

new가 없으면 4단계가 전부 사라진다. 만들어 주는 객체도, 프로토타입 연결도, 암묵적 반환도 없다. 그냥 일반 함수 호출이라 this는 전역 객체가 되고, `this.radius = 15`는 전역에 프로퍼티를 만든다. 반환값은 `undefined`. [strict mode였다면](/javascript/09-this-binding) this가 `undefined`라 여기서 TypeError로 즉시 잡혔을 것이다 — 조용한 전역 오염보다는 나은 결말이다.

이런 실수를 막고 싶으면 함수 안에서 `new.target`을 확인하면 된다. new와 함께 호출됐을 때만 값이 있는 메타 프로퍼티다.

```javascript
function Circle(radius) {
  if (!new.target) {
    return new Circle(radius); // new 없이 불렸으면 대신 new로 다시 호출
  }
  this.radius = radius;
}
```

다만 요즘은 이 방어 코드를 직접 쓸 일이 드물다. class가 언어 차원에서 new를 강제하기 때문인데, 그건 [다음 글](/javascript/13-class-sugar)에서 다룬다.

## instanceof는 무엇을 확인하나

new가 2단계에서 걸어준 링크는 나중에 "이 객체가 누구의 인스턴스인가"를 판별하는 근거가 된다.

```javascript
function Person(name) { this.name = name; }
const me = new Person('Lee');

console.log(me instanceof Person); // true
console.log(me instanceof Object); // true — 이건 왜?
```

`me instanceof Person`은 "me가 Person으로 만들어졌는가"를 기록해 둔 게 아니다. 확인하는 건 하나뿐이다 — **`Person.prototype`이 `me`의 프로토타입 체인 위에 존재하는가.** `me instanceof Object`도 true인 이유가 여기서 바로 나온다. 체인의 종점이 `Object.prototype`이니까, 모든 객체는 `Object`의 인스턴스로 판정된다.

"생성 기록이 아니라 현재 체인을 본다"는 건 실험으로 확인할 수 있다.

```javascript
Object.setPrototypeOf(me, {}); // 체인을 갈아끼우면

console.log(me instanceof Person); // false — Person으로 만들었지만 아니라고 나온다
console.log(me instanceof Object); // true
```

`me`는 분명 `new Person`으로 태어났지만, 체인에서 `Person.prototype`이 사라지자 instanceof는 false를 반환한다. 출생 증명서가 아니라 **지금의 족보**를 확인하는 연산자다.

---

new는 자바스크립트에서 4단계 대행이다. **만들고(빈 객체), 잇고(프로토타입 링크), 채우고(this로 초기화), 돌려준다(암묵적 반환).** instanceof는 그중 2단계에서 걸린 링크가 아직 체인에 있는지 확인할 뿐이다.

그런데 이 4단계를 이해하고 나면 생성자 함수의 불편함도 보인다. new를 빼먹어도 조용히 지나가고, 메서드는 prototype에 따로 달아야 하고, 이 모든 관례를 아는 사람만 안전하게 쓸 수 있다. ES6의 class가 이 불편을 어떻게 정리했는지, 그리고 "class는 문법 설탕일 뿐"이라는 말이 정확한지 다음 글에서 정리해보겠다. → [class는 문법 설탕인가](/javascript/13-class-sugar)
