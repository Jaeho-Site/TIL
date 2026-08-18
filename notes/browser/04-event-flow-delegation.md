---
title: 이벤트 위임은 왜 쓰는가
description: 이벤트는 문서를 여행한다 — 캡처링과 버블링, target vs currentTarget, passive까지
---

# 이벤트 위임은 왜 쓰는가

아래 코드를 보자.

```html
<ul id="fruits">
  <li id="apple">Apple</li>
  <li id="banana">Banana</li>
</ul>
<script>
  document.getElementById('fruits').addEventListener('click', () => {
    console.log('ul에서 클릭을 잡았다');
  });
</script>
```

나는 `li#apple`을 클릭했는데, `ul`에 달아둔 핸들러가 실행된다. 클릭한 요소와 핸들러가 붙은 요소가 다른데 왜 잡힐까? 처음엔 편리한 버그 같았는데, 사실 이건 이벤트 시스템의 핵심 설계였다.

## 이벤트는 타깃에서만 발생하지 않는다

클릭 이벤트가 발생하면 브라우저는 이벤트 객체를 만들어 **문서 꼭대기부터 타깃까지 내려보냈다가, 다시 꼭대기로 올려보낸다.** 세 단계다.

<svg viewBox="0 0 680 300" role="img" aria-label="이벤트가 window에서 타깃까지 내려가는 캡처링 단계, 타깃 단계, 다시 올라가는 버블링 단계를 보여주는 다이어그램" style="max-width:680px;width:100%;height:auto;margin:16px 0">
<defs><marker id="ef-ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--vp-c-brand-1)"/></marker></defs>
<rect x="270" y="24" width="140" height="36" rx="7" class="ef-box"/>
<text x="340" y="47" text-anchor="middle" class="ef-c">window</text>
<rect x="270" y="84" width="140" height="36" rx="7" class="ef-box"/>
<text x="340" y="107" text-anchor="middle" class="ef-c">document</text>
<rect x="270" y="144" width="140" height="36" rx="7" class="ef-box"/>
<text x="340" y="167" text-anchor="middle" class="ef-c">ul#fruits</text>
<rect x="270" y="204" width="140" height="36" rx="7" class="ef-live"/>
<text x="340" y="227" text-anchor="middle" class="ef-c">li#apple</text>
<text x="426" y="227" class="ef-hl">② 타깃 단계</text>
<path d="M225,40 L225,214" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#ef-ah)"/>
<text x="205" y="130" text-anchor="end" class="ef-hl">① 캡처링</text>
<text x="205" y="148" text-anchor="end" class="ef-dim">위에서 타깃으로</text>
<path d="M455,214 L455,40" fill="none" stroke="var(--vp-c-brand-1)" stroke-width="2" marker-end="url(#ef-ah)"/>
<text x="475" y="130" class="ef-hl">③ 버블링</text>
<text x="475" y="148" class="ef-dim">타깃에서 다시 위로</text>
<text x="20" y="284" class="ef-dim">핸들러는 기본적으로 ③에서 실행된다 — addEventListener 3번째 인자(capture: true)로 ①에서 잡을 수도 있다</text>
</svg>

1. **캡처링(capturing)** — 이벤트가 `window`에서 출발해 타깃을 향해 내려온다.
2. **타깃(target)** — 타깃에 도착한다.
3. **버블링(bubbling)** — 물거품 올라오듯 다시 `window`까지 올라간다.

`addEventListener`의 핸들러는 기본적으로 **버블링 단계**에서 실행된다. 그래서 `li`에서 발생한 클릭이 올라오는 길목의 `ul` 핸들러에 잡힌 것이다. 캡처링 단계에서 잡고 싶으면 3번째 인자로 `true`(또는 `{ capture: true }`)를 주면 되는데, 실전에서 쓸 일은 드물고 "3번째 인자가 그거였구나" 정도면 충분하다.

이 구조에서 헷갈리기 쉬운 두 이름을 정확히 갈라두자.

- **`event.target`** — 이벤트를 **발생시킨** 요소. 위 예제에서 `li#apple`.
- **`event.currentTarget`** — 지금 실행 중인 **핸들러가 붙은** 요소. 위 예제에서 `ul#fruits`(핸들러 안의 `this`와 같다).

타깃 자신에 단 핸들러에서는 둘이 같지만, 전파를 타고 잡은 핸들러에서는 달라진다. 이 구분이 다음 주제의 전부다.

## 위임: 버블링을 역이용하기

