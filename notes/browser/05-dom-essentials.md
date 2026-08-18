---
title: DOM 컬렉션의 함정 - live와 non-live
description: 요소를 절반만 바꾸는 반복문의 미스터리 — HTMLCollection vs NodeList, 그리고 innerHTML의 두 가지 문제
---

# DOM 컬렉션의 함정: live와 non-live

멀쩡해 보이는데 버그가 있는 코드로 시작한다. class가 `red`인 li 세 개를 전부 `blue`로 바꾸려고 한다.

```html
<ul>
  <li class="red">Apple</li>
  <li class="red">Banana</li>
  <li class="red">Orange</li>
</ul>
<script>
  const $elems = document.getElementsByClassName('red');
  console.log($elems.length); // 3

  for (let i = 0; i < $elems.length; i++) {
    $elems[i].className = 'blue';
  }

  console.log($elems.length); // ?
</script>
```

전부 blue가 됐을 것 같지만, 실행하면 **Banana가 red로 남는다.** 마지막 length는 `1`이다. 반복문에는 아무 잘못이 없는데 요소를 절반만 바꾸는 이 미스터리의 범인은 `getElementsByClassName`의 반환값이다.

## HTMLCollection은 살아있다

`getElementsBy*` 계열이 반환하는 **HTMLCollection**은 조회 결과의 스냅샷이 아니라, **DOM의 현재 상태를 실시간 반영하는 살아있는(live) 객체**다. 조건은 "class가 red인 요소들"인데, 반복문이 그 조건을 파괴하면서 돌고 있다.

- `i = 0`: Apple을 blue로 → Apple이 조건에서 탈락, **컬렉션에서 실시간으로 빠진다** → 남은 것 `[Banana, Orange]`, Banana가 인덱스 0으로 당겨진다
- `i = 1`: 인덱스 1은 이제 Orange다 → Orange가 blue로 → 남은 것 `[Banana]`
- `i = 2`: `length`(1)보다 크다 → 종료. **Banana는 건너뛰어졌다**

컬렉션을 순회하면서 컬렉션의 소속 조건을 바꾸는 것 — 배열이었다면 안전했을 코드가, live 객체라서 발밑이 움직인 것이다. 우회는 세 가지가 있는데(역방향 순회, length가 남아있는 동안 인덱스 0만 처리하는 while), 개인적으로 답은 하나라고 생각한다. **순회 전에 배열로 변환해서 스냅샷을 만드는 것.**

```javascript
[...$elems].forEach(elem => elem.className = 'blue'); // 전부 blue, 안전하다
```

HTMLCollection은 유사 배열이면서 이터러블이라 스프레드가 통한다 — 이 문장의 정확한 의미는 [이터러블 글](/javascript/21-iterable)에서 다룬다.

## querySelectorAll은 스냅샷이다

같은 조회를 `querySelectorAll`로 하면 **NodeList**가 반환되는데, 이쪽은 **호출 시점의 스냅샷**(non-live)이다. 이후 DOM이 바뀌어도 컬렉션은 그대로라서 위의 사고가 없고, `forEach`도 직접 제공한다.

| 메서드 | 반환 | 성격 |
|---|---|---|
| `getElementById` | 요소 하나 | — |
| `getElementsByTagName` / `ByClassName` | HTMLCollection | **live** |
| `querySelector` / `querySelectorAll` | 요소 하나 / NodeList | non-live (스냅샷) |

단서가 하나 있다. NodeList는 대부분 non-live지만 **`childNodes` 등 일부 API가 반환하는 NodeList는 live**라서, "NodeList = 항상 안전"이라고 외우면 다시 당한다. 그래서 결론은 종류 불문 하나로 수렴한다 — **DOM 컬렉션을 순회하며 DOM을 바꿀 거라면, 먼저 배열로 변환하라.** live 객체는 "지금 몇 개인가"를 실시간으로 물을 때만 그 성질이 장점이 된다.

## innerHTML의 두 가지 문제

DOM 조작에서 하나만 더 정리해 둔다. 제일 편한 도구라서 제일 자주 쓰이는 `innerHTML`에는 값비싼 함정이 둘 있다.

**첫째, XSS(크로스 사이트 스크립팅).** innerHTML은 문자열을 **HTML로 파싱해서 실행 가능한 DOM으로** 만든다. 그 문자열에 사용자 입력이 섞이면, 마크업을 주입할 통로가 열린다.

```javascript
const name = `<img src="x" onerror="alert('털렸다')">`; // 사용자 입력이라면?

$div.innerHTML = `<span>${name}</span>`; // onerror가 실행된다
```

(`<script>` 태그는 innerHTML로 삽입 시 실행되지 않지만, 이렇게 이벤트 핸들러 속성으로 우회하면 실행된다.) 사용자 입력을 화면에 넣을 때의 원칙은 단순하다 — **텍스트는 `textContent`로.** textContent는 파싱 없이 글자 그대로 넣기 때문에 주입 자체가 성립하지 않는다.

**둘째, 다시 만들기 비용.** `$list.innerHTML += '<li>새 항목</li>'`은 "추가"처럼 보이지만 실제로는 **기존 내용 전체를 문자열로 직렬화 → 이어붙이기 → 전부 파괴하고 처음부터 재파싱·재생성**이다. 자식이 많을수록 비용이 커지고([리플로우 글](/browser/02-reflow-repaint)에서 본 그 비용이다), 기존 요소들이 파괴·재생성되면서 걸어뒀던 이벤트 핸들러와 포커스 상태도 함께 사라진다. 위치를 지정해 삽입만 하는 `insertAdjacentHTML('beforeend', ...)`이나 `append` 계열이 이럴 때의 도구다.

---

DOM API의 함정들은 결국 같은 질문으로 정리된다. **"이 객체는 DOM의 스냅샷인가, 실시간 뷰인가"** — 컬렉션이 live인지, innerHTML이 기존 DOM을 살리는지. 스냅샷이 필요하면 배열로, 텍스트는 textContent로, 삽입은 위치 지정으로.

이 글에서 "유사 배열이면서 이터러블"이라고 얼버무린 말에서 스프레드가 되는 것과 안 되는 것의 경계가 정확히 어디인지 궁금하다면 javascript파트의 이터러블 프로토콜에서 다룬다. → [for...of와 for...in은 뭐가 다른가](/javascript/21-iterable)
