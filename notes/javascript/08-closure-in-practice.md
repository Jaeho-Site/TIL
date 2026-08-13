---
title: 클로저는 어디에 쓰는가
description: 상태 은닉, 디바운스, var 반복문, 그리고 React의 stale closure까지
---

# 클로저는 어디에 쓰는가

[지난 글](/javascript/07-closure)에서 클로저가 어떻게 가능한지는 이해했다. 남은 궁금증은 "그래서 이걸 어디에 쓰나"였는데, 정리해 보니 답은 하나로 모인다. **상태를 함수 안에 가두고 싶을 때** 쓴다.

간단한 요구사항으로 시작해 본다. 호출할 때마다 1씩 증가하는 카운터를 만들자.

```javascript
let num = 0;

const increase = function () {
  return ++num;
};

console.log(increase()); // 1
console.log(increase()); // 2
```

동작은 한다. 그런데 `num`이 전역에 노출되어 있다. 누구든 `num = 100`을 대입하면 카운터가 망가진다. 카운터의 상태는 `increase`만 바꿀 수 있어야 맞다. 그래서 `num`을 함수 안으로 넣으면?

```javascript
const increase = function () {
  let num = 0;
  return ++num;
};

console.log(increase()); // 1
console.log(increase()); // 1 — 호출마다 0으로 리셋된다
```

이번엔 상태가 유지되지 않는다. 딜레마다. **상태는 호출 사이에 유지돼야 하고, 동시에 외부에서는 건드릴 수 없어야 한다.** 이 두 요구를 동시에 만족시키는 도구가 클로저다.

```javascript
const increase = (function () {
  let num = 0; // 자유 변수 — 외부에서 접근할 방법이 없다

  return function () {
    return ++num;
  };
}());

console.log(increase()); // 1
console.log(increase()); // 2
```

즉시 실행 함수(IIFE)는 한 번만 실행되니 `num`도 한 번만 만들어지고, 반환된 함수가 그 환경을 기억하니 상태가 유지된다. 그리고 `num`에 접근할 통로는 반환된 함수뿐이다 — **정보 은닉**이다. 요즘은 클래스에 `#private` 필드(ES2022)가 있어서 은닉만이 목적이면 그쪽을 쓰지만, 함수 단위로 상태를 가둘 때는 지금도 클로저가 기본 도구다.

## 매일 쓰는 예: 디바운스

검색창에 글자를 입력할 때마다 API를 호출하면 낭비다. "입력이 멈추고 300ms 지나면 한 번만 호출"을 만들어 보자.

```javascript
function debounce(fn, delay) {
  let timer = null; // 자유 변수 — 호출 사이에 유지된다

  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

const onInput = debounce((keyword) => search(keyword), 300);
```

`onInput`이 연속으로 호출돼도 이전 타이머를 취소할 수 있는 건, 반환된 함수가 `timer`를 클로저로 기억하고 있기 때문이다. 카운터와 완전히 같은 구조다 — 상태(`timer`)를 가두고, 그 상태를 다루는 함수만 내보냈다.

## 클로저 때문에 생기는 문제: var 반복문

클로저는 도구이기도 하지만, 모르면 당하는 함정이기도 하다. 유명한 문제가 있다.

```javascript
var funcs = [];

for (var i = 0; i < 3; i++) {
  funcs[i] = function () { return i; };
}

for (var j = 0; j < funcs.length; j++) {
  console.log(funcs[j]()); // ?
}
```

`0 1 2`를 기대했다면 틀렸다. 답은 **`3 3 3`**이다.

[var 글](/javascript/05-var-let-const)에서 봤듯 `var i`는 블록 스코프가 아니라서 `i`는 전역에 딱 하나다. 세 함수는 각자의 `i`를 기억하는 게 아니라 **같은 환경의 같은 `i` 하나를 공유하는 클로저**다. 루프가 끝난 시점에 `i`는 3이고, 나중에 호출하면 셋 다 그 3을 읽는다. 클로저는 값을 복사해 두는 게 아니라 **변수가 사는 환경을 참조한다**는 걸 정확히 보여주는 예제다.

`let`으로 바꾸면 해결된다.

