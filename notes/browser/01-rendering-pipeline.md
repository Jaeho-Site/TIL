---
title: HTML이 화면이 되기까지 무슨 일이 일어나나
description: DOM, CSSOM, 렌더 트리, 레이아웃, 페인트 — 렌더링 파이프라인 5단계
---

# HTML이 화면이 되기까지 무슨 일이 일어나나

[이벤트 루프 글](/javascript/17-micro-macro-task)을 쓰면서 "렌더링 기회"라는 말을 썼는데, 문득 그 "렌더링"을 남에게 정확히 뭘 하는 건지 논리적으로 설명 못 하는 나를 발견했다. 브라우저가 HTML 문자열을 받아서 픽셀로 바꾸기까지 그 사이에 무슨 일이 있는 걸까를 정리해보자.

## 파이프라인: 두 갈래로 파싱하고, 합쳐서, 그린다

브라우저의 렌더링 엔진은 정해진 순서의 파이프라인으로 움직인다.

<svg viewBox="0 0 680 310" role="img" aria-label="HTML과 CSS가 각각 DOM과 CSSOM으로 파싱되고, 합쳐져 렌더 트리가 된 뒤 레이아웃, 페인트, 합성을 거치는 파이프라인" style="max-width:680px;width:100%;height:auto;margin:16px 0">
<defs><marker id="rp-ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-brand-1)"/></marker></defs>
<rect x="20" y="36" width="110" height="42" rx="7" class="rp-box"/>
<text x="75" y="62" text-anchor="middle" class="rp-c">HTML</text>
<rect x="200" y="36" width="110" height="42" rx="7" class="rp-box"/>
<text x="255" y="62" text-anchor="middle" class="rp-c">DOM</text>
<rect x="20" y="104" width="110" height="42" rx="7" class="rp-box"/>
<text x="75" y="130" text-anchor="middle" class="rp-c">CSS</text>
<rect x="200" y="104" width="110" height="42" rx="7" class="rp-box"/>
<text x="255" y="130" text-anchor="middle" class="rp-c">CSSOM</text>
<path d="M134,57 L195,57" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#rp-ah)"/>
<path d="M134,125 L195,125" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#rp-ah)"/>
<text x="164" y="47" text-anchor="middle" class="rp-dim">파싱</text>
<rect x="430" y="70" width="130" height="42" rx="7" class="rp-live"/>
<text x="495" y="96" text-anchor="middle" class="rp-c">렌더 트리</text>
<path d="M314,57 C370,57 380,80 425,86" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#rp-ah)"/>
<path d="M314,125 C370,125 380,102 425,96" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#rp-ah)"/>
<text x="525" y="142" class="rp-dim">display:none은 여기서 빠진다</text>
<rect x="20" y="200" width="180" height="46" rx="7" class="rp-box"/>
<text x="110" y="220" text-anchor="middle" class="rp-c">레이아웃 (리플로우)</text>
<text x="110" y="238" text-anchor="middle" class="rp-dim">위치·크기 계산</text>
<rect x="270" y="200" width="150" height="46" rx="7" class="rp-box"/>
<text x="345" y="220" text-anchor="middle" class="rp-c">페인트</text>
<text x="345" y="238" text-anchor="middle" class="rp-dim">픽셀로 그린다</text>
<rect x="490" y="200" width="150" height="46" rx="7" class="rp-box"/>
<text x="565" y="220" text-anchor="middle" class="rp-c">합성</text>
<text x="565" y="238" text-anchor="middle" class="rp-dim">레이어 합치기</text>
<path d="M495,116 C495,160 200,150 130,196" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#rp-ah)"/>
<path d="M204,223 L265,223" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#rp-ah)"/>
<path d="M424,223 L485,223" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#rp-ah)"/>
<text x="20" y="290" class="rp-dim">구조(DOM)와 스타일(CSSOM)을 따로 만들고, 화면에 보일 것만 합쳐서, 재고 → 그리고 → 합친다</text>
</svg>

