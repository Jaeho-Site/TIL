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
