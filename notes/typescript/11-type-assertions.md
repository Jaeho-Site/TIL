---
title: as는 언제 써야 하는가
description: 단언 vs 선언 — 검사를 끄는 문법의 정당한 사용처와 봉인하는 방법
---

# as는 언제 써야 하는가

[지난 글](/typescript/10-any-unknown-never)에서 unknown을 좁히는 정석을 봤지만, 현실의 코드에는 `as`가 널려 있다. 그런데 `as`가 정확히 뭘 하는 건지 시험해보다가 당황한 비교가 있다.

```typescript
interface Person {
  name: string;
}

const alice: Person = {};
//    ~~~~~ Property 'name' is missing in type '{}'
//          but required in type 'Person'

const bob = {} as Person; // 에러 없음
```

같은 빈 객체다. 선언(`: Person`)은 잡아주는데 단언(`as Person`)은 통과시킨다. `bob.name`을 읽는 순간 `undefined`인데도.

## 선언은 검사, 단언은 선언(宣言)

콜론과 `as`는 하는 일이 다르다. **타입 선언**(`: Person`)은 "이 값이 그 타입에 맞는지 검사해라"는 요청이다. 값이 조건을 만족하는지 할당 가능성 검사가 돌고, [잉여 속성 검사](/typescript/04-excess-property-checking)도 발동한다.

**타입 단언**(`as Person`)은 "검사하지 말고 내 말을 믿어라"다. 컴파일러는 두 타입이 아예 무관하지 않은 한(겹치는 부분이 있는 한) 순순히 믿어준다. `{}`는 `Person`의 상위집합 격이라 통과, 오타 속성이 있어도 통과다. `any`가 스위치라면 `as`는 국소 스위치다 — 그 표현식 한 곳의 검사를 끈다.

그래서 기본값은 명확하다. **선언이 가능한 자리면 선언을 쓴다.** 콜백 안이라 선언 자리가 애매하면 화살표 함수의 반환 타입 표기를 쓰면 된다.

```typescript
const people = ['alice', 'bob', 'jan'].map(
  (name): Person => ({ name })
); // Person[] — 검사 받으면서 타입도 붙는다
```

## 그럼에도 단언이 정당한 순간

단언이 존재하는 이유는 하나다. **컴파일러가 모르는 정보를 내가 알고 있을 때.** 대표적인 무대가 DOM이다.

```typescript
document.querySelector('#myButton')?.addEventListener('click', (e) => {
  e.currentTarget;
  // ^? (property) Event.currentTarget: EventTarget | null
  const button = e.currentTarget as HTMLButtonElement;
});
```

컴파일러가 보는 건 "어떤 이벤트의 currentTarget"뿐이지만, 나는 이 리스너가 `#myButton`에 달렸고 그게 버튼 엘리먼트라는 걸 안다. 이 정보는 코드 바깥(HTML)에 있어서 컴파일러가 영원히 알 수 없다. 이럴 때의 단언은 거짓말이 아니라 **컴파일러가 접근 못 하는 사실의 전달**이다.

null이 아니라는 확신만 전달하는 축약형도 있다. 접미사 `!` — non-null 단언이다.

```typescript
const el = document.getElementById('foo')!;
//    ^? const el: HTMLElement — null 가능성이 지워졌다
```

단언은 단언이다. 근거 없이 쓰면 `null.addEventListener`가 런타임에 터진다. 확신이 없다면 `?.`나 if 체크로 [좁히는](/typescript/08-narrowing) 게 맞고, 확신이 있다면 **왜 확신하는지 주석으로 근거를 남기는** 게 책의 조언이다. 미래의 내가 그 HTML을 바꿀 수도 있으니까.

## 단언을 쓰되, 새어 나가지 않게

단언이 불가피할 때도 요령이 있다. 핵심은 **오염 범위를 최소로** 잡는 것이다.

```typescript
function eatDinner1() {
  const pizza: any = getPizza(); // 이러지 말 것
  eatSalad(pizza);               // 통과 (의도)
  pizza.slice();                 // 이 호출도 검사망 밖 (의도 아님!)
}

function eatDinner2() {
  const pizza = getPizza();
  eatSalad(pizza as any);        // 이 인자 하나만 끈다
  pizza.slice();                 // 여전히 검사받는다
}
```

변수 전체에 `any`를 붙이면 그 변수의 남은 생애 전부가 검사망을 벗어난다. 표현식 하나에만 붙이면 오염이 그 자리에서 끝난다.

한 단계 더 나아간 패턴이 **잘 타입된 함수 안에 단언을 숨기는** 것이다. 예를 들어 API 응답을 가져오는 함수에서 `unknown`을 도메인 타입으로 바꿔야 한다면, 단언을 호출부마다 흩뿌리지 않고 시그니처가 정확한 함수 하나에 가둔다.

```typescript
async function fetchPeak(peakId: string): Promise<MountainPeak> {
  return checkedFetchJSON(
    `/api/mountain-peaks/${peakId}`
  ) as Promise<MountainPeak>; // 단언은 이 한 곳뿐
}
```

바깥에서 보면 `fetchPeak`은 완전히 타입 안전한 함수다. 위험한 가정("이 API는 MountainPeak을 준다")은 한 곳에 모여 있고, 주석과 테스트로 그 한 곳만 지키면 된다. 사실 [두 번째 글](/typescript/02-runtime-types)에서 본 Zod 같은 런타임 검증이 더 안전한 정답이지만, 검증 비용을 쓰지 않기로 **선택**했다면 최소한 이렇게 가둬야 한다.

---

`as`는 컴파일러와 나 사이의 책임 이전 계약이다 — **컴파일러가 알 수 없는 사실을 내가 보증하는 문서**고, 보증인이 됐으면 근거(주석)와 담보(좁은 범위, 테스트)를 남겨야 한다. 그런데 단언을 한 번도 안 썼는데도 타입과 런타임이 어긋나는 경우가 있다는 게 더 찜찜했다. 첫 글의 `names[2]`가 그랬다. → [타입 체크를 통과했는데 왜 런타임 에러가 나는가](/typescript/12-unsoundness)
