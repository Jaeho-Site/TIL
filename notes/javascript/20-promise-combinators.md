---
title: Promise.all은 언제 쓰나
description: await 남발이 느린 이유, 순차 vs 병렬 — 그리고 all, allSettled, race, any의 용도 구분
---

# Promise.all은 언제 쓰나

[지난 글](/javascript/19-async-await) 끝에서 예고한 함정부터. 각각 1초 걸리는 독립적인 요청 세 개를 이렇게 썼다.

```javascript
async function loadDashboard() {
  const user = await fetchUser();       // 1초
  const posts = await fetchPosts();     // 1초
  const weather = await fetchWeather(); // 1초
  return { user, posts, weather };
}
// 총 몇 초 걸릴까?
```

**3초**다. 세 요청은 서로의 결과가 전혀 필요 없는데도, `await`이 각 요청의 완료까지 함수를 일시정지시키므로 앞이 끝나야 뒤가 **시작**된다. 자연스럽게 읽히는 코드가 자연스럽게 느린 코드가 되는, async/await의 대표적인 부작용이다.

## 프로미스는 만드는 순간 이미 달리고 있다

해법의 열쇠는 [프로미스 글](/javascript/18-promise)에서 본 성질에 있다. 프로미스는 **생성되는 순간 비동기 처리를 시작한다.** await은 "시작" 버튼이 아니라 "결과 기다리기"일 뿐이다. 그러니 시작을 먼저 다 시켜놓고, 기다리는 것은 나중에 몰아서 하면 된다.

```javascript
async function loadDashboard() {
  const userP = fetchUser();       // 셋 다 지금 출발
  const postsP = fetchPosts();
  const weatherP = fetchWeather();

  return {
    user: await userP,             // 이미 달리는 중인 것을 기다리기만
    posts: await postsP,
    weather: await weatherP
  };
}
```

이 "여러 프로미스를 모아서 기다리기"를 표준 메서드로 만든 것이 `Promise.all`이다.

```javascript
const [user, posts, weather] = await Promise.all([
  fetchUser(), fetchPosts(), fetchWeather()
]); // 약 1초 — 제일 느린 것만큼만 걸린다
```

<svg viewBox="0 0 680 250" role="img" aria-label="await 연쇄는 세 요청이 순차로 3초 걸리고, Promise.all은 동시에 출발해 1초 걸리는 타임라인 비교" style="max-width:680px;width:100%;height:auto;margin:16px 0">
<text x="20" y="56" class="pl-c">await 연쇄</text>
<rect x="140" y="42" width="160" height="20" rx="4" class="pl-bar"/>
<text x="220" y="57" text-anchor="middle" class="pl-in">user</text>
<rect x="300" y="42" width="160" height="20" rx="4" class="pl-bar"/>
<text x="380" y="57" text-anchor="middle" class="pl-in">posts</text>
<rect x="460" y="42" width="160" height="20" rx="4" class="pl-bar"/>
<text x="540" y="57" text-anchor="middle" class="pl-in">weather</text>
<text x="628" y="57" class="pl-dim">3초</text>
<text x="140" y="92" class="pl-dim">앞이 끝나야 뒤가 출발한다</text>
<text x="20" y="150" class="pl-c">Promise.all</text>
<rect x="140" y="136" width="160" height="20" rx="4" class="pl-ok"/>
<text x="220" y="151" text-anchor="middle" class="pl-in">user</text>
<rect x="140" y="162" width="160" height="20" rx="4" class="pl-ok"/>
<text x="220" y="177" text-anchor="middle" class="pl-in">posts</text>
<rect x="140" y="188" width="160" height="20" rx="4" class="pl-ok"/>
<text x="220" y="203" text-anchor="middle" class="pl-in">weather</text>
<text x="308" y="177" class="pl-dim">1초 — 제일 느린 것만큼만</text>
<text x="140" y="238" class="pl-dim">셋이 동시에 출발한다 — 순서는 await이 아니라 의존 관계가 정해야 한다</text>
</svg>

기준은 명확하다. **뒤 요청이 앞 결과를 필요로 하면 await 연쇄(순차), 서로 독립이면 Promise.all(병렬).** 순서를 정하는 건 문법 편의가 아니라 데이터 의존 관계여야 한다.

