---
title: 화살표 함수의 this는 왜 다른가
description: this를 스코프 체인에서 찾는 함수 — call/apply/bind, 콜백에서 깨지는 this까지
---

# 화살표 함수의 this는 왜 다른가

[지난 글](/javascript/09-this-binding)에서 this는 호출 방식이 결정한다고 정리했다. 그 규칙이 통하지 않는 함수가 있다는 걸 보여주는 문제부터 본다.

```javascript
window.x = 1;

const normal = function () { return this.x; };
const arrow = () => this.x;

console.log(normal.call({ x: 10 })); // ?
console.log(arrow.call({ x: 10 }));  // ?
```

`call`은 this를 강제로 지정하는, 우선순위가 가장 높은 규칙이었다. 그런데 결과는 `10`과 `1`이다. 일반 함수는 지정한 `{ x: 10 }`을 받았지만, **화살표 함수는 call을 무시하고 전역의 `x`를 읽었다.**

## 화살표 함수에는 this가 아예 없다

무시한 게 아니라, 정확히는 **받을 곳이 없다.** 화살표 함수는 자체 this 바인딩을 갖지 않는다. 그럼 화살표 함수 안의 `this`는 뭘까 — 엔진은 이걸 일반 식별자처럼 취급해서 **[스코프 체인](/javascript/06-scope-chain)을 따라 상위 스코프의 this를 찾아 쓴다.** 변수 `x`를 바깥 스코프에서 찾아오듯 this도 바깥에서 찾아오는 것이다. 그래서 "렉시컬 this"라고 부른다.

위 문제의 `arrow`는 전역에서 정의됐으니 상위 스코프는 전역이고, 전역의 this는 `window`다. `call`로 뭘 넘기든 자기 바인딩이 없으니 바꿀 대상 자체가 없다 — 인수는 정상적으로 전달되지만 this만은 항상 스코프를 따른다.

## 왜 이런 함수를 만들었을까: 콜백에서 깨지는 this

화살표 함수의 렉시컬 this는 ES6 이전 개발자들이 매일 겪던 고통에 대한 답이다. 지난 글의 규칙 ①(일반 호출 → 전역)이 콜백에서 어떤 사고를 치는지 보자.

```javascript
var value = 1;

const obj = {
  value: 100,
  foo() {
    setTimeout(function () {
      console.log(this.value); // 1 — 100이 아니다! (브라우저 기준, Node는 undefined)
    }, 100);
  }
};

obj.foo();
```

`obj.foo()`는 메서드 호출이라 `foo`의 this는 `obj`다. 하지만 setTimeout에 넘긴 콜백은 나중에 **타이머가 일반 함수로 호출**한다. 내 코드 문맥과 무관하게 규칙 ①이 적용되어 this는 전역이 된다. "메서드 안에 썼으니 당연히 obj겠지"라는 직관이 배신당하는 지점이다.

ES6 이전에는 두 가지 우회로를 썼다.

```javascript
// 우회 1: this를 변수에 담아 클로저로 전달
foo() {
  const that = this;
  setTimeout(function () {
    console.log(that.value); // 100
  }, 100);
}

// 우회 2: bind로 this를 고정한 함수를 만들어 전달
foo() {
  setTimeout(function () {
    console.log(this.value); // 100
  }.bind(this), 100);
}
```

우회 1이 재미있다. this는 스코프 체인을 타지 않지만 **변수 `that`은 탄다.** this를 변수에 옮겨 담는 순간 [클로저](/javascript/07-closure)로 전달할 수 있게 된다. 화살표 함수는 바로 이 패턴을 언어 차원에서 내장한 것이다.

```javascript
foo() {
  setTimeout(() => console.log(this.value), 100); // 100
}
```

화살표 함수 안의 this는 상위 스코프인 `foo`의 this를 그대로 본다. `() => this.x`는 사실상 `function () { return this.x; }.bind(this)`의 축약인 셈이다.

## call / apply / bind는 그럼 언제 쓰나

지난 글에서 미뤄둔 명시적 바인딩 3형제를 여기서 정리한다. 셋 다 this를 지정하지만 동작이 다르다.

