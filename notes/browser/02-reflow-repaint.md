---
title: reflow와 repaint는 뭐가 다른가
description: 변경이 파이프라인의 어느 단계로 되돌아가느냐 — 그리고 transform이 싼 이유
---

# reflow와 repaint는 뭐가 다른가

[지난 글](/browser/01-rendering-pipeline)의 파이프라인을 알고 나서 생긴 궁금증이다. 자바스크립트로 `width`를 바꾸는 것과 `background-color`를 바꾸는 것 — 브라우저 입장에서 비용이 같을까?

같지 않다. 그리고 그 차이를 설명하는 열쇠가 지난 글의 마지막 세 단계(레이아웃 → 페인트 → 합성)다. **어떤 변경이냐에 따라, 파이프라인의 다른 지점으로 되돌아간다.**

![width·font-size는 리플로우, color·background는 리페인트, transform·opacity는 합성만 유발하며 왼쪽 단계일수록 비용이 큰 것을 보여주는 다이어그램](/images/browser/02-reflow-repaint-composite.png)

- **리플로우(reflow)** — 기하(위치·크기)에 영향을 주는 변경. `width`, `height`, `margin`, `padding`, `font-size`, 요소 추가/삭제 등. 레이아웃을 다시 계산해야 하고, 그 결과로 페인트와 합성도 따라온다. 게다가 한 요소의 기하가 바뀌면 주변 요소들의 위치도 연쇄적으로 다시 계산되므로 **제일 비싸다.**
- **리페인트(repaint)** — 기하는 그대로고 보이는 모양만 바뀌는 변경. `color`, `background`, `visibility` 등. 레이아웃은 건너뛰고 그리기부터 다시 한다.
- **합성만(composite-only)** — `transform`, `opacity`. 레이아웃도 페인트도 다시 하지 않는다.

## transform은 왜 그렇게 싼가

`left: 100px`로 옮기는 것과 `transform: translateX(100px)`로 옮기는 것은 화면상 결과가 같다. 그런데 전자는 리플로우, 후자는 합성만이다. 왜?

비밀은 **레이어**에 있다. 브라우저는 `transform`이나 `opacity` 애니메이션이 걸린 요소를 별도의 레이어로 분리해 둔다. 레이어는 이미 페인트가 끝난 그림이고, 합성 단계는 그 그림들을 "어디에, 얼마나 투명하게 겹칠까"만 결정한다. 이 조합 작업은 GPU가 잘하는 일이라 메인 스레드의 [렌더링 예산](/browser/01-rendering-pipeline)을 거의 먹지 않는다. 포토샵으로 비유하면, 리플로우는 그림을 다시 그리는 것이고 합성은 이미 그려진 레이어를 드래그해서 옮기는 것이다.

애니메이션을 `left`/`top` 대신 `transform`/`opacity`로 만들라는 조언이 여기서 나온다. `will-change: transform`으로 레이어 분리를 미리 힌트할 수도 있는데, 레이어는 각각 메모리를 먹으므로 남발하면 오히려 손해다.

## 함정 요소: 읽기가 리플로우를 일으킨다

여기까지는 "쓰기" 이야기였다. 그런데 개인적으로 더 놀랐던 건, **레이아웃 값을 읽기만 해도 리플로우가 일어날 수 있다**는 것이다.

```javascript
boxes.forEach((box) => {
  box.style.width = box.offsetWidth + 10 + 'px'; // 읽고, 쓰고, 읽고, 쓰고…
});
```

브라우저는 영리해서 스타일 변경을 바로 반영하지 않고 모아뒀다가 다음 렌더링 타이밍에 한 번에 처리한다. 그런데 `offsetWidth` 같은 기하 값을 읽으면 이야기가 달라진다 — 정확한 값을 돌려주려면 밀려 있던 변경을 **지금 당장** 계산해야 한다(강제 동기 레이아웃). 위 코드는 쓰기와 읽기를 번갈아 하므로 반복마다 리플로우가 터진다. 레이아웃 스래싱(layout thrashing)이라고 부르는 패턴이다.

해법은 읽기와 쓰기를 분리하는 것이다.

```javascript
const widths = boxes.map((box) => box.offsetWidth); // 읽기를 전부 먼저

boxes.forEach((box, i) => {
  box.style.width = widths[i] + 10 + 'px'; // 쓰기는 나중에 몰아서
});
```

읽기 구간에서 리플로우는 최대 한 번, 쓰기는 브라우저가 알아서 배치 처리한다.

## DOM 조작이 비싸다는 말의 실체

"DOM 조작은 비싸다"는 말을 많이 듣는데, 이 글을 정리하면서 복습하니 더 정확하게 말할 수 있게 됐다. 비싼 건 DOM 객체를 바꾸는 일 자체가 아니라 **그 변경이 유발하는 리플로우·리페인트**다. 그래서 최적화의 방향도 "변경 횟수를 줄이는 것"이 아니라 "파이프라인을 다시 돌리는 횟수를 줄이는 것"이 된다 — 변경을 모아서 한 번에 반영하기.

React의 방식도 이 관점에서 보면 명확하다. 상태 변경들을 모아 가상 DOM에서 차이를 계산한 뒤, 실제 DOM에는 **최소한의 변경을 배치로** 적용한다. 프레임워크가 없애준 것은 DOM 조작이 아니라, 무분별하게 흩어진 리플로우다.

---

리플로우와 리페인트의 차이는 **변경이 파이프라인의 어느 단계로 되돌아가느냐**다. 레이아웃까지 가면 리플로우, 페인트까지만 가면 리페인트, 합성에서 끝나면 공짜에 가깝다.

렌더링을 다시 돌게 만드는 요인은 하나 더 남았다. 파이프라인이 시작되기도 전에 HTML 파싱 자체를 멈춰 세우는 존재 — `<script>` 태그다. 옛날부터 "script는 body 끝에 두라"던 국룰의 이유이기도 하다. → [script 태그는 어디에 둬야 하나](/browser/03-script-loading)

<style>
.rr-c{font:600 12.5px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.rr-dim{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.rr-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.rr-hot{fill:var(--vp-c-danger-soft);stroke:var(--vp-c-danger-1)}
.rr-ok{fill:var(--vp-c-green-soft);stroke:var(--vp-c-green-1)}
</style>
