---
title: 자바스크립트의 상속은 어떻게 동작하는가
description: 상속은 복사가 아니라 링크다 — 프로토타입 체인, __proto__와 prototype의 차이
---

# 자바스크립트의 상속은 어떻게 동작하는가

[this 글](/javascript/09-this-binding)에서 "프로토타입 상속은 수천 개의 인스턴스가 메서드 하나를 공유하는 구조"라고 말하고 지나갔다. 그 공유가 어떻게 가능한지 확인하는 문제부터 본다.

```javascript
function Circle(radius) {
  this.radius = radius;
  this.getArea = function () {
    return Math.PI * this.radius ** 2;
  };
}

const circle1 = new Circle(1);
const circle2 = new Circle(2);

console.log(circle1.getArea === circle2.getArea); // ?
```

답은 `false`다. 두 인스턴스의 `getArea`는 내용이 완전히 같은데도 **다른 함수 객체**다. 생성자 본문이 인스턴스를 만들 때마다 실행되니, 함수도 매번 새로 만들어진다. 인스턴스를 1,000개 만들면 똑같은 함수가 1,000개 생긴다는 뜻이다.

메서드는 하나만 만들어 모두가 공유하는 게 맞다. 그런데 공유하려면 그 하나를 **어디에** 둬야 할까? 전역에 두면 [전역 오염](/javascript/05-var-let-const)이고, 각 인스턴스에 두면 지금처럼 중복이다. 자바스크립트의 답이 프로토타입이다.

## 모든 객체에는 숨겨진 부모 링크가 있다

자바스크립트의 모든 객체는 내부에 `[[Prototype]]`이라는 숨겨진 링크를 하나 갖고 있다. 자신의 "부모 역할을 하는 객체"를 가리키는 참조다. 그리고 프로퍼티 접근에는 규칙이 있다.

**자기 자신에게 없는 프로퍼티는, 이 링크를 따라 올라가며 찾는다.**

이 링크로 연결된 사슬이 **프로토타입 체인**이다. 어디서 본 구조다 — [식별자를 스코프 체인에서 찾아 올라가던 것](/javascript/06-scope-chain)과 똑같은 패턴이다. 식별자는 스코프 체인에서, 프로퍼티는 프로토타입 체인에서 찾는다.

이제 메서드 공유 문제를 풀 수 있다. 공유할 메서드를 인스턴스들의 **공통 부모**에 두면 된다.

```javascript
function Circle(radius) {
  this.radius = radius;
}

// 모든 인스턴스의 공통 부모에 메서드를 하나만 만든다
Circle.prototype.getArea = function () {
  return Math.PI * this.radius ** 2;
};

const circle1 = new Circle(1);
const circle2 = new Circle(2);

console.log(circle1.getArea === circle2.getArea); // true — 같은 함수를 공유한다
console.log(circle1.getArea()); // 3.141592653589793
```

`circle1.getArea()`를 호출하면 엔진은 먼저 `circle1` 자신에게서 `getArea`를 찾고, 없으니 `[[Prototype]]` 링크를 따라 `Circle.prototype`으로 올라가 거기서 찾아낸다. 메서드는 한 곳에 있는데 모든 인스턴스가 쓸 수 있다 — 이게 자바스크립트 상속의 실체다. **무언가를 물려받아 복사하는 게 아니라, 없으면 부모에게 가서 찾는 것이다.**

<svg viewBox="0 0 680 300" role="img" aria-label="circle1에서 getArea를 찾지 못하면 __proto__ 링크를 따라 Circle.prototype에서 찾고, 체인은 Object.prototype을 거쳐 null로 끝나는 구조" style="max-width:680px;width:100%;height:auto;margin:16px 0">
<defs><marker id="pc-ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-brand-1)"/></marker><marker id="pc-ad" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-text-3)"/></marker></defs>
<rect x="20" y="70" width="170" height="84" rx="8" class="pc-box"/>
<text x="36" y="94" class="pc-s">circle1</text>
<text x="36" y="118" class="pc-c">radius: 1</text>
<text x="36" y="140" class="pc-dim">getArea? ① 없다</text>
<rect x="250" y="70" width="180" height="84" rx="8" class="pc-live"/>
<text x="266" y="94" class="pc-s">Circle.prototype</text>
<text x="266" y="118" class="pc-c">getArea <tspan class="pc-hl">② 발견!</tspan></text>
<rect x="490" y="70" width="170" height="84" rx="8" class="pc-box"/>
<text x="506" y="94" class="pc-s">Object.prototype</text>
<text x="506" y="118" class="pc-c">hasOwnProperty,</text>
<text x="506" y="138" class="pc-c">toString, …</text>
<path d="M194,100 L245,100" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#pc-ah)"/>
<text x="219" y="88" text-anchor="middle" class="pc-hl">__proto__</text>
<path d="M434,100 L485,100" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#pc-ah)"/>
<text x="459" y="88" text-anchor="middle" class="pc-hl">__proto__</text>
<path d="M575,158 L575,196" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#pc-ah)"/>
<text x="575" y="218" text-anchor="middle" class="pc-s">null — 체인의 끝</text>
<rect x="20" y="196" width="170" height="50" rx="8" class="pc-box"/>
<text x="36" y="226" class="pc-s">Circle 함수 객체</text>
<path d="M194,220 C260,220 340,200 340,158" fill="none" stroke="var(--vp-c-text-3)" stroke-width="1.5" marker-end="url(#pc-ad)"/>
<text x="248" y="242" class="pc-dim">.prototype 프로퍼티</text>
<text x="20" y="284" class="pc-dim">검색은 자기 자신부터 __proto__ 링크를 따라 위로 — 끝(null)까지 없으면 undefined</text>
</svg>

