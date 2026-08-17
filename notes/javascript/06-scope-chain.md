---
title: 스코프 체인은 어떻게 만들어지는가
description: 상위 스코프는 함수를 호출한 위치가 아니라 정의한 위치가 결정한다
---

# 스코프 체인은 어떻게 만들어지는가

자바스크립트를 처음 공부할 당시 이 문제와 유사한 문제를 처음 봤을 때 나는 틀렸다.

```javascript
var x = 1;

function foo() {
  var x = 10;
  bar();
}

function bar() {
  console.log(x);
}

foo(); // ?
bar(); // ?
```

내 예상은 `10`과 `1`이었다. `foo()`가 `bar()`를 호출했으니, `bar` 안의 `x`는 호출한 쪽인 `foo`의 `x = 10`을 참조할 거라고 생각했다. 실제 답은 둘 다 `1`이다. `bar`는 누가 호출했든 상관없이 전역의 `x`만 본다.

## 문제는 "상위 스코프가 언제 정해지는가"

이 문제를 틀리는 이유는 상위 스코프가 **호출 위치**에서 정해진다고 생각하기 때문이다. 자바스크립트는 반대다. 함수의 상위 스코프는 **함수를 어디서 정의했는가**로 결정되고, 정의가 끝난 순간 이미 확정되어 있다. 호출 위치는 아무 영향이 없다.

`bar`는 전역에서 정의됐다. 그래서 `bar`의 상위 스코프는 영원히 전역 스코프이고, `foo` 안에서 호출되든 어디서 호출되든 `x`를 찾을 때 전역으로 간다. 이 검색 과정을 움직임으로 보면 이렇다.

<svg viewBox="0 0 660 350" role="img" aria-label="bar 스코프에서 x를 찾지 못하면 호출한 foo가 아니라 정의된 곳의 상위 스코프인 전역으로 올라가 x를 찾는 애니메이션" style="max-width:660px;width:100%;height:auto;margin:16px 0">
<defs><marker id="sc-ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-brand-1)"/></marker></defs>
<rect x="20" y="36" width="620" height="270" rx="10" class="sc-box"/>
<text x="36" y="60" class="sc-t">전역 스코프</text>
<text x="36" y="90" class="sc-c">var x = 1;</text>
<rect x="40" y="112" width="250" height="150" rx="8" class="sc-box"/>
<text x="56" y="136" class="sc-t">foo 스코프</text>
<text x="56" y="164" class="sc-c">var x = 10;</text>
<text x="56" y="190" class="sc-c sc-dim">bar(); // 호출</text>
<rect x="350" y="112" width="250" height="150" rx="8" class="sc-box"/>
<text x="366" y="136" class="sc-t">bar 스코프</text>
<text x="366" y="164" class="sc-c">console.log(x);</text>
<g class="sc-g1"><rect x="350" y="112" width="250" height="150" rx="8" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2"/><text x="366" y="196" class="sc-s sc-hl">① x? 여기엔 없다</text></g>
<g class="sc-g2"><path d="M420,112 C420,78 250,70 140,84" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#sc-ah)"/><text x="330" y="66" text-anchor="middle" class="sc-s sc-hl">② [[Environment]]에 저장된 상위 스코프로</text></g>
<g class="sc-g3"><rect x="28" y="70" width="106" height="28" rx="6" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2"/><text x="150" y="98" class="sc-s sc-hl">③ 1 발견!</text></g>
<path d="M350,232 L296,232" fill="none" stroke="var(--vp-c-text-3)" stroke-width="1.5" stroke-dasharray="5 4"/>
<text x="323" y="226" text-anchor="middle" class="sc-s sc-dim">✕</text>
<text x="323" y="252" text-anchor="middle" class="sc-s sc-dim">검색 경로 아님</text>
<text x="330" y="334" text-anchor="middle" class="sc-s">bar를 호출한 건 foo지만, x는 bar가 정의된 곳의 상위 스코프(전역)에서 찾는다</text>
</svg>

이렇게 정의 위치(렉시컬, lexical — "코드가 쓰인 곳")로 스코프가 정해지는 방식을 **렉시컬 스코프**라고 한다. 반대로 호출 위치에 따라 스코프가 바뀌는 방식은 동적 스코프라고 부르는데, 자바스크립트를 포함한 대부분의 언어는 렉시컬 스코프를 택했다. 함수의 동작이 호출될 때마다 달라진다면 코드를 읽는 것만으로 결과를 예측할 수 없기 때문이다.

## 스코프 체인: 검색은 안에서 밖으로, 한 방향으로만

스코프가 중첩되면 어떻게 될까.

```javascript
const x = 1;

function foo() {
  const y = 2;

  function bar() {
    const z = 3;
    console.log(x + y + z);
  }
  bar();
}

foo(); // 6
```