```javascript
const funcs = [];

for (let i = 0; i < 3; i++) {
  funcs[i] = function () { return i; };
}

funcs.forEach(f => console.log(f())); // 0 1 2
```

`let`은 **반복마다 새로운 `i` 바인딩을 만든다.** 세 함수가 각각 다른 환경을 기억하게 되니, 각자의 `i`가 0, 1, 2로 보존된다. let 이전에는 즉시 실행 함수로 `i`를 인자로 넘겨 매번 새 스코프를 만드는 우회로를 썼다 — 같은 원리를 수동으로 만든 것이다.

## React에서 만나는 함정: stale closure

이 "환경을 참조한다"는 성질이 React에서는 반대 방향의 버그를 만든다. 1초마다 카운트가 올라가는 컴포넌트를 만들었다고 하자.

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount(count + 1); // count는 첫 렌더의 0에 갇혀 있다
    }, 1000);
    return () => clearInterval(id);
  }, []);

  return <div>{count}</div>;
}
```

기대와 달리 카운트는 **1에서 멈춘다.** 이펙트 안의 함수는 첫 렌더 시점에 만들어진 클로저라 그때의 `count`(0)를 기억한다. 이후 렌더에서 `count`가 바뀌어도 이 클로저가 보는 `count`는 여전히 0이고, `setCount(0 + 1)`만 1초마다 반복된다. 오래된(stale) 값을 참조한다고 해서 **stale closure**라고 부른다.

var 반복문과 묘하게 대칭이다. var 반복문은 "다 같은 환경을 봐서" 문제였고, 여기는 "옛 환경에 갇혀서" 문제다. 둘 다 원인은 같다 — 클로저는 값이 아니라 환경을 기억한다는 것. 해결은 최신 상태를 함수형 업데이트로 받아오는 것이다.

```jsx
setCount(c => c + 1); // 인자 c는 항상 최신 상태다
```

사실 `useState`가 상태를 유지하는 방식도 같은 원리로 이해할 수 있다. 함수 컴포넌트는 렌더마다 실행되고 끝나는데 상태가 살아남는 이유는, React가 상태를 컴포넌트 함수 바깥에 가둬두고 훅이 그걸 참조하기 때문이다(실제 구현은 fiber라는 자료구조에 저장하지만, 구조는 카운터 예제와 같다 — 상태를 밖에 가두고 접근 통로만 내어준다). 클로저를 모르면 React의 절반은 마법처럼 보일 수밖에 없다.

## 안 놓으면 누수가 된다

마지막으로 비용 이야기. 클로저가 참조하는 렉시컬 환경은 [지난 글](/javascript/07-closure)에서 봤듯 GC가 회수하지 못한다. 뒤집어 말하면, **클로저를 오래 붙들고 있으면 그 환경 전체가 메모리에 남는다.**

```javascript
function attach() {
  const bigData = new Array(1_000_000).fill('...');

  window.addEventListener('resize', () => {
    console.log(bigData.length); // bigData를 참조하는 클로저
  });
}
```

이 리스너를 해제하지 않는 한 `bigData`는 영원히 회수되지 않는다. 클로저 자체가 누수는 아니다 — **필요가 끝난 클로저를 놓아주지 않는 것**이 누수다. 리스너는 `removeEventListener`, 타이머는 `clearTimeout`으로 참조를 끊어주면, 클로저가 도달 불가능해지는 순간 환경도 함께 회수된다. React의 `useEffect`가 클린업 함수 반환을 요구하는 것도 같은 이유다.

---

클로저는 **상태를 함수에 가두는 도구**다. 가둔 상태는 지키는 힘(은닉)이 되고, 낡으면 버그(stale closure)가 되고, 안 놓으면 누수가 된다. 셋 다 "클로저는 값이 아니라 환경을 기억한다"는 한 문장에서 나온다.

그런데 여기까지 오면서 함수가 기억하는 것들은 전부 **정의될 때** 정해졌다. 스코프도, 클로저도. 그렇다면 함수 안의 `this`도 정의될 때 정해질까? 사실 this는 정반대다 — **호출될 때** 정해진다. 다음 글에서 다룬다. → [this는 언제 결정되는가](/javascript/09-this-binding)