## __proto__와 prototype은 다른 것이다

위 자료처럼 교재에 그림에 같은 그림이 다 나왔는데, 처음에 나는 이 둘이 정말 헷갈렸다. 하지만 둘은 이름이 비슷할 뿐 **주어가 다르다.**

- **`__proto__`** — 모든 객체가 가진, **자기 부모를 가리키는 링크**(`[[Prototype]]`에 접근하는 통로). "나의 부모는 누구인가"
- **`prototype`** — 함수만 가진 프로퍼티로, **내가 new로 만들 인스턴스들의 부모가 될 객체**. "내 자식들의 부모는 누구가 될 것인가"

그래서 이 등식이 성립한다.

```javascript
console.log(circle1.__proto__ === Circle.prototype); // true
console.log(Object.getPrototypeOf(circle1) === Circle.prototype); // true — 표준 방법
```

참고로 `__proto__`는 객체 자신의 프로퍼티도 아니다. `Object.prototype`에 정의된 접근자 프로퍼티를 모든 객체가 체인으로 상속받아 쓰는 것이고, 지금은 표준 메서드인 `Object.getPrototypeOf` / `Object.setPrototypeOf` 사용이 권장된다.

## 체인의 끝은 어디인가

`Circle.prototype`도 객체니까 부모가 있다. 따라가 보면:

```javascript
console.log(Object.getPrototypeOf(Circle.prototype) === Object.prototype); // true
console.log(Object.getPrototypeOf(Object.prototype)); // null — 여기가 끝
```

모든 체인의 종점은 `Object.prototype`이고, 그 위는 `null`이다(유일한 예외는 `Object.create(null)`로 부모 없이 만든 객체 — 체인이 아예 없어서 `hasOwnProperty`조차 못 쓴다). 종점까지 뒤져도 없으면 에러가 아니라 `undefined`가 나온다(식별자를 못 찾으면 `ReferenceError`가 나는 스코프 체인과의 차이점이다).

이 구조 덕분에 설명되는 일상이 하나 있다. 우리가 아무 객체에나 `hasOwnProperty`나 `toString`을 쓸 수 있는 이유다.

```javascript
const person = { name: 'Lee' };

console.log(person.hasOwnProperty('name')); // true — 그런데 이 메서드는 누구 것인가?
```

`person`에 직접 정의한 적 없는 이 메서드는 `Object.prototype`의 것이다. 모든 객체는 체인의 종점으로 `Object.prototype`을 두기 때문에, 거기 있는 메서드들을 전부 "상속"받는다. 매일 쓰던 기능이 사실 프로토타입 체인 검색이었다.

---

자바스크립트의 상속은 **복사가 아니라 링크**다. 없는 프로퍼티는 `__proto__`를 따라 올라가며 찾는다. (식별자를 스코프 체인에서 찾듯이)

그런데 그림을 다시 보면 궁금한 게 남는다. `circle1.__proto__`가 `Circle.prototype`을 가리키도록 **누가 연결해 줬을까?** 내가 한 적은 없다. 범인은 `new`다. → [new는 무슨 일을 하는가](/javascript/12-new-and-constructor)

<style>
.pc-s{font:600 13px var(--vp-font-family-base);fill:var(--vp-c-text-2)}
.pc-c{font:12.5px var(--vp-font-family-mono);fill:var(--vp-c-text-1)}
.pc-dim{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.pc-hl{font:600 12px var(--vp-font-family-base);fill:var(--vp-c-brand-1)}
.pc-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.pc-live{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-brand-1);stroke-width:1.5}
</style>
