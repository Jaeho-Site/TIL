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

## type만 할 수 있는 것 — 타입 연산

`interface`는 이름 그대로 객체의 형태 서술이 전부다. 반면 `type`은 **임의의 타입에 이름을 붙이는** 도구라서, [값의 집합](/typescript/05-types-as-sets)에 대한 연산 결과도 담을 수 있다.

```typescript
type AorB = 'a' | 'b';                    // 유니온
type Pair = [a: number, b: number];       // 이름 붙은 튜플
type NamedNums = [string, ...number[]];   // 가변 튜플
```

유니온 타입, 튜플(엄밀히는 `{ 0: number; 1: number; length: 2 }`식 흉내는 가능하지만 튜플 문법과 기능을 잃는다), 그리고 나중에 다룰 매핑·조건부 타입은 `interface`로 표현할 수 없다. 타입 설계가 유니온 중심으로 갈수록(다음 글이 정확히 그 이야기다) `type`이 자주 나오는 이유다.

## interface만 할 수 있는 것 — 선언 병합

도입 퀴즈의 정체가 `interface`의 고유 능력, **선언 병합**(declaration merging)이다. 같은 이름의 인터페이스 선언들은 에러가 아니라 하나로 합쳐진다.

처음엔 "누가 이런 걸 원하지?"였는데, 알고 보니 타입스크립트 생태계가 이 기능 위에 서 있었다. 자바스크립트 표준 라이브러리의 타입(`lib.es5.d.ts`, `lib.es2015.core.d.ts`...)이 대표 사례다 — `Array` 인터페이스는 `lib.es5.d.ts`에 한 번, `lib.es2015.core.d.ts`에서 `find` 같은 새 메서드와 함께 또 한 번 선언되고, 프로젝트의 `target` 설정에 따라 필요한 선언들이 병합돼 최종 `Array`가 만들어진다. 사용자 쪽에서도 라이브러리가 제공한 인터페이스에 속성을 추가(모듈 보강)할 때 쓴다. 반대로 이런 "열려 있음"이 싫다면 — 내가 정의한 타입이 어디선가 몰래 확장되는 걸 막고 싶다면 — `type`을 쓰는 게 봉인이 된다.

## 헷갈리면 에러가 나는 쪽이 낫다

실전에서 겪을 만한 차이가 하나 더 있다. **모순된 확장에 대한 반응**이다.

```typescript
interface Person {
  name: string;
  age: string;
}

type TPerson = Person & { age: number }; // 에러 없음. 그러나...
// age: string & number = never — 사용 불가능한 타입이 조용히 만들어진다

interface IPerson extends Person {
  age: number;
  // ~~~ Interface 'IPerson' incorrectly extends interface 'Person'.
  //     Types of property 'age' are incompatible.
}
```

`&`는 집합 연산이라 모순을 만나도 성실하게 교집합(`never`)을 계산할 뿐 에러를 내지 않는다. `extends`는 부분집합 선언이라 모순을 즉시 잡아준다. 잘못을 정의 지점에서 알려주는 쪽이 낫다 — 객체 타입의 확장이라면 `extends`에 점수를 주게 되는 대목이다.

## 그래서 결론은

책의 조언은 담백했다. **확립된 스타일이 있으면 그걸 따르고, 없으면 객체 타입에는 interface를 기본으로.** 에러 메시지가 더 친절하고(인라인으로 풀어헤쳐지지 않고 이름이 유지된다), extends가 모순을 잡아주고, 병합이 필요한 생태계 관례와도 맞는다. 유니온·튜플·타입 연산이 필요해지면 그때 `type`을 쓰면 된다.

개인적으로는 "뭘 쓰든 큰일 나지 않지만, 한 코드베이스 안에서 오락가락하는 게 제일 나쁘다"가 진짜 결론이라고 생각한다. 이 논쟁으로 팀 시간을 태우는 것보다 린트 규칙 하나로 통일하는 게 낫다.

---

`type`과 `interface`는 겹치는 영역이 80%인 두 도구고, 갈리는 20%는 **type의 타입 연산 vs interface의 선언 병합·엄격한 확장**이다. 그런데 도구를 고르는 것보다 훨씬 중요한 질문이 남아 있다. 그 타입이 **표현하면 안 되는 상태까지 표현하고 있지는 않은가**다. → [잘못된 상태를 표현할 수 없게 만들기](/typescript/14-discriminated-union)
