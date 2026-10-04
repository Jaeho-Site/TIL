---
title: Partial은 어떻게 만들어지는가
description: keyof, 인덱스 접근, 매핑된 타입 — 유틸리티 타입을 직접 조립하기, 그리고 Object.keys의 진실
---

# Partial은 어떻게 만들어지는가

[지난 글](/typescript/16-generics-as-functions)에서 유틸리티 타입이 "내장 타입 함수"라고 했으니, 이번엔 그 함수의 부품을 뜯는다. 그 전에 부품이 왜 필요한지 보여주는 퀴즈 하나. [구조적 타이핑](/typescript/03-structural-typing)에서 만났던 그 에러의 재림이다.

```typescript
const obj = {
  one: 'uno',
  two: 'dos',
  three: 'tres',
};
for (const k in obj) {
  const v = obj[k];
  //        ~~~~~~ Element implicitly has an 'any' type because expression
  //               of type 'string' can't be used to index type
  //               '{ one: string; two: string; three: string; }'
}
```

`obj`의 키는 눈에 보이는 대로 셋뿐인데, `k`는 왜 `'one' | 'two' | 'three'`가 아니라 `string`으로 추론될까. 그 이유를 답할 부품들을 모으고 나서 글 끝에서 다시 돌아온다.

## 부품 1 — keyof: 타입에서 키들을 꺼낸다

```typescript
interface Options {
  width: number;
  height: number;
  color: string;
  label: string;
}

type OptionsKeys = keyof Options;
// "width" | "height" | "color" | "label"
```

`keyof T`는 타입의 키들을 리터럴 유니온으로 준다. [값 공간의 `Object.keys`에 대응하는 타입 공간의 연산](/typescript/06-type-value-space)인 셈이다.

## 부품 2 — 인덱스 접근: 타입에서 속성 타입을 꺼낸다

```typescript
type WidthType = Options['width'];  // number

type Action = { type: 'save' } | { type: 'load' };
type ActionType = Action['type'];   // 'save' | 'load' — 유니온에도 동작
```

값 공간의 `obj['width']`와 똑같이 생겼지만 대괄호 안에 들어가는 게 **타입**이다(`'width'`는 리터럴 타입). 유니온을 넣으면 각 멤버의 속성 타입이 유니온으로 나온다.

## 부품 3 — 매핑: 키들을 순회하며 새 타입을 조립한다

```typescript
type MyPartial<T> = { [K in keyof T]?: T[K] };
```

이제 읽을 수 있다. "`T`의 키 각각을 `K`라 할 때(`in`은 유니온 순회), 같은 키에 `T[K]` 타입을 주되 전부 옵셔널(`?`)로." — 값 세계로 번역하면 `Object.fromEntries(Object.entries(obj).map(...))` 같은 변환 루프다. 실제로 `MyPartial<Options>`는 내장 `Partial<Options>`와 완전히 같은 타입이 나온다. `Pick`도 마찬가지로 두 부품의 조합이다.

```typescript
type MyPick<T extends object, K extends keyof T> = { [P in K]: T[P] };
```

여기서 `K extends keyof T` 제약이 지난 글의 황금률 그대로 일한다 — 제약이 없으면 `T`에 없는 키가 들어와 `T[P]`가 성립하지 않는다.

이 부품들의 진짜 가치는 유틸리티 타입을 직접 만드는 게 아니라(대부분 내장으로 충분하다), **타입 사이의 중복을 파생 관계로 바꾸는** 데 있다. `Options`와 "모든 속성이 옵셔널인 Options 갱신용 타입"을 각각 손으로 관리하면, 속성 하나 추가할 때 두 곳을 고쳐야 하고 언젠가 어긋난다. `Partial<Options>`로 파생시키면 원본만 고치면 된다. 타입에도 DRY 원칙이 적용되는 것이다.

값에서 타입을 파생시키는 부품도 있다. [typeof의 타입 공간 버전](/typescript/06-type-value-space)과 `ReturnType`이다.

```typescript
const INIT_OPTIONS = { width: 640, height: 480, color: '#00FF00', label: 'VGA' };
type InferredOptions = typeof INIT_OPTIONS; // 값에서 타입을 역산 — 위의 Options와 같은 형태

type UserInfo = ReturnType<typeof getUserInfo>; // 함수 반환 타입에서 파생
```

## 다시 도입 퀴즈로 — Object.keys는 왜 string[]인가

부품이 모였으니 답할 수 있다. `k`가 `keyof typeof obj`가 아닌 이유는 컴파일러의 게으름이 아니라 [구조적 타이핑의 정직한 귀결](/typescript/03-structural-typing)이다. **타입은 열려 있다.** `obj` 자리에 올 수 있는 값은 선언에 없는 속성을 얼마든지 더 가질 수 있고, 특히 함수 매개변수라면 실제로 그런 값이 들어온다. 그러니 런타임 순회에서 만날 키의 집합을 컴파일러는 `'one' | 'two' | 'three'`로 **보장할 수 없다**. `string`이 정확한 답이다. `Object.keys`의 반환 타입이 `(keyof T)[]`가 아니라 `string[]`인 것도 같은 논리다.

그래서 우회는 두 갈래다. 키 집합을 정말 내가 안다면 — 지역에서 만든 리터럴 객체처럼 — 그 지식을 [단언으로](/typescript/11-type-assertions) 전달한다.

```typescript
for (const kStr in obj) {
  const k = kStr as keyof typeof obj;
  //    ^? const k: "one" | "two" | "three"
  const v = obj[k]; // 통과
}
```

모른다면 키를 좁히려 하지 말고 값 쌍으로 순회하는 게 편하다.

```typescript
for (const [k, v] of Object.entries(obj)) {
  // k: string, v: string — 보장 가능한 만큼만 정확하다
}
```

개인적으로 이 퀴즈가 좋았던 건, "타입스크립트가 불편하게 군다"고 느꼈던 지점이 사실 3편에서 배운 원리의 논리적 귀결이었다는 점이다. 원리 하나가 시리즈를 관통해서 같은 얼굴로 계속 나타난다.

---

`keyof`·인덱스 접근·매핑은 **타입을 데이터처럼 순회하고 변환하는 부품**이고, Partial과 Pick은 그 부품으로 조립된 함수일 뿐이다. 그런데 함수라면 아직 없는 게 하나 있다. 입력에 따라 **다른 결과를 반환하는 분기**는 타입 세계에 없을까. → [타입에도 조건문이 있다](/typescript/18-conditional-types)