## all의 성격: 전부 아니면 실패

`Promise.all`은 성격이 급하다. 배열의 프로미스가 **모두 fulfilled되면** 결과 배열(순서 보존)로 fulfilled되지만, **하나라도 reject되는 순간** 나머지를 기다리지 않고 즉시 그 에러로 reject된다.

```javascript
Promise.all([
  new Promise((_, reject) => setTimeout(() => reject(new Error('Error 1')), 3000)),
  new Promise((_, reject) => setTimeout(() => reject(new Error('Error 2')), 2000)),
  new Promise((_, reject) => setTimeout(() => reject(new Error('Error 3')), 1000))
]).catch(console.log); // Error: Error 3 — 가장 먼저 실패한 것
```

"전부 있어야 화면을 그릴 수 있다"면 맞는 성격이다. 하지만 "위젯 셋 중 하나 실패해도 나머지는 보여주고 싶다"면 곤란하다 — 그럴 때가 `allSettled`다. 성공이든 실패든 **전원의 결과**를 기다렸다가 `{status, value}` 또는 `{status, reason}` 객체 배열로 준다.

```javascript
const results = await Promise.allSettled([fetchA(), fetchB(), fetchC()]);
// [{status: 'fulfilled', value: …}, {status: 'rejected', reason: …}, …]
```

나머지 둘은 "여럿 중 하나"를 고르는 도구다. `race`는 성공이든 실패든 **가장 먼저 settled된 것** 하나를 취한다 — 요청에 시간제한을 거는 고전 패턴이 이걸로 만들어진다.

```javascript
const timeout = ms =>
  new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), ms));

const data = await Promise.race([fetchData(), timeout(5000)]);
```

`any`는 race의 낙관적인 버전으로, **가장 먼저 fulfilled된 것**을 취하고 실패는 무시한다(전원이 실패하면 그때 `AggregateError`). 미러 서버 여러 곳에 요청해 먼저 오는 응답을 쓰는 식의 용도다.

| 메서드 | 끝나는 시점 | 결과 | 용도 한 줄 |
|---|---|---|---|
| `all` | 전원 성공 or 첫 실패 | 값 배열 / 첫 에러 | 전부 있어야 한다 |
| `allSettled` | 전원 settled | 상태 객체 배열 | 각자 독립, 결과는 전부 |
| `race` | 첫 settled | 그 값 or 그 에러 | 시간제한, 먼저 온 것 |
| `any` | 첫 성공 or 전원 실패 | 그 값 / AggregateError | 하나만 성공하면 된다 |

마지막으로 심화 포인트 하나. `all`이 첫 실패로 reject돼도 **나머지 프로미스가 취소되는 것은 아니다.** 프로미스에는 취소 개념이 없어서, 결과만 무시될 뿐 뒤에서 요청은 끝까지 실행된다. 진짜 중단이 필요하면 `AbortController` 같은 별도 메커니즘을 붙여야 한다.

---

**await은 순서가 필요할 때만, 독립적인 작업은 시작부터 병렬로.** 4형제의 구분은 "언제 끝난 걸로 칠 것인가(전부/전부의 결과/최초/최초의 성공)"의 구분이다.

그런데 `Promise.all(ids.map(id => fetchUser(id)))`처럼 쓰다 보면, 함수를 배열에 담고 map으로 변환하고 인자로 넘기는 게 너무 자연스러워서 잊게 된다 — 함수를 이렇게 값처럼 다룰 수 있다는 것 자체가 자바스크립트의 특징이라는 걸. 함수가 "일급 객체"라는 말의 의미는 [함수 글](/javascript/14-first-class-function)에서 다룬다.

<style>
.pl-c{font:600 13px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.pl-in{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-1)}
.pl-dim{font:12px var(--vp-font-family-base);fill:var(--vp-c-text-3)}
.pl-bar{fill:var(--vp-c-default-soft);stroke:var(--vp-c-divider)}
.pl-ok{fill:var(--vp-c-green-soft);stroke:var(--vp-c-green-1)}
</style>
