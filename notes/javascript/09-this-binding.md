---
title: this는 언제 결정되는가
description: 함수가 소속된 곳이 아니라 호출한 방식이 this를 결정한다 — 바인딩 4가지 규칙
---

# this는 언제 결정되는가

[지난 글](/javascript/08-closure-in-practice) 끝에서 던진 질문을 이어받는다. 스코프도 클로저도 전부 함수가 **정의될 때** 정해졌는데, this도 그럴까? 아래 예제를 보자.

```javascript
const person = {
  name: 'Lee',
  getName() {
    return this.name;
  }
};

console.log(person.getName()); // ?

const getName = person.getName;
console.log(getName()); // ?
```

첫 번째는 예상대로 `'Lee'`다. 문제는 두 번째다. 같은 함수를 변수에 담아 호출했을 뿐인데 `'Lee'`가 아니라 `''`(브라우저 기준, Node.js에서는 `undefined`)가 나온다. 함수는 그대로인데 결과가 달라졌다.

## this가 "자기가 속한 객체"라는 이해가 함정이다

나도 처음엔 this를 "메서드가 소속된 객체"라고 이해했다. 그 이해로는 위 문제를 설명할 수 없다. `getName`은 여전히 `person` 안에서 정의된 그 함수인데, 왜 this가 달라졌을까?

답은 방향을 뒤집어야 보인다. **this는 함수가 정의될 때 정해지는 게 아니라, 호출될 때 정해진다.** 함수 객체는 어디에도 소속되지 않는다. `person.getName`은 그저 프로퍼티가 함수 객체를 가리키고 있을 뿐이고, this는 그 함수를 **어떤 방식으로 호출했느냐**에 따라 매번 새로 바인딩된다.

극단적인 예로, 하나의 함수를 네 가지 방식으로 호출하면 this가 네 번 다 달라진다.

```javascript
const foo = function () {
  console.dir(this);
};

foo();                       // ① 일반 함수 호출 → window
const obj = { foo };
obj.foo();                   // ② 메서드 호출 → obj
new foo();                   // ③ 생성자 호출 → 새로 생성된 인스턴스
foo.call({ name: 'bar' });   // ④ 간접 호출 → { name: 'bar' }
```

이 네 가지가 this 바인딩 규칙의 전부다. 하나씩 이유를 보자.

## ① 일반 함수 호출 — 전역 객체

아무 객체 없이 `foo()`처럼 호출하면 this는 전역 객체(브라우저에선 `window`)다. 중요한 건 **어디에 정의됐는지는 전혀 상관없다**는 것이다. 메서드 안에 정의한 중첩 함수든, 콜백 함수든, 호출이 일반 호출이면 this는 전역이다.

```javascript
var value = 1;

const obj = {
  value: 100,
  foo() {
    console.log(this.value); // 100 — 메서드 호출

    function bar() {
      console.log(this.value); // 1 — 일반 호출이라 window.value
    }
    bar(); // obj.foo 안에서 호출했지만, 형태는 일반 호출이다
  }
};

obj.foo();
```

`bar`는 메서드 안에 살고 있지만 `bar()`는 앞에 아무 객체도 없는 일반 호출이므로 this는 `window`다. 그래서 `window.value`인 1이 나온다([var 전역 변수가 window 프로퍼티가 되는 이유](/javascript/05-var-let-const)까지 겹친 예제다).

사실 "헬퍼 함수의 this가 전역을 가리키는 게 무슨 의미가 있나" 싶은데, 스펙 설계자들도 같은 생각이었는지 strict mode에서는 일반 호출의 this가 `undefined`다. 전역 객체 바인딩은 의미도 없고 실수만 부르기 때문에 제거한 것이다. 뒤에서 볼 클래스 내부가 항상 strict mode인 것도 이 맥락이다.

## ② 메서드 호출 — 마침표 앞의 객체

`obj.foo()`처럼 호출하면 this는 **마침표 앞의 객체**다. 규칙이 이렇게 단순하기 때문에, 같은 함수라도 어떤 객체를 통해 호출하느냐에 따라 this가 바뀐다.