`bar` 안에서 `x`, `y`, `z`를 모두 참조할 수 있는 이유는 스코프가 계층으로 연결되어 있기 때문이다. `bar` 스코프 → `foo` 스코프 → 전역 스코프. 이 연결을 **스코프 체인**이라고 한다.

엔진이 식별자를 찾는 규칙은 단순하다. **자기 스코프에서 먼저 찾고, 없으면 바로 위 상위 스코프로 올라간다.** 전역까지 갔는데도 없으면 그때 `ReferenceError`다. 중요한 건 이 검색이 **단방향**이라는 것이다. 안에서 밖으로는 올라가지만, 밖에서 안으로 내려오지는 않는다. 그래서 전역에서 `bar` 안의 `z`를 참조할 수는 없다.

이 규칙을 알면 같은 이름이 겹칠 때의 동작도 설명된다.

```javascript
function foo() {
  console.log('global function foo');
}

function bar() {
  function foo() {
    console.log('local function foo');
  }
  foo(); // local function foo
}

bar();
```

`bar` 안에서 `foo`를 호출하면 검색이 자기 스코프에서 시작되므로 중첩 함수 `foo`가 먼저 잡힌다. 안쪽 식별자가 바깥 식별자를 가리는 이 현상을 **섀도잉**(shadowing)이라고 한다. [지난 글](/javascript/05-var-let-const)의 TDZ 문제에서 엔진이 바깥 `foo` 대신 블록 안의 `foo`를 잡은 것도 같은 원리다 — 블록도 (let/const에게는) 하나의 스코프이고, 검색은 가장 안쪽에서 시작되니까.

## 그 체인은 누가, 언제 만드나?

함수가 정의될 때다. 함수는 자신이 정의된 시점의 스코프(정확히는 렉시컬 환경)에 대한 참조를 내부에 저장해 둔다. 스펙에서는 이걸 함수 객체의 `[[Environment]]` 내부 슬롯이라고 부른다. 함수가 호출되면 자신의 지역 스코프를 새로 만들고, 그 상위를 `[[Environment]]`에 저장해 둔 스코프로 연결한다. 이 연결이 쌓인 것이 스코프 체인이다.

처음 문제로 돌아가면, `bar`의 `[[Environment]]`에는 정의 시점의 전역 스코프가 저장되어 있다. `foo`가 호출하든 말든 `bar`의 체인은 `bar → 전역`으로 이미 굳어 있는 것이다.

사실 이 대목이 이 글에서 제일 중요하다. 함수가 "자신이 태어난 스코프를 기억한다"는 것 — 여기서 자연스럽게 다음 질문이 나온다. **함수를 정의한 바깥 함수가 이미 종료됐는데도, 그 기억이 유효할까?**

```javascript
function outer() {
  const x = 10;
  return function inner() {
    console.log(x);
  };
}

const fn = outer(); // outer는 이미 종료됐다
fn(); // ?
```

답은 `10`이다. `outer`는 끝났는데 `inner`는 여전히 `outer`의 `x`를 참조한다. 이게 바로 그 유명한 클로저다.

---

상위 스코프는 함수를 **호출한 위치가 아니라 정의한 위치**가 결정하고, 함수는 그 스코프를 `[[Environment]]`에 담아 평생 기억한다. 이 문장을 이해했다면 클로저는 이미 절반 이상 이해한 것이라고 나는 생각한다. 다음 글에서 마저 다루겠다. → [클로저는 어떻게 가능한가](/javascript/07-closure)

<style>
.sc-t{font:600 13px var(--vp-font-family-base);fill:var(--vp-c-text-2)}
.sc-c{font:12.5px var(--vp-font-family-mono);fill:var(--vp-c-text-1)}
.sc-dim{fill:var(--vp-c-text-3)}
.sc-hl{fill:var(--vp-c-brand-1);font-weight:600}
.sc-s{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-2)}
.sc-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.sc-g1{animation:sc-k1 5.5s infinite}
.sc-g2{animation:sc-k2 5.5s infinite}
.sc-g3{animation:sc-k3 5.5s infinite}
@keyframes sc-k1{0%{opacity:0}6%{opacity:1}90%{opacity:1}97%{opacity:0}100%{opacity:0}}
@keyframes sc-k2{0%,32%{opacity:0}40%{opacity:1}90%{opacity:1}97%{opacity:0}100%{opacity:0}}
@keyframes sc-k3{0%,60%{opacity:0}68%{opacity:1}90%{opacity:1}97%{opacity:0}100%{opacity:0}}
@media (prefers-reduced-motion: reduce){.sc-g1,.sc-g2,.sc-g3{animation:none}}
</style>
