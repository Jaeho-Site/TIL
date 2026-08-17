---
title: 원시 타입과 객체는 뭐가 다른가
description: 변수에 담기는 것은 값인가 참조인가 — 불변성, 그리고 const 객체가 수정되는 이유
---

# 원시 타입과 객체는 뭐가 다른가

거의 같은 모양의 코드 두 개를 살펴보자. 출력이 뭘까?

```javascript
let a = 'hello';
let b = a; // 복사
a = 'world';
console.log(b); // ?
```

```javascript
const x = { name: 'Lee' };
const y = x; // 복사
x.name = 'Kim';
console.log(y.name); // ?
```

첫 번째는 `'hello'`다. `b`는 복사해 온 값을 그대로 갖고 있고, 이후 `a`를 바꿔도 영향이 없다. 그런데 두 번째는 `'Kim'`이다. **`y`를 건드린 적이 없는데 `x`를 바꿨더니 `y`가 따라 바뀌었다.** 같은 "복사"인데 왜 결과가 다를까?

## 변수에 담기는 것이 다르다

자바스크립트의 값은 딱 두 부류다. **원시 타입**(string, number, boolean, undefined, null, symbol, bigint — 7종)과 **객체**(그 외 전부 — 배열, 함수, 정규식도 모두 객체다). 그리고 두 부류는 변수에 담기는 내용물부터 다르다.

- **원시 값은 변수에 값 자체가 담긴다.** `let b = a`는 값을 통째로 복사한다. 복사 후 `a`와 `b`는 서로 완전히 남남이다.
- **객체는 변수에 참조(어디 있는지 가리키는 주소)가 담긴다.** 객체 자체는 메모리 어딘가(엔진 구현으로는 힙)에 하나만 있고, 변수는 그곳을 가리킬 뿐이다. `const y = x`가 복사하는 건 객체가 아니라 **참조**다.

그래서 두 번째 문제에서 `x`와 `y`는 **같은 객체를 가리키는 두 개의 이름**이 된다. `x.name = 'Kim'`은 그 공유된 객체를 바꾼 것이고, `y`로 들여다봐도 당연히 바뀌어 보인다.

<svg viewBox="0 0 680 250" role="img" aria-label="원시 값은 변수마다 값을 따로 갖고, 객체는 두 변수가 같은 객체를 가리키는 구조 비교" style="max-width:680px;width:100%;height:auto;margin:16px 0">
<defs><marker id="dt-ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-brand-1)"/></marker></defs>
<text x="20" y="30" class="dt-t">원시 값 — 값을 복사한다</text>
<rect x="20" y="50" width="130" height="40" rx="6" class="dt-box"/>
<text x="36" y="75" class="dt-c">a: 'world'</text>
<rect x="20" y="104" width="130" height="40" rx="6" class="dt-box"/>
<text x="36" y="129" class="dt-c">b: 'hello'</text>
<text x="20" y="180" class="dt-dim">복사한 뒤로는 남남 —</text>
<text x="20" y="198" class="dt-dim">a를 바꿔도 b는 그대로</text>
<line x1="345" y1="24" x2="345" y2="220" class="dt-ln"/>
<text x="390" y="30" class="dt-t">객체 — 참조를 복사한다</text>
<rect x="390" y="50" width="90" height="40" rx="6" class="dt-box"/>
<text x="406" y="75" class="dt-c">x: ref</text>
<rect x="390" y="104" width="90" height="40" rx="6" class="dt-box"/>
<text x="406" y="129" class="dt-c">y: ref</text>
<rect x="540" y="66" width="130" height="60" rx="8" class="dt-live"/>
<text x="556" y="102" class="dt-c">name: 'Kim'</text>
<path d="M484,70 C510,70 520,86 535,92" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#dt-ah)"/>
<path d="M484,124 C510,124 520,106 535,100" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#dt-ah)"/>
<text x="390" y="180" class="dt-dim">두 변수가 같은 객체를 가리킨다 —</text>
<text x="390" y="198" class="dt-dim">x로 바꾸면 y로 봐도 바뀌어 있다</text>
</svg>

왜 이렇게 설계했을까 생각해 보면 크기 문제다. 숫자나 짧은 문자열은 복사 비용이 싸지만, 객체는 얼마든지 커질 수 있다. 프로퍼티가 수백 개인 객체를 대입할 때마다 통째로 복사하는 건 낭비라서, "위치만 알려주는" 참조 방식이 기본이 된 것이다.

## 원시 값은 바꿀 수 없다 — 불변성

원시 타입에는 성질이 하나 더 있다. **값 자체를 수정할 방법이 없다**는 것이다. 처음엔 이 말이 이상했다. `a = 'world'`로 방금 바꾸지 않았나?

아니다. 그건 값을 바꾼 게 아니라 **변수가 새 값을 가리키게 재할당한 것**이다. `'hello'`라는 값 자체는 태어난 그대로 있다가 버려질 뿐이다. 진짜로 값을 수정하려는 시도는 조용히 무시된다.

```javascript
let str = 'hello';
str[0] = 'H'; // 에러도 없이 무시된다
console.log(str); // 'hello'

console.log(str.toUpperCase()); // 'HELLO' — 새 문자열을 만들어 반환할 뿐
console.log(str); // 'hello' — 원본은 그대로
```

참고로 "조용히 무시"는 비엄격 모드 이야기고, strict mode(ESM 모듈, 클래스 내부)에서는 같은 코드가 `TypeError`를 던진다 — 나중에 var에서 다룰 "실수를 늦게 발견 vs 즉시 발견"의 구도가 여기에도 있다. 문자열 메서드가 전부 "바꾸지 않고 새로 만들어 반환"하는 이유가 이것이다. 반면 객체는 언제든 내용물을 수정할 수 있는 **가변(mutable)** 값이다.

`const`로 선언한 객체가 수정되는 이유 — **const가 잠그는 건 변수에 담긴 내용물(참조)이지, 참조가 가리키는 객체가 아니다.** 변수와 값이 서로 다른 층에 있다는 걸 알아야 이 문장이 읽힌다.

## 원시 값인데 왜 메서드를 쓸 수 있나

사소하지만 한 번쯤 궁금해지는 지점이다. `'hello'`는 객체가 아니라면서 `str.toUpperCase()`처럼 프로퍼티 접근이 된다?

원시 값에 객체처럼 접근하는 순간, 엔진이 **래퍼 객체**(String, Number 등의 인스턴스)를 임시로 만들어 그걸 통해 메서드를 실행하고 바로 버린다. `toUpperCase`가 실제로 사는 곳은 `String.prototype` — [프로토타입 체인](/javascript/11-prototype-chain) 검색이 여기서도 일어나고 있었던 것이다.

---

원시 타입과 객체의 차이는 결국 한 문장이다. **변수에 값이 담기는가, 값의 위치(참조)가 담기는가.** 복사·비교·수정의 모든 차이가 이 한 줄에서 갈라져 나온다.

그럼 다음 궁금증은 자연스럽다. 참조 복사 말고 **객체의 내용물을 진짜로 복사**하고 싶으면 어떻게 해야 할까? 스프레드로 복사하면 되는 줄 알았는데, 거기엔 함정이 하나 있다. → [얕은 복사와 깊은 복사는 뭐가 다른가](/javascript/02-shallow-deep-copy)

<style>
.dt-t{font:600 13.5px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.dt-c{font:12.5px var(--vp-font-family-mono);fill:var(--vp-c-text-1)}
.dt-dim{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.dt-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.dt-live{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-brand-1);stroke-width:1.5}
.dt-ln{stroke:var(--vp-c-divider);stroke-dasharray:4 4}
</style>
