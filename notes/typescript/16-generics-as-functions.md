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