```javascript
function getThisBinding() {
  return this;
}

const thisArg = { a: 1 };

getThisBinding.call(thisArg, 1, 2, 3);    // 즉시 호출, 인수는 쉼표로
getThisBinding.apply(thisArg, [1, 2, 3]); // 즉시 호출, 인수는 배열로
const bound = getThisBinding.bind(thisArg); // 호출하지 않고, this가 고정된 새 함수를 반환
bound(); // { a: 1 }
```

- **call과 apply**는 인수 전달 방식만 다를 뿐 같다 — this를 바꿔서 **지금 즉시 호출**한다.
- **bind**는 호출하지 않는다. this가 영구히 고정된 **새 함수를 만들어 반환**한다.

용도가 갈리는 지점도 여기다. call/apply는 그 자리에서 한 번 빌려 쓸 때, bind는 **나중에 남이 호출할 함수**(콜백)의 this를 미리 고정해 둘 때 쓴다. 위의 setTimeout 우회 2가 정확히 그 용례다.

## 그렇다고 아무 데나 화살표 함수를 쓰면 안 된다

"this 문제는 화살표 함수로 해결"이라고만 외우면 반대 방향 사고가 난다. 메서드를 화살표 함수로 정의해 보자.

```javascript
const counter = {
  num: 1,
  increase: () => ++this.num
};

console.log(counter.increase()); // NaN
```

`increase`의 상위 스코프는 `counter` 객체가 아니라 **전역**이다(객체 리터럴은 스코프를 만들지 않는다 — 스코프를 만드는 건 함수와 블록이다). this는 `window`고 `window.num`은 `undefined`, `++undefined`는 `NaN`. **호출한 객체를 this로 받아야 하는 메서드는 일반(축약) 메서드로, 상위 문맥의 this를 이어받아야 하는 콜백은 화살표 함수로** — 이게 선택 기준이다.

## React가 bind를 강요하던 이유

클래스 컴포넌트 시절 React 코드에는 이런 보일러플레이트가 반드시 있었다.

```jsx
class Toggle extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this); // 왜 이걸 매번?
  }

  handleClick() {
    this.setState(/* ... */);
  }

  render() {
    return <button onClick={this.handleClick}>toggle</button>;
  }
}
```

이제 이유를 전부 설명할 수 있다. `onClick={this.handleClick}`은 메서드를 **떼어내서** 넘기는 것이다 — 도입 문제에서 `const getName = person.getName`을 한 것과 같다. React가 나중에 이 함수를 호출할 때 인스턴스와의 연결은 이미 사라졌고, 클래스 내부는 항상 strict mode라 this는 `undefined`가 된다. `this.setState`에서 터진다. 그래서 bind로 미리 고정하거나, 클래스 필드에 화살표 함수(`handleClick = () => {...}`)를 써서 렉시컬 this로 인스턴스를 잡아두는 관례가 생겼다.

함수 컴포넌트와 훅으로 넘어오면서 이 고통이 통째로 사라졌는데, 방법이 흥미롭다. this를 다루기 쉽게 만든 게 아니라 **this를 아예 쓰지 않는 구조**로 바꿨다. 상태는 [클로저가 가둬서 기억한다](/javascript/08-closure-in-practice). this의 가장 큰 실전 무대가 사라진 셈이지만, 여전히 클래스·이벤트 핸들러·라이브러리 코드 곳곳에서 this는 살아 있다.

---

**일반 함수의 this는 호출이 결정하고, 화살표 함수의 this는 스코프가 결정한다.** 화살표 함수는 this를 클로저의 세계로 데려온 함수다 — 그래서 규칙이 아니라 방향 자체가 다르다.

남은 궁금증은 지난 글에서 미뤄둔 규칙 ③이다. `new`와 함께 호출하면 this가 "새로 만들어질 인스턴스"라고 했는데, 그 인스턴스는 누가 언제 만들고, 어떻게 메서드를 물려받는 걸까? 다음 그룹에서 프로토타입으로 들어간다. → [자바스크립트의 상속은 어떻게 동작하는가](/javascript/11-prototype-chain)