li가 100개인 리스트에 클릭 핸들러를 달아야 한다면? 순진한 방법은 100개 각각에 등록하는 것이다. 함수 100개가 등록되고([메모리를 붙드는 건 클로저 글에서 본 그대로](/javascript/08-closure-in-practice)), 더 큰 문제는 **나중에 추가된 li에는 핸들러가 없다**는 것이다 — 동적 리스트에서 "새로 추가한 아이템만 클릭이 안 돼요"라는 버그의 정체다.

**이벤트 위임**(event delegation)은 버블링을 역이용한다. 어차피 모든 li의 이벤트는 ul을 지나 올라오니까, **상위 요소 하나에만 등록하고 target으로 걸러낸다.**

```javascript
const $fruits = document.getElementById('fruits');

$fruits.addEventListener('click', ({ target }) => {
  // ul 자신이나 무관한 요소의 클릭은 무시한다
  if (!target.matches('#fruits > li')) return;

  console.log(`${target.id} 클릭됨`);
});
```

등록은 한 번, 나중에 추가된 li도 자동으로 처리된다(이벤트는 어차피 버블링으로 올라오니까). 필터로 `target.matches`를 쓰는 것까지가 관용구다.

## 위임을 둘러싼 두 가지 "막기"

이름이 비슷해서 자주 섞이는 두 메서드는 막는 대상이 다르다.

- **`stopPropagation()`** — **전파**를 막는다. 이벤트가 더 위로 올라가지 않는다. 위임 입장에서는 위험한 도구다 — 중간의 어떤 요소가 이걸 호출하면 상위의 위임 핸들러는 그 이벤트를 영영 못 본다. "위임으로 짠 코드베이스에서 stopPropagation은 신중하게"라는 조언이 여기서 나온다.
- **`preventDefault()`** — **기본 동작**을 막는다. 링크의 페이지 이동, 폼의 제출 같은 브라우저 내장 동작이 취소될 뿐, 전파는 계속된다. 둘은 독립적이다.

전파도 기본 동작도 아닌, 세 번째 옵션도 하나 있다. `addEventListener(type, fn, { passive: true })`는 "이 핸들러는 preventDefault를 호출하지 않겠다"는 **약속**이다. 스크롤 계열 이벤트(`touchmove`, `wheel`)에서 중요한데 — 브라우저는 핸들러가 스크롤을 preventDefault로 막을지 모르니 [핸들러 실행이 끝날 때까지 스크롤(렌더링)을 보류](/browser/01-rendering-pipeline)해야 한다. passive 약속이 있으면 기다릴 필요 없이 즉시 스크롤한다. 최신 브라우저들이 `touchstart`/`touchmove`를 문서 레벨에서 기본 passive로 바꾼 이유이기도 하다.

## React의 onClick도 사실 위임이다

React에서 `<button onClick={...}>`을 쓸 때, React는 그 버튼에 리스너를 붙이지 않는다. **루트 컨테이너에 이벤트 종류별 리스너만 등록해 두고**(React 17부터 루트, 이전엔 document), 버블링으로 올라온 이벤트를 받아 어느 컴포넌트의 핸들러를 실행할지 스스로 라우팅한다 — 지금까지 본 위임 그 자체다. 핸들러가 받는 `e`가 네이티브 이벤트가 아니라 브라우저 차이를 감싼 합성 이벤트(SyntheticEvent)인 것도 이 구조 덕분에 가능하다. 수천 개 컴포넌트에 onClick을 써도 실제 리스너는 몇 개뿐인 이유다.

---

이벤트 위임은 트릭이 아니라 **이벤트가 원래 흐르는 길(버블링)을 그대로 이용하는 것**이다. 흐름 3단계와 target/currentTarget 구분만 정확하면, 위임도 stopPropagation의 부작용도 React의 구조도 전부 같은 그림 안에서 설명된다.

다음은 browser 마지막 글이다. 이벤트를 달 요소를 찾을 때 쓰는 `getElementsByClassName`과 `querySelectorAll` — 결과가 똑같아 보이는 이 둘의 차이 때문에, 멀쩡해 보이는 반복문이 요소를 절반만 바꾸는 사고가 난다. → [DOM 컬렉션의 함정: live와 non-live](/browser/05-dom-essentials)

<style>
.ef-c{font:600 13px var(--vp-font-family-mono);fill:var(--vp-c-text-1)}
.ef-dim{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.ef-hl{font:600 12.5px var(--vp-font-family-base);fill:var(--vp-c-brand-1)}
.ef-box{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-divider)}
.ef-live{fill:var(--vp-c-bg-soft);stroke:var(--vp-c-brand-1);stroke-width:1.5}
</style>
