---
title: type과 interface, 뭘 써야 하나
description: 같은 것 80%, 다른 것 20% — 유니온·튜플 vs 선언 병합, 그리고 선택 기준
---

# type과 interface, 뭘 써야 하나

객체 타입을 정의하는 방법이 둘이라는 건 처음부터 알았지만, 뭐가 다른지는 계속 미뤄뒀다. 대부분의 경우 뭘 써도 됐기 때문이다. 그러다 이 코드를 만나고 미룬 빚을 갚게 됐다.

```typescript
interface IState {
  name: string;
  capital: string;
}
interface IState {
  population: number;
}
```

같은 이름의 인터페이스를 두 번 선언했다. 당연히 "중복 선언" 에러를 예상했는데, 컴파일러는 조용하다. 심지어 이게 된다.

```typescript
const wyoming: IState = {
  name: 'Wyoming',
  capital: 'Cheyenne',
  population: 578_000,
}; // 통과 — 두 선언이 합쳐진 IState
```

`type`으로 같은 걸 하면 즉시 `Duplicate identifier` 에러다. 이 차이의 정체가 두 도구를 가르는 열쇠였다.

## 먼저, 같은 것부터 — 생각보다 많다

객체 타입, 인덱스 시그니처, 함수 타입, 제네릭 — 전부 양쪽 다 표현할 수 있다.

```typescript
type TFn = (x: number) => string;
interface IFn {
  (x: number): string; // 호출 시그니처 문법만 다를 뿐 같은 타입
}
```

확장도 서로 넘나든다. `interface`가 `type`을 `extends`할 수 있고, `type`은 `&`로 `interface`를 합칠 수 있고, 클래스는 둘 다 `implements`할 수 있다.

```typescript
type TState = { name: string; capital: string };
interface IStateWithPop extends TState {
  population: number;
}
class StateT implements TState {
  name = '';
  capital = '';
}
```

그래서 "객체 타입 하나 정의한다"의 관점에서는 정말 아무거나 써도 된다. 차이는 가장자리에 있다.
