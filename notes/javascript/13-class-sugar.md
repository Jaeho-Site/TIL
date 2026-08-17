---
title: class는 문법 설탕인가
description: 거의 맞지만 셋이 다르다 — new 강제, TDZ, strict mode. 그리고 getter/setter
---

# class는 문법 설탕인가

ES6 이전의 자바스크립트 개발자는 [프로토타입](/javascript/11-prototype-chain)과 [new의 4단계](/javascript/12-new-and-constructor)를 전부 알아야 "클래스 같은 것"을 만들 수 있었다. [클로저 은닉](/javascript/08-closure-in-practice)에서 본 IIFE 패턴까지 동원하면 이런 모양이 된다.

```javascript
var Person = (function () {
  function Person(name) {
    this.name = name;
  }

  Person.prototype.sayHi = function () {
    console.log('Hi! My name is ' + this.name);
  };

  return Person;
}());
```

ES6 class로 쓰면 이렇다.

```javascript
class Person {
  constructor(name) {
    this.name = name;
  }

  sayHi() {
    console.log(`Hi! My name is ${this.name}`);
  }
}

const me = new Person('Lee');
me.sayHi(); // Hi! My name is Lee
```

그래서 "class는 프로토타입의 문법 설탕(syntactic sugar)일 뿐"이라는 말을 정말 많이 듣는다. 새로운 게 아니라 기존 것의 포장이라는 뜻인데 — 어디까지 맞는 말일까?

## 설탕이 맞긴 하다

뼈대는 프로토타입으로 진짜로 같다. 확인해 보면:

```javascript
class Person {
  constructor(name) { this.name = name; }
  sayHi() { console.log('Hi!'); }
}

console.log(typeof Person); // "function" — 클래스도 함수다
console.log(Person === Person.prototype.constructor); // true

const me = new Person('Lee');
console.log(Object.getPrototypeOf(me) === Person.prototype); // true
```

class는 특별한 새 타입이 아니라 **함수**고, class 몸체에 쓴 메서드는 `Person.prototype`에 올라가며, 인스턴스는 [프로토타입 체인](/javascript/11-prototype-chain)으로 메서드를 찾아 쓴다. `me.sayHi()`의 검색 경로는 생성자 함수 버전과 완전히 동일하다. 상속(`extends`)도 마찬가지로 새 메커니즘이 아니다 — 부모 클래스의 prototype을 자식 클래스 prototype의 프로토타입으로 연결해서, **체인을 한 층 더 쌓는 것**이다.

## 그런데 세 부분이 다르다

포장만 바꾼 게 아니다. class는 생성자 함수가 조용히 허용하던 실수들을 **에러로 바꿨다.** 지금까지의 글들에서 본 사고들이 하나씩 막혀 있는 게 보인다.

**첫째, new 없이 호출하면 에러다.** [지난 글](/javascript/12-new-and-constructor)에서 생성자 함수는 new를 빼먹으면 조용히 전역을 오염시켰다. class는 호출 자체를 거부한다.

```javascript
const me = Person('Lee');
// TypeError: Class constructor Person cannot be invoked without 'new'
```

**둘째, 호이스팅이 let/const처럼 동작한다.** 함수 선언문은 [통째로 호이스팅](/javascript/04-hoisting)되어 선언 전에 호출할 수 있었다. class는 선언되지만 [TDZ](/javascript/05-var-let-const)에 걸린다.

```javascript
console.log(Person); // ReferenceError: Cannot access 'Person' before initialization

class Person {}
```

**셋째, 내부가 항상 strict mode다.** [화살표 함수 글](/javascript/10-arrow-function-this)에서 클래스 메서드를 떼어내 호출하면 this가 `window`가 아니라 `undefined`였던 이유가 이것이다. 그 밖에도 class의 메서드는 열거되지 않고(`for...in`에 안 잡힌다), `new`로 호출할 수 없는 non-constructor다.

공통점이 보인다. 전부 **느슨함을 없애는 방향**이다. 그래서 나는 "class는 문법 설탕인가"라는 질문에 이렇게 답하게 됐다 — 동작 원리는 프로토타입 그대로라서 설탕이 맞지만, 단순한 설탕이라기엔 **더 엄격하다.** var를 고친 let/const가 그랬듯, class는 생성자 함수의 함정들을 고친 버전이다.

## 덤: 메서드인데 프로퍼티처럼 읽는다 — getter와 setter

class 문법에서 자주 만나는 요소 하나만 더 정리한다. `get`/`set` 키워드다.

```javascript
class Person {
  constructor(firstName, lastName) {
    this.firstName = firstName;
    this.lastName = lastName;
  }

  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  }

  set fullName(name) {
    [this.firstName, this.lastName] = name.split(' ');
  }
}

const me = new Person('Jaeho', 'Lee');

console.log(me.fullName); // "Jaeho Lee" — 호출 괄호가 없는데 함수가 실행됐다
me.fullName = 'Gildong Hong'; // 할당인데 함수가 실행됐다
console.log(me.firstName); // "Gildong"
```

`fullName`은 함수로 정의했지만 값을 저장하지 않는다. **읽는 행위와 쓰는 행위 뒤에 함수를 숨긴 프로퍼티**로, 이런 프로퍼티를 접근자 프로퍼티(accessor property)라고 부른다(값을 직접 가진 일반 프로퍼티는 데이터 프로퍼티다). 파생 값을 프로퍼티처럼 노출하거나, 할당 시점에 검증 로직을 끼워 넣을 때 쓴다.

은닉이 필요하면 [클로저 글](/javascript/08-closure-in-practice)에서 언급한 `#private` 필드(ES2022)를 조합한다. `#age`는 클래스 밖에서 접근하면 문법 에러라서, IIFE+클로저로 은닉을 흉내 내던 시절의 정식 해법이 됐다.

---

class는 프로토타입을 대체한 게 아니라 **프로토타입 위에 안전장치를 얹은 포장**이다. 설탕은 맞다. 다만 원료를 모르면 `typeof Person`이 왜 `"function"`인지, 메서드가 어디에 저장되는지, instanceof가 왜 그렇게 판정하는지 아무것도 설명할 수 없다.

여기까지로 객체를 만들고 잇는 이야기는 일단락이다. 다음 궁금증은 더 아래층에 있다 — new가 만들어 주는 "객체"라는 값 자체는 원시 값과 뭐가 다른가. `const`로 선언한 객체가 수정되는 이유, 복사가 두 종류인 이유가 전부 거기서 나온다. → [원시 타입과 객체는 뭐가 다른가](/javascript/01-primitive-vs-object)
