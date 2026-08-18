---
title: Browser
description: 브라우저 렌더링과 이벤트 동작 원리 노트
---

# Browser

브라우저가 HTML을 화면으로 바꾸는 과정과 이벤트 시스템을 정리합니다.

## 질문 지도

```
렌더링 파이프라인 ──→ reflow/repaint ──→ script 로딩(async/defer)
이벤트 흐름(캡처링/버블링) ──→ 이벤트 위임 ──→ (React 합성 이벤트)
```

## 글 목록

### 렌더링

1. [HTML이 화면이 되기까지 무슨 일이 일어나나](/browser/01-rendering-pipeline) — DOM, CSSOM, 렌더 트리, 레이아웃, 페인트
2. [reflow와 repaint는 뭐가 다른가](/browser/02-reflow-repaint) — 유발 속성, transform이 싼 이유, 레이아웃 스래싱
3. [script 태그는 어디에 둬야 하나](/browser/03-script-loading) — 파서 블로킹, async vs defer

### 이벤트와 DOM

4. [이벤트 위임은 왜 쓰는가](/browser/04-event-flow-delegation) — 캡처링/버블링, target vs currentTarget, passive
5. [DOM 컬렉션의 함정: live와 non-live](/browser/05-dom-essentials) — HTMLCollection vs NodeList, innerHTML과 XSS
