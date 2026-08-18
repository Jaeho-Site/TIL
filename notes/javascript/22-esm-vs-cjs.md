---
title: ESM과 CJS는 뭐가 다른가
description: 파일이 곧 스코프가 되기까지 — IIFE의 시대, 값 복사 vs 라이브 바인딩, 정적 구조의 의미
---

# ESM과 CJS는 뭐가 다른가

모듈이 왜 필요한지부터가 사실 하나의 문제다. script 파일을 나눠 로드하던 시절의 코드다.

```html
<script src="a.js"></script> <!-- 안에서 var x = 1; -->
<script src="b.js"></script> <!-- 안에서 var x = 2; -->
<script>
  console.log(x); // ?
</script>
```

답은 `2`다. 파일을 나눴어도 **모든 script는 하나의 전역 스코프를 공유한다.** a.js의 `x`를 b.js가 조용히 덮어썼고, 에러조차 없다. [var의 전역 오염](/javascript/05-var-let-const)이 파일 단위로 확장된 것이다 — 파일은 나뉘어 있지만, 파일이 스코프는 아니었다.

## 모듈 이전의 시대: 함수로 파일을 흉내 내다

언어에 모듈이 없던 시절, 개발자들은 이미 가진 도구로 격리를 만들었다. 스코프를 만들 수 있는 유일한 단위 — [함수](/javascript/06-scope-chain)다.

```javascript
// a.js
var moduleA = (function () {
  var x = 1; // 이제 전역이 아니다

  return { getX: function () { return x; } }; // 공개할 것만 클로저로
}());
```

[클로저 은닉](/javascript/08-closure-in-practice)에서 본 IIFE 패턴이 사실 모듈 시스템의 수공업 버전이었던 셈이다. 하지만 한계가 명확했다. 공개 창구(`moduleA`)는 여전히 전역에 놓이고, 파일 간 의존 순서는 script 태그 순서로 사람이 관리해야 했다. 이 문제를 제대로 풀려는 시도에서 두 모듈 시스템이 나왔다. 서버(Node.js) 진영의 **CommonJS**(CJS, `require`/`module.exports`)가 먼저였고, 언어 표준으로는 ES2015에 **ESM**(`import`/`export`)이 들어왔다.

```javascript
// CJS
const { count } = require('./counter');
module.exports = { increase };

// ESM
import { count } from './counter.mjs';
export const increase = () => {};
```

문법 차이로 보이지만, 실제 차이는 세 축이다.

## 차이 ①: 내보내는 것이 값인가, 연결인가

제일 미묘하고 그래서 제일 자주 회자되는 차이부터. 두 시스템은 **export한 변수가 나중에 바뀌었을 때** 동작이 갈린다.

```javascript
// counter 모듈
export let count = 0;
export const increase = () => { count += 1; };

// 사용하는 쪽
import { count, increase } from './counter.mjs';

increase();
console.log(count); // ESM: 1
```

- **CJS**는 `module.exports` 객체에 담긴 **값의 복사본**을 받는다(정확히는 그 시점 값을 담은 객체). require 이후 모듈 내부에서 원시 값이 바뀌어도 받아온 쪽은 모른다.
- **ESM**은 **라이브 바인딩(live binding)** — 값이 아니라 원본 변수와의 연결을 준다. 모듈 안에서 `count`가 바뀌면 import한 쪽에서도 바뀐 값이 보인다(단, import한 쪽에서 재할당은 불가능한 읽기 전용 뷰다).

## 차이 ②: 정적인가, 동적인가

CJS의 `require`는 **그냥 함수다.** 조건문 안에서도, 변수로 만든 경로로도 호출할 수 있다 — 즉 **코드를 실행해 봐야** 무엇을 가져오는지 안다(동적). 반면 ESM의 `import`/`export`는 함수가 아니라 **문(statement)이다.** 모듈 최상위에만 쓸 수 있고 경로는 문자열 리터럴이어야 한다.

```javascript
// CJS — 된다 (실행해야 안다)
if (isDev) {
  const debug = require('./debug-' + name);
}

// ESM — SyntaxError (import 문은 최상위에만)
if (isDev) {
  import debug from './debug.js';
}
```

불편해 보이는 이 제약이 ESM의 핵심 설계다. 덕분에 엔진과 도구는 **코드를 실행하지 않고 파싱만으로** 모듈 의존 그래프 전체를 그릴 수 있다 — [호이스팅 글](/javascript/04-hoisting)의 "평가 단계" 관점이 파일 단위로 확장된 것이다. 이 정적 구조가 무엇을 가능하게 하는지(트리 셰이킹)는 다음 글의 주제다. 참고로 동적 로딩이 정말 필요할 때를 위해 ESM에도 `import()` 함수(동적 임포트, 프로미스 반환)가 따로 있다.

## 차이 ③: 브라우저에서의 대접

브라우저에서 ESM은 `type="module"` 하나로 켠다.

```html
<script type="module" src="app.mjs"></script>
```

이 한 줄에 지금까지 글들의 답이 몰려 있다. 모듈 스크립트는 **파일마다 독립 스코프**를 가진다 — 도입부의 전역 공유 문제가 언어 차원에서 해결된다. 내부는 [항상 strict mode](/javascript/10-arrow-function-this)다. 그리고 [script 로딩 글](/browser/03-script-loading)에서 예고했듯 **기본 동작이 defer**라서 붙일 필요조차 없다. 파일 = 스코프 = 모듈이라는, 처음부터 그랬어야 할 등식이 성립하는 것이다.

Node.js는 두 시스템이 공존하는 세계라 구분자가 필요하다 — `.mjs` 확장자 또는 `package.json`의 `"type": "module"`이 ESM 선언이고, 오래된 생태계의 CJS 패키지들과의 상호 운용이 아직도 현실 이슈로 남아 있다.

---

모듈의 본질은 **파일을 스코프로 만드는 것**이고, ESM이 CJS와 결정적으로 다른 점은 **정적**이라는 것이다 — 실행 전에 무엇을 주고받는지 전부 드러난다.

그런데 이상하다. 브라우저가 ESM을 네이티브로 지원한다면, 우리는 왜 아직도 Vite나 웹팩 같은 도구로 코드를 합치고 변환해서 배포할까? 시리즈의 마지막 질문이다. → [번들러는 왜 여전히 쓰나](/javascript/23-bundler-babel)
