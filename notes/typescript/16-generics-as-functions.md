---
title: 제네릭은 타입의 함수다
description: extends 제약은 매개변수의 타입 표기이고, 타입 파라미터에도 황금률이 있다
---

# 제네릭은 타입의 함수다

제네릭 문법 자체는 익숙해진 지 오래인데, 어느 날 이 코드가 컴파일된다는 게 새삼 이상하게 느껴졌다.

```typescript
interface Weight {
  pounds: number;
  ounces: number;
}
declare function parseYAML<T>(input: string): T;

const w: Weight = parseYAML(''); // 통과?!
```

`parseYAML`은 문자열을 받을 뿐인데, 반환값이 `Weight`라는 걸 어떻게 보장한다는 걸까. 보장 못 한다. 그런데도 통과한다. [any를 다룰 때](/typescript/10-any-unknown-never) "반환에만 쓰이는 제네릭은 가짜 안전"이라고 스치듯 언급했는데, 이번에 제네릭을 제대로 정리하면서 그 이유를 끝까지 따라가 봤다.

## 함수의 어휘로 번역하면 전부 설명된다

책이 제안하는 관점은 제목 그대로다. **제네릭 타입은 타입을 받아 타입을 반환하는 함수다.** 이 번역표가 생각보다 정밀하게 작동한다.

| 값의 세계 | 타입의 세계 |
|---|---|
| 함수 `f(x)` | 제네릭 `F<T>` |
| 매개변수 `x` | 타입 파라미터 `T` |
| 매개변수의 타입 표기 `x: number` | 제약 `T extends object` |
| 인자 전달 `f(3)` | 타입 인자 `F<Person>` |
| 인자 추론 (콜백 등) | 제네릭 함수 호출 시 `T` 추론 |

`extends` 제약이 "매개변수의 타입 표기"라는 번역이 특히 마음에 들었다. `function f(x: number)`가 "아무 값이나 받지 않겠다"이듯, `<K extends keyof T>`는 "아무 타입이나 받지 않겠다"다. 제약 없는 타입 파라미터는 타입 표기를 생략한 매개변수와 같은 냄새가 난다.

제약이 실전에서 어떻게 쓰이는지는 객체에서 속성 몇 개를 뽑는 `pick` 함수가 잘 보여준다.

```typescript
interface Person {
  name: string;
  age: number;
}

function pick<T extends object, K extends keyof T>(
  obj: T,
  ...keys: K[]
): Pick<T, K> {
  // ...
}

const p: Person = { name: 'Matilda', age: 5.5 };
const age = pick(p, 'age');
//    ^? const age: Pick<Person, "age">
pick(p, 'address');
//      ~~~~~~~~~ Argument of type '"address"' is not assignable
//                to parameter of type 'keyof Person'.
```

`K extends keyof T`라는 제약 덕분에 두 가지가 공짜로 따라온다. 존재하지 않는 키를 넘기면 에러가 나고, `T`와 `K`는 호출 인자에서 **추론**되어 명시적 타입 인자 없이도 정확한 반환 타입이 나온다. 타입의 함수에 인자를 안 적어도 되는 건, 값의 함수에서 콜백 매개변수 타입을 안 적어도 되던 [문맥 추론](/typescript/09-context-inference)과 같은 원리다.

## 타입 파라미터의 황금률 — 두 번 이상 등장해야 한다

이 관점에서 도입 퀴즈를 해부해 보자. 타입 파라미터의 존재 이유는 **타입들 사이의 관계를 묶는 것**이다. `identity<T>(arg: T): T`에서 `T`는 두 번 등장하며 "입력과 출력이 같은 타입"이라는 관계를 만든다. 관계를 만들려면 당연히 **최소 두 자리에 나타나야 한다.**

```typescript
function third<A, B, C>(a: A, b: B, c: C): C {
  return c;
}
```

`A`와 `B`는 각각 한 번씩만 등장한다. 아무 관계도 안 묶으면서 시그니처만 무겁게 만드는 가짜 파라미터다. 한 번만 등장하는 타입 파라미터는 [unknown](/typescript/10-any-unknown-never)으로 바꿔도 잃는 게 없다.

```typescript
function third<C>(a: unknown, b: unknown, c: C): C {
  return c;
}
```

그리고 도입의 `parseYAML<T>`. `T`는 반환 자리에 한 번만 등장한다 — 황금률 위반이다. 입력과 아무 관계도 없는 `T`를 컴파일러가 추론할 방법은 없으니, 결국 **호출자가 원하는 타입을 그냥 선언하는** 꼴이 된다. `parseYAML('') as Weight`와 완전히 같은데 `as`가 안 보일 뿐이다. 검증 없는 단언은 [잘 보이게 쓰거나 한곳에 가두는 게](/typescript/11-type-assertions) 원칙이었는데, 반환 전용 제네릭은 단언을 **숨긴다**. 그래서 가짜 안전이다. 정직한 시그니처는 `unknown`을 반환하고 호출자에게 좁히기를 요구하는 것이다.

## 제네릭 "타입"도 같은 규칙으로 읽힌다

여기까지는 제네릭 함수였지만, 타입 별칭에 붙는 제네릭도 똑같이 읽으면 된다.

```typescript
type MyPartial<T> = { [K in keyof T]?: T[K] };

type PartPerson = MyPartial<Person>;
//   ^? type PartPerson = { name?: string | undefined; age?: number | undefined; }
```

`MyPartial`은 타입 `T`를 받아 새 타입을 반환하는 함수고, `MyPartial<Person>`은 그 함수의 호출이다. 표준 라이브러리의 `Partial`, `Pick`, `ReturnType` 같은 유틸리티 타입들은 전부 이렇게 정의된 **내장 타입 함수**들이다. 함수라는 걸 알고 나면 "제공되는 함수 목록을 외운다"에서 "필요하면 직접 짠다"로 넘어갈 수 있는데, 본문 안의 `[K in keyof T]?` 같은 문법이 바로 그 함수의 몸통이다.

---

제네릭은 특별한 문법이 아니라 **타입 세계의 함수이고, extends는 매개변수 타입, 황금률(두 번 이상 등장)은 매개변수가 진짜 일하는지의 검사**다. 그럼 이제 함수의 몸통을 쓸 차례다 — `MyPartial`의 `[K in keyof T]?`는 정확히 어떻게 동작하는 걸까. → [Partial은 어떻게 만들어지는가](/typescript/17-mapped-utility-types)
