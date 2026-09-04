---
title: 타입은 값의 집합이다
description: never부터 unknown까지 — 할당 가능성, 유니온, 인터섹션, extends를 관통하는 하나의 관점
---

# 타입은 값의 집합이다

[지난 글](/typescript/04-excess-property-checking)까지 "구조가 맞으면 할당된다"는 감각으로 버텨왔는데, 인터섹션 타입을 만난 날 그 감각이 무너졌다.

```typescript
interface Person {
  name: string;
}
interface Lifespan {
  birth: Date;
  death?: Date;
}
type PersonSpan = Person & Lifespan;
```

`&`는 인터섹션, 즉 교집합이라고 배웠다. `Person`과 `Lifespan`의 교집합이라면... 두 타입의 공통 속성? 공통 속성은 없으니 `PersonSpan`은 빈 타입일까? 퀴즈: 아래 코드는 컴파일될까?

```typescript
const ps: PersonSpan = {
  name: 'Alan Turing',
  birth: new Date('1912/06/23'),
};
```

**통과한다.** `PersonSpan`은 빈 타입이 아니라 `name`과 `birth`를 **모두** 요구하는 타입이다. 교집합이라더니 속성은 합집합처럼 불어났다. 여기서 뭘 놓치고 있는 걸까.

## 타입이 담고 있는 건 속성이 아니라 값이다

내 착각은 `&`가 **속성 목록**에 적용된다고 생각한 것이었다. 타입스크립트 공식 문서와 책이 공통으로 미는 관점은 이렇다. **타입은 할당 가능한 값들의 집합이다.**

- `Person`은 "name이 문자열인 모든 객체"의 집합이다. 지난 글에서 본 대로 타입은 열려 있으니, `birth`가 더 있는 값도 이 집합의 원소다.
- `Lifespan`은 "birth가 Date인 모든 객체"의 집합이다.
- `Person & Lifespan`은 이 **값 집합의 교집합** — 양쪽 모두에 속하는 값들이다.

양쪽 모두에 속하려면 `name`도 있어야 하고 `birth`도 있어야 한다. 그래서 값의 교집합을 구했더니 속성 요구 조건은 합쳐진 것이다. 교집합인데 속성이 늘어나는 게 아니라, **집합이 좁아질수록 조건이 늘어나는** 것이다.

![Person 값 집합과 Lifespan 값 집합의 벤 다이어그램 — 교집합 영역이 Person & Lifespan이고, name과 birth를 모두 가진 값들이 위치한다](/images/typescript/05-types-as-sets.png)

이 관점으로 지금까지의 개념을 다시 쓰면 전부 집합 용어로 번역된다.

| 타입스크립트 용어 | 집합 용어 |
|---|---|
| `A`에 할당 가능하다 | `A`의 부분집합이다 (원소다) |
| `A \| B` | 합집합 |
| `A & B` | 교집합 |
| `A extends B` | `A ⊂ B` |
| `never` | 공집합 |
| `unknown` | 전체집합 |

## 집합의 크기로 타입을 줄 세워 보면

제일 작은 집합은 원소가 없는 `never`다. 어떤 값도 담을 수 없다.

```typescript
const x: never = 12;
//    ~ Type '12' is not assignable to type 'never'.
```

그다음은 원소가 하나인 리터럴 타입(`type A = 'A'`), 유니온으로 원소를 늘린 타입(`type AB = 'A' | 'B'`), 무한 집합인 `string`·`number`, 그리고 모든 값을 담는 `unknown`까지. 할당 가능성 검사는 이 스펙트럼 위 어딘가의 두 집합에 대한 포함 관계 판정이다 — 참고로 `string`과 `number`처럼 어느 쪽도 부분집합이 아닌 쌍도 얼마든지 있다. 타입들은 계층이 아니라 겹치는 벤 다이어그램을 이룬다.

```typescript
type AB = 'A' | 'B';
type AB12 = 'A' | 'B' | 12;

declare let ab: AB;
const ab12: AB12 = ab; // 통과 — {'A','B'} ⊂ {'A','B',12}

declare let twelve: AB12;
const back: AB = twelve;
//    ~~~~ Type 'AB12' is not assignable to type 'AB'.
//         Type '12' is not assignable to type 'AB'.
```

`extends`도 마찬가지다. 상속이라는 어감 때문에 "기능을 물려받는다"로 읽기 쉬운데, 집합 관점에서는 그냥 부분집합 선언이다. 그래서 이런 에러도 설명된다.

```typescript
interface NullyStudent {
  name: string;
  ageYears: number | null;
}
interface StringyStudent extends NullyStudent {
  ageYears: number | string;
  // ~~~ Interface 'StringyStudent' incorrectly extends interface 'NullyStudent'.
}
```

`ageYears`를 `number | string`으로 바꾸면 `NullyStudent`에 속하지 않는 값(문자열 나이)이 생겨서 부분집합이 깨진다. "자식이 부모보다 넓어질 수 없다"는 규칙의 정체는 집합의 포함 관계였다.

참고로 `string`과 `String`(래퍼 객체 타입)도 집합으로 보면 깔끔하다. 원시 문자열 집합은 `String` 집합의 부분집합이라 `string → String` 할당은 되지만 역방향은 에러다. 그리고 애초에 래퍼 타입을 쓸 일은 없다 — 항상 소문자 `string`이 정답이다.

## keyof (Person | Lifespan)은 왜 never인가

이 관점의 위력을 시험해볼 문제가 하나 있다. 책에서 만난 건데 처음엔 정말 이해가 안 됐다.

```typescript
type K = keyof (Person | Lifespan);
//   ^? type K = never
```

`Person | Lifespan`의 키라면 `name`, `birth`, `death` 다 나와야 할 것 같은데 `never`다. 집합으로 풀어보자. `Person | Lifespan` 타입의 값은 두 집합의 **합집합** 원소다 — `Person`일 수도, `Lifespan`일 수도 있다. 이 값에서 **확실하게** 존재한다고 말할 수 있는 키는? `name`은 `Lifespan` 쪽 값이면 없을 수 있고, `birth`는 `Person` 쪽 값이면 없을 수 있다. 보장되는 키는 공통 키뿐인데, 둘의 공통 키는 없다. 그래서 공집합, `never`다.

일반화하면 `keyof (A | B) = (keyof A) & (keyof B)`. 값의 집합이 넓어질수록(유니온) 보장되는 키는 좁아진다(인터섹션). 방향이 반대로 움직이는 게 처음엔 어지럽지만, "집합이 커지면 모든 원소가 공유하는 성질은 줄어든다"고 생각하면 자연스럽다.

---

할당 가능성, 유니온, 인터섹션, extends, never — 따로 외우던 규칙들이 **타입은 값의 집합이고 모든 검사는 부분집합 판정**이라는 한 문장으로 접힌다. 그런데 이렇게 타입을 값의 세계와 계속 오가며 설명하다 보니, 정작 기본적인 걸 헷갈리고 있었다. `Person`이라는 이름은 타입인데, 코드 어떤 자리에서는 값처럼 보이기도 한다. 이 이름들은 대체 어디에 사는 걸까. → [같은 이름이 타입도 되고 값도 된다](/typescript/06-type-value-space)