```javascript
const person = { name: 'Lee', getName() { return this.name; }};
const anotherPerson = { name: 'Kim' };
anotherPerson.getName = person.getName; // 같은 함수 객체를 가리키게 한다

console.log(person.getName());        // Lee — 마침표 앞이 person
console.log(anotherPerson.getName()); // Kim — 마침표 앞이 anotherPerson

const getName = person.getName;
console.log(getName());               // '' — 마침표가 없다, 일반 호출
```

도입 문제의 답이 여기 있다. `const getName = person.getName`으로 함수를 떼어내는 순간 `person`과의 연결은 사라진다. 변수가 가리키는 건 함수 객체 자체이지 "person의 메서드"가 아니기 때문이다. 그다음 `getName()`은 마침표 없는 일반 호출이라 규칙 ①이 적용되고, this는 `window`, `this.name`은 `window.name`(기본값 `''`)이 된다.

## ③ new와 함께 호출 — 새로 만들어질 인스턴스

```javascript
function Circle(radius) {
  this.radius = radius;
}

const circle = new Circle(5);
console.log(circle.radius); // 5
```

`new`와 함께 호출하면 this는 지금 만들어지고 있는 새 인스턴스를 가리킨다. 뒤집어 말하면, `new`를 빼먹는 순간 규칙 ①로 굴러떨어진다.

```javascript
const circle3 = Circle(15); // new를 빼먹었다 — 그냥 일반 호출

console.log(circle3); // undefined — 반환문이 없으니
console.log(radius);  // 15 — this가 window라서 전역에 radius가 생겼다!
```

에러도 없이 전역이 오염된다. `new`가 정확히 무슨 일을 하길래 this가 새 객체로 바뀌는지는 프로토타입 글에서 파헤칠 예정이다.

## ④ call / apply / bind — 내가 지정한 객체

마지막 규칙은 예외 조항이다. `foo.call(thisArg)`처럼 호출하면 일반 호출·메서드 호출 규칙을 무시하고 **첫 번째 인수로 넘긴 객체**가 this가 된다. this를 개발자가 직접 지정하는건데, 셋의 차이와 실전 쓰임은 분량이 있어서 [다음 글](/javascript/10-arrow-function-this)에서 화살표 함수와 함께 다루면 좋을것 같다.

정리하면 이렇다. 규칙끼리 겹치면 **③ new가 가장 세고, 그다음이 ④ 간접 호출**이다(③ > ④ > ② > ①). bind로 this를 고정해 둔 함수라도 `new`로 호출하면 bind가 지정한 객체는 무시되고 새 인스턴스가 this가 된다.

| 호출 방식 | this |
|---|---|
| ① 일반 함수 호출 `foo()` | 전역 객체 (strict mode: `undefined`) |
| ② 메서드 호출 `obj.foo()` | 마침표 앞의 객체 `obj` |
| ③ 생성자 호출 `new foo()` | 새로 생성될 인스턴스 |
| ④ 간접 호출 `foo.call(x)` | 지정한 객체 `x` |

## 왜 이렇게 설계했을까?

호출할 때마다 바뀌는 this는 처음엔 불합리해 보였다. 그런데 "하나의 함수를 여러 객체가 공유한다"는 관점에서 보면 이게 핵심 기능이다. 위에서 `person.getName`을 `anotherPerson`이 그대로 재사용할 수 있었던 건 this가 호출 시점에 결정되기 때문이다. 자바스크립트의 프로토타입 상속은 수천 개의 인스턴스가 메서드 하나를 공유하는 구조인데, this가 정의 시점에 굳어 있다면 이 공유는 불가능하다.

---

**this는 함수가 소속된 곳이 아니라, 호출한 방식이 결정한다.** 정의 시점에 굳는 스코프·클로저와 정확히 반대 방향이다 — 그래서 "스코프는 정의가, this는 호출이"라고 대구로 기억하면 안 잊는다.

그런데 이걸 무시하는 함수가 하나 있다. 화살표 함수는 위의 네 규칙을 전부 무시하고, this마저 스코프처럼 정의 위치에서 가져온다. call로 지정해도 안 바뀐다. 왜 그런 함수를 만들었는지는 다음 포스팅에서 다루도록 하겠다. [화살표 함수의 this는 왜 다른가](/javascript/10-arrow-function-this)