1. **HTML 파싱 → DOM.** 서버가 준 것은 그냥 바이트 덩어리다. 문자로 디코딩하고, 토큰으로 자르고, 노드로 만들어 트리로 엮은 것이 DOM이다. "HTML을 브라우저가 이해할 수 있는 자료구조로 번역한 것"이 정확한 정의다.
2. **CSS 파싱 → CSSOM.** 파싱 중 `<link>`나 `<style>`을 만나면 CSS도 같은 과정을 거쳐 CSSOM이 된다. 상속과 캐스케이딩이 계산된, 스타일의 트리다.
3. **렌더 트리 = DOM + CSSOM.** 둘을 합치되, **화면에 보이는 것만** 남긴다. `display: none`인 요소는 렌더 트리에서 빠진다 — 반면 `visibility: hidden`은 공간을 차지하므로 트리에 남는다. 두 속성의 차이가 여기서 갈린다.
4. **레이아웃(리플로우).** 렌더 트리의 각 노드가 뷰포트 안에서 정확히 어디에, 어떤 크기로 있어야 하는지 계산한다. `%`나 `vw` 같은 상대값이 절대 픽셀로 확정되는 단계다.
5. **페인트 → 합성.** 계산된 위치에 실제 픽셀을 그리고(페인트), 여러 레이어로 나눠 그렸다면 최종적으로 한 장으로 합친다(합성, composite).

## CSS는 왜 렌더링을 막는가

파이프라인을 보고 나니 예전에 외웠던 규칙 하나가 이해로 바뀌었다. "CSS는 렌더링 차단(render-blocking) 리소스다"라는 말이다.

3단계가 이유다. 렌더 트리를 만들려면 CSSOM이 **완성되어 있어야** 한다. CSS를 절반만 적용해서 일단 그렸다가 나머지가 도착하면 다시 그리는 선택지도 있겠지만, 그러면 사용자는 스타일이 벗겨진 화면이 번쩍이는 걸 보게 된다(FOUC, Flash of Unstyled Content). 그래서 브라우저는 CSSOM이 완성될 때까지 렌더링을 하지 않는 쪽을 택했다. CSS 파일이 크고 느릴수록 첫 화면이 늦게 뜨는 이유이자, 성능 도구들이 "크리티컬 CSS를 인라인하라"고 조언하는 이유다.

그런데 파싱을 막는 게 하나 더 있다. `<script>`는 CSS보다 더 과격하게 — **HTML 파싱 자체를** 멈춰 세운다. 이건 별도 글에서 다룬다.

## 이 파이프라인은 한 번으로 끝나지 않는다

첫 렌더링이 끝난 뒤에도 파이프라인은 계속 다시 돈다. 자바스크립트가 DOM을 바꾸면, 사용자가 창 크기를 바꾸면, 폰트가 늦게 도착하면 — 바뀐 부분부터 다시 계산해서 다시 그린다.

이 "다시 그리기"가 실행되는 타이밍이 바로 [이벤트 루프 글](/javascript/17-micro-macro-task)에서 본 **렌더링 기회**다. 매끄러운 화면은 초당 60번(약 16.7ms 간격) 갱신되어야 하는데, 그 짧은 예산 안에서 자바스크립트 실행과 이 파이프라인이 시간을 나눠 써야 한다. [무거운 동기 코드가 화면을 멈추게 하는 이유](/javascript/16-event-loop)도, 다시 그리는 비용을 줄여야 하는 이유도 전부 이 예산 문제다.

---

렌더링은 마법이 아니라 **번역(DOM·CSSOM) → 선별(렌더 트리) → 계산(레이아웃) → 그리기(페인트·합성)** 파이프라인이다. 각 단계의 이름을 알고 나면 성능 이야기의 절반은 이미 이해한 것이다.

바로 다음 궁금증이 성능의 나머지 절반이다. 무언가 바뀌면 파이프라인의 **어느 단계부터** 다시 도는 걸까? `width`를 바꾸는 것과 `background-color`를 바꾸는 것의 비용이 완전히 다른 이유가 거기 있다. → [reflow와 repaint는 뭐가 다른가](/browser/02-reflow-repaint)

<style>
.rp-c{font:600 13px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.rp-dim{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.rp-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.rp-live{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-brand-1);stroke-width:1.5}
</style>
