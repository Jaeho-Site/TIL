---
title: 함수가 일급 객체라는 게 무슨 의미인가
description: 함수를 값처럼 다룰 수 있다 — 콜백, 고차 함수, 그리고 제어권의 이동
---

# 함수가 일급 객체라는 게 무슨 의미인가

모든 언어가 그렇겠지만 자바스크립트에서 객체가 갖는 의미는 중요하다. 함수를 배열 메서드에 넘기고, 함수가 함수를 만들어 돌려주고
자바스크립트에서 이게 되는 이유를 한 문장으로 **함수는 일급 객체**라고 한다.

일급 객체의 조건은 "값과 동일하게 취급된다"는 것이고, 구체적으로 네 가지다.

```javascript
// 1. 이름 없는 리터럴로 만들 수 있고, 2. 변수나 자료구조에 담을 수 있다
const increase = function (num) { return ++num; };
const decrease = function (num) { return --num; };
const auxs = { increase, decrease }; // 객체에도 담긴다

// 3. 함수의 인자로 전달할 수 있고, 4. 함수의 반환값이 될 수 있다
function makeCounter(aux) {
  let num = 0;
  return function () {
    num = aux(num);
    return num;
  };
}

const increaser = makeCounter(auxs.increase);
console.log(increaser()); // 1
console.log(increaser()); // 2
```

낯익은 코드다 — [클로저 활용 글](/javascript/08-closure-in-practice)의 카운터가 정확히 이 구조였다. 클로저라는 기능 자체가 "함수를 반환값으로 쓸 수 있다"(4번)는 전제 위에 서 있는 셈이다.

## 함수는 진짜로 객체다

"객체처럼 취급된다"는 비유가 아니다. 함수는 [프로토타입 글](/javascript/11-prototype-chain)에서 본 객체의 조건을 전부 갖췄고, 심지어 자기만의 프로퍼티도 있다.

```javascript
function square(number) {
  return number * number;
}

console.log(square.length); // 1 — 매개변수 개수
console.log(square.name);   // "square"
console.log(square.hasOwnProperty('prototype')); // true — 함수만 가진 프로퍼티
```

일반 객체와의 차이는 딱 하나, **호출할 수 있다**는 것이다(내부적으로 `[[Call]]`이라는 내부 메서드를 가진 객체가 함수다). 그러니 "일급 객체"의 실체는 함수는 호출 가능한 객체이고, 객체는 값이므로, **함수도 값이다.** 라는 것이다.

참고 : 위 예제에서 모든 함수는 prototype 프로퍼티를 갖고있다 처럼 말하고 있지만 화살표함수는 예외이다. 엄밀히 말하면 생성자로 사용할 수 있는 함수에 주로 존재하며 [[Construct]]와 관련되어 있다.

## 값이라서 가능한 것: 로직을 값처럼 주고받기

이 성질이 코드 스타일을 어떻게 바꾸는지가 진짜 내용이다. 반복 로직을 예로 들면:

```javascript
function repeat1(n) { // n번 반복하며 전부 출력
  for (var i = 0; i < n; i++) console.log(i);
}

function repeat2(n) { // n번 반복하며 홀수만 출력
  for (var i = 0; i < n; i++) {
    if (i % 2) console.log(i);
  }
}
```

반복이라는 공통 로직과 "각 회차에 무엇을 할 것인가"라는 변하는 로직이 한 덩어리라서, 할 일이 바뀔 때마다 함수를 통째로 새로 써야 한다. 함수가 값이라면 **변하는 부분만 값으로 받으면 된다.**

```javascript
function repeat(n, f) { // 공통 로직만 남기고
  for (var i = 0; i < n; i++) f(i); // 변하는 로직은 넘겨받는다
}

repeat(5, i => console.log(i));           // 0 1 2 3 4
repeat(5, i => { if (i % 2) console.log(i); }); // 1 3
```

이때 넘겨지는 함수가 **콜백 함수**, 콜백을 받거나 함수를 반환하는 함수가 **고차 함수**(higher-order function)다. 배열의 `map`·`filter`·`reduce`가 전부 이 패턴이고 — `map`은 "순회하며 변환한다"는 공통 로직에 "어떻게 변환할지"만 콜백으로 받는 고차 함수다 — [디바운스](/javascript/08-closure-in-practice)도, [Promise.then](/javascript/18-promise)도, 이벤트 핸들러 등록도 전부 함수를 값으로 넘기는 행위였다.

주의할 점도 그대로 따라온다. 콜백을 넘긴다는 건 **내 로직의 실행 시점과 횟수를 상대에게 맡긴다**는 뜻이다 — [프로미스 글](/javascript/18-promise)에서 콜백 방식의 문제로 꼽았던 제어권 역전이 바로 이것이고, 고차 함수를 쓴다는 건 그 제어권 거래를 하는 것이다.

## 덤: arguments, 그리고 rest 파라미터

함수가 객체라는 사실의 흔적 하나를 더 정리해 둔다. 모든 일반 함수 안에서는 `arguments`라는 객체를 쓸 수 있다 — 전달된 인수 전부를 담은, 배열 흉내를 내는 **유사 배열 객체**다.

```javascript
function sum() {
  let res = 0;
  for (let i = 0; i < arguments.length; i++) res += arguments[i]; // 순회는 되지만
  return res;
}
// arguments에는 map, reduce 같은 배열 메서드가 없다 — 배열이 "아니라서"

// ES6 rest 파라미터: 진짜 배열로 받는다
function sum2(...args) {
  return args.reduce((pre, cur) => pre + cur, 0);
}
console.log(sum2(1, 2, 3, 4, 5)); // 15
```

ES6 이후로는 rest 파라미터가 정답이라 `arguments`를 직접 쓸 일은 드물지만, "배열처럼 생겼는데 배열이 아닌 것"이 존재한다는 사실은 기억해 둘 만하다 — 유사 배열과 이터러블의 정확한 차이는 [이터러블 글](/javascript/21-iterable)에서 다룬다.

---

함수형 프로그래밍이니 고차 함수니 하는 말들이 거창하게 들렸는데, 정리하고 나니 전부 한 문장의 결과였다. **함수가 값이므로, 로직을 데이터처럼 주고받을 수 있다.**

그런데 함수가 값이라면, 모든 함수는 같은 종류의 값일까? 사실 ES6부터 함수는 세 종류로 갈라졌고, 똑같이 생긴 두 메서드 중 하나만 `new`가 되는 이유가 거기 있다. → [화살표 함수와 일반 함수는 뭐가 다른가](/javascript/15-arrow-vs-normal)
