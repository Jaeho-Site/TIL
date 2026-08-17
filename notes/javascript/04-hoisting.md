---
title: 호이스팅은 왜 일어나는가
description: 선언문이 끌어올려지는 게 아니라, 실행 전에 먼저 처리될 뿐이다
---

# 호이스팅은 왜 일어나는가

책을 읽다가 만난 이 코드부터 확인해보자. 출력이 뭘까?

```javascript
console.log(score); // ?

var score = 80;

console.log(score); // ?
```

처음 이 코드를 봤을 때 나는 첫 줄에서 에러가 날 거라고 생각했다. `score`는 아직 선언되지 않았으니까. 그런데 실제로 실행하면 에러 없이 `undefined`와 `80`이 출력된다. 한술 더 떠서 이런 코드도 동작한다.

```javascript
console.log(score); // undefined

score = 80; // 할당이 선언보다 위에 있다
var score;

console.log(score); // 80
```

"코드는 위에서 아래로 실행된다"는 직관이 여기서 깨진다. 선언문이 제일 아래에 있는데 왜 에러가 안 날까?

## 문제는 "언제 선언이 처리되는가"

이 문제를 틀리는 이유는 자바스크립트 엔진이 코드를 **한 번에 처리하지 않는다**는 걸 모르기 때문이다. 엔진은 코드를 실행하기 전에 먼저 한 바퀴 훑는다. 이 과정은 두 단계로 나눠 이해하면 된다.

1. **평가 단계** — 코드를 실행하기 전에 선언문(변수 선언, 함수 선언)만 먼저 찾아서 실행 컨텍스트에 등록한다. `var`로 선언한 변수는 이때 `undefined`로 초기화까지 된다.
2. **실행 단계** — 선언문을 제외한 코드가 위에서 아래로 한 줄씩 실행된다. 할당문 `score = 80`은 이때 실행된다.

그래서 `console.log(score)`가 선언문보다 위에 있어도, 실행 단계가 시작되는 시점엔 이미 `score`가 등록되어 있다. 에러가 아니라 `undefined`가 나오는 이유다.

<svg viewBox="0 0 680 290" role="img" aria-label="평가 단계에서 선언이 먼저 등록되고, 실행 단계에서 코드가 실행되는 2단계 다이어그램" style="max-width:680px;width:100%;height:auto;margin:16px 0">
<defs><marker id="hz-ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-text-3)"/></marker></defs>
<text x="20" y="24" class="hz-t">① 평가 단계 — 선언문만 먼저 처리</text>
<rect x="20" y="38" width="300" height="66" rx="8" class="hz-box"/>
<text x="36" y="64" class="hz-c hz-dim">console.log(score);</text>
<text x="36" y="90" class="hz-c"><tspan class="hz-hl">var score</tspan> = 80;</text>
<path d="M170,104 L170,138" class="hz-ar"/>
<rect x="20" y="144" width="300" height="62" rx="8" class="hz-ctx"/>
<text x="36" y="166" class="hz-s">실행 컨텍스트</text>
<text x="36" y="192" class="hz-c">score: <tspan class="hz-hl">undefined</tspan></text>
<text x="20" y="238" class="hz-s">실행 전에 score가 이미 undefined로 등록된다</text>
<text x="360" y="24" class="hz-t">② 실행 단계 — 위에서 아래로 실행</text>
<rect x="360" y="38" width="300" height="66" rx="8" class="hz-box"/>
<text x="376" y="64" class="hz-c"><tspan class="hz-hl">console.log(score);</tspan></text>
<text x="376" y="90" class="hz-c">var score <tspan class="hz-hl">= 80;</tspan></text>
<path d="M510,104 L510,138" class="hz-ar"/>
<rect x="360" y="144" width="300" height="62" rx="8" class="hz-ctx"/>
<text x="376" y="166" class="hz-s">실행 컨텍스트</text>
<text x="376" y="192" class="hz-c">score: undefined <tspan class="hz-hl">→ 80</tspan></text>
<text x="360" y="238" class="hz-s">1행: 등록돼 있던 undefined를 출력</text>
<text x="360" y="258" class="hz-s">2행: 이제서야 80이 할당된다</text>
</svg>

여기서 오해하기 쉬운 게 하나 있다. 호이스팅(hoisting)이라는 이름 때문에 선언문이 코드 최상단으로 "끌어올려져서 이동한다"고 상상하기 쉬운데, 사실 코드는 어디로도 이동하지 않는다. 선언이 **실행보다 먼저 처리되는 순서의 문제**일 뿐이고, 그 결과가 마치 끌어올려진 것처럼 보이는 것이다.

## 그럼 함수도 호이스팅되나?

된다. 그런데 **어떻게 정의했느냐에 따라 결과가 완전히 다르다.**

```javascript
console.log(add(2, 5)); // 7
console.log(sub(2, 5)); // TypeError: sub is not a function

// 함수 선언문
function add(x, y) {
  return x + y;
}

// 함수 표현식
var sub = function (x, y) {
  return x - y;
};
```

- **함수 선언문**은 평가 단계에서 **함수 객체까지 통째로** 등록된다. 그래서 선언문보다 위에서 호출해도 동작한다.
- **함수 표현식**은 함수가 아니라 **변수 선언**이다. `var sub`만 호이스팅되어 `undefined`로 초기화되고, 함수 객체 할당은 실행 단계에서 그 줄에 도달해야 일어난다. 그래서 `undefined`를 호출하려다 `TypeError`가 난다.

에러 종류를 구분하는 것도 중요하다. `sub`가 아예 없어서 나는 `ReferenceError`가 아니라, `undefined`라는 값은 있는데 함수가 아니라서 나는 `TypeError`다. 이 차이를 설명할 수 있으면 호이스팅을 정확히 이해한 것이다.

## 왜 이렇게 설계했을까?

함수 선언문 호이스팅은 나름의 쓸모가 있다. 함수를 정의 순서와 상관없이 호출할 수 있으니, 핵심 로직을 파일 상단에 두고 세부 구현 함수를 아래로 내리는 식으로 코드를 배치할 수 있다.

반면 `var`의 호이스팅은 의도된 기능이라기보다 이 2단계 처리 방식의 부작용에 가깝다. 선언 전에 변수를 참조했는데 에러 대신 `undefined`가 조용히 나오는 건 버그를 숨기는 동작이다. 개인적으로 이건 언어가 "실수를 허용해 주는" 게 아니라 "실수를 늦게 발견하게 만드는" 쪽이라고 생각한다.

그래서 ES6의 `let`/`const`는 같은 호이스팅을 겪으면서도 다르게 동작하도록 설계됐다. 선언 전에 참조하면 `undefined`가 아니라 `ReferenceError`를 던진다.

---

호이스팅은 코드가 위로 이동하는 현상이 아니라, **선언이 실행보다 먼저 처리되는 평가 단계의 흔적**이다.

그런데 방금 "let도 같은 호이스팅을 겪는다"고 했다. 근데 왜 let은 다르게 동작할까? → [var와 let/const는 뭐가 다른가](/javascript/05-var-let-const)

<style>
.hz-t{font:600 13.5px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.hz-s{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-2)}
.hz-c{font:12.5px var(--vp-font-family-mono);fill:var(--vp-c-text-1)}
.hz-dim{fill:var(--vp-c-text-3)}
.hz-hl{fill:var(--vp-c-brand-1);font-weight:600}
.hz-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.hz-ctx{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-brand-1)}
.hz-ar{stroke:var(--vp-c-text-3);stroke-width:1.5;fill:none;marker-end:url(#hz-ah)}
</style>
