---
title: 잘못된 상태를 표현할 수 없게 만들기
description: 태그된 유니온 — 무효 상태 제거, 인터페이스의 유니온, never 완전성 검사
---

# 잘못된 상태를 표현할 수 없게 만들기

[지난 글](/typescript/13-type-vs-interface) 끝에서 도구보다 중요하다고 한 질문이 이거다. 페이지 로딩 화면의 상태 타입을 이렇게 설계했다고 하자. 컴파일 에러 없이 잘 돌아가는 타입이다. 퀴즈: 이 타입에는 무슨 문제가 있을까?

```typescript
interface State {
  pageText: string;
  isLoading: boolean;
  error?: string;
}
```

나는 한동안 문제를 못 찾았다. 필요한 정보가 다 있지 않나? 힌트는 "이 타입으로 표현할 수 있는 값 중, 현실에 존재하면 안 되는 값이 있는가"다.

```typescript
const wat: State = {
  pageText: '이전 페이지 내용',
  isLoading: true,
  error: '404 Not Found',
}; // 로딩 중인데 에러? 에러인데 본문도 있음?
```

**로딩 중이면서 동시에 에러인 상태**가 타입 위에서는 멀쩡히 존재한다. 렌더링 함수는 이 모순을 마주하면 뭘 그려야 할지 알 수 없고, 결국 `if (state.error) ... else if (state.isLoading) ...` 같은 우선순위 규칙을 임의로 정하게 된다. 그 규칙이 코드마다 다르면 버그다. 타입 체커는 아무것도 도와줄 수 없다 — **타입이 무효 상태를 유효하다고 선언해버렸으니까.**

## 상태는 열거하는 것이다

발상을 바꿔서, 속성들의 조합이 아니라 **존재할 수 있는 상태 자체를 열거**한다.

```typescript
interface RequestPending {
  state: 'pending';
}
interface RequestError {
  state: 'error';
  error: string;
}
interface RequestSuccess {
  state: 'ok';
  pageText: string;
}
type RequestState = RequestPending | RequestError | RequestSuccess;
```

[두 번째 글](/typescript/02-runtime-types)에서 런타임 타입 확인 수단으로 잠깐 만났던 **태그된 유니온**이다. 이제 "로딩 중이면서 에러"는 표현조차 불가능하다 — `state`는 하나의 값만 가질 수 있으니까. 그리고 에러 메시지는 `error` 상태에만, 본문은 `ok` 상태에만 존재한다. 렌더링 함수에서는 [좁히기](/typescript/08-narrowing)가 전부 알아서 해준다.

```typescript
function renderPage(requestState: RequestState, currentPage: string) {
  switch (requestState.state) {
    case 'pending':
      return `Loading ${currentPage}...`;
    case 'error':
      return `Error! ${requestState.error}`; // 여기서만 error 접근 가능
    case 'ok':
      return `<h1>${currentPage}</h1>\n${requestState.pageText}`;
  }
}
```

우선순위 규칙도, 방어적 undefined 체크도 사라졌다. 무효 상태를 코드에서 처리하는 게 아니라 **타입 설계 단계에서 소멸**시킨 것이다.

![isLoading과 error 속성 조합이 만드는 2x2 상태 공간에는 로딩 중이면서 에러인 무효 칸이 타입상 유효하게 존재하지만, 태그된 유니온 설계에서는 유효한 상태 세 개만 표현 가능한 비교](/images/typescript/14-state-space.png)

## 유니온을 어디에 두느냐가 설계다

같은 원리를 다른 각도에서 보여주는 사례가 "유니온을 품은 인터페이스"다.

```typescript
// 나쁜 쪽: 인터페이스 안에 유니온
interface Layer {
  layout: FillLayout | LineLayout | PointLayout;
  paint: FillPaint | LinePaint | PointPaint;
}

// 좋은 쪽: 인터페이스들의 유니온
interface FillLayer { type: 'fill'; layout: FillLayout; paint: FillPaint; }
interface LineLayer { type: 'line'; layout: LineLayout; paint: LinePaint; }
interface PointLayer { type: 'point'; layout: PointLayout; paint: PointPaint; }
type Layer = FillLayer | LineLayer | PointLayer;
```

위쪽 설계에서는 `FillLayout`에 `LinePaint`를 조합한 잡종 레이어가 유효하다. 속성 사이에 "짝이 맞아야 한다"는 관계가 있는데 타입이 그걸 말하지 못하는 것이다. 아래쪽은 짝이 인터페이스 단위로 묶여 있어 잡종이 원천 봉쇄되고, `type` 태그 하나로 좁히기까지 얻는다. 유효한 조합의 [집합](/typescript/05-types-as-sets)만 정확히 담는 타입이 곧 좋은 타입이다.

## 빠뜨린 케이스는 never가 잡는다

태그된 유니온의 마지막 조각은 [any 글](/typescript/10-any-unknown-never)에서 예고했던 `never`의 쓸모다. 상태가 셋일 때 switch가 셋을 다 처리했는지, 컴파일러에게 감시를 맡길 수 있다.

```typescript
function assertUnreachable(value: never): never {
  throw new Error(`Missed a case! ${value}`);
}

function area(shape: Shape) { // Shape = Box | Circle | Line
  switch (shape.type) {
    case 'box': return shape.size[0] * shape.size[1];
    case 'circle': return Math.PI * shape.radius ** 2;
    default:
      return assertUnreachable(shape);
      //                       ~~~~~
      // Argument of type 'Line' is not assignable to parameter of type 'never'.
  }
}
```

모든 케이스를 처리했다면 `default`에 도달할 값은 없고, 좁히기 끝의 `shape`는 공집합 `never`가 되어 조용히 통과한다. `Line` 케이스를 빠뜨린 지금은 `default`의 `shape`가 `Line`으로 남고, `never` 매개변수에 들어갈 수 없어 에러가 난다. 에러 메시지가 **어떤 케이스를 빠뜨렸는지 이름까지 알려주는** 게 백미다. 나중에 누가 유니온에 상태를 추가하면, 그 순간 관련된 모든 switch가 컴파일 에러로 "나 여기 수정해야 해요"라고 손을 든다.

## React에서 매일 하는 실수이기도 하다

사실 도입의 `State`는 React 컴포넌트에서 흔히 보는 모양 그대로다.

```typescript
const [data, setData] = useState<Page | null>(null);
const [isLoading, setIsLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
```

`useState` 세 개는 곧 "유니온을 품은 인터페이스"와 같은 설계다 — `isLoading && error`가 동시에 참인 순간이 얼마든지 생긴다(에러 후 `setIsLoading(false)`를 깜빡하는 게 단골). 상태 하나로 합쳐 태그된 유니온을 담거나, 이 패턴을 제대로 구현해둔 라이브러리(React Query의 `status`가 정확히 태그다)를 쓰는 게 같은 원리의 실무 버전이다.

---

좋은 타입 설계란 표현력을 늘리는 게 아니라 **유효한 상태의 집합과 타입이 표현하는 집합을 일치시키는 것**이고, 태그된 유니온은 그 일치를 만드는 가장 실용적인 도구다. 그런데 무효 상태의 단골 원인이 하나 남아 있다 — 어디에나 스며드는 `null`이다. → [null은 타입의 어디에 둬야 하나](/typescript/15-null-handling)
