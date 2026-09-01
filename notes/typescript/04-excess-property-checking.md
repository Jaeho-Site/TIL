---
title: 객체 리터럴만 더 엄격하게 검사되는 이유
description: 잉여 속성 검사는 할당 가능성 검사와 별개의 절차다
---

# 객체 리터럴만 더 엄격하게 검사되는 이유

[지난 글](/typescript/03-structural-typing) 끝에서 예고한 실험이다. 타입은 열려 있다고 했으니, 속성이 더 달린 객체를 넘기는 두 가지 방법을 나란히 놓고 돌려봤다.

```typescript
interface Room {
  numDoors: number;
  ceilingHeightFt: number;
}

// A. 객체 리터럴을 바로 할당
const r1: Room = {
  numDoors: 1,
  ceilingHeightFt: 10,
  elephant: 'present',
};

// B. 변수에 담았다가 할당
const obj = {
  numDoors: 1,
  ceilingHeightFt: 10,
  elephant: 'present',
};
const r2: Room = obj;
```

같은 값, 같은 타입. 결과도 같아야 하지 않을까? 실제로는 **A만 에러**다.

```
error TS2353: Object literal may only specify known properties,
and 'elephant' does not exist in type 'Room'.
```

B는 통과한다. `obj`는 `Room`의 구조를 만족하니까, 지난 글의 결론 그대로다. 그럼 A는 뭐가 다른 걸까. 사실 나는 이 지점에서 구조적 타이핑을 잘못 이해했나 싶어 한참 헤맸다.

## 검사가 하나가 아니었다

답은 의외로 단순했다. 타입 체커는 여기서 **서로 다른 두 개의 검사**를 운용한다.

하나는 지금까지 봐온 **할당 가능성 검사** — 구조가 요구 조건을 만족하는가. A도 B도 이 검사는 통과한다.

다른 하나가 **잉여 속성 검사**(excess property checking)다. 발동 조건이 아주 좁다. **객체 리터럴을, 타입이 알려진 자리에, 직접** 쓸 때만 발동한다. 이때는 선언에 없는 속성이 있으면 에러를 낸다. B처럼 중간 변수를 거치면 "객체 리터럴 직접 할당"이 아니게 되므로 이 검사 자체가 일어나지 않는다.

![같은 객체라도 리터럴 직접 할당 경로는 할당 가능성 검사에 더해 잉여 속성 검사까지 발동해 elephant에서 에러가 나고, 중간 변수 경로는 잉여 속성 검사가 발동하지 않아 통과하는 두 갈래 흐름](/images/typescript/04-two-checks.png)

왜 리터럴만 특별 취급할까? 의도를 생각해 보면 납득이 된다. 이미 존재하는 값에 여분 속성이 있는 건 구조적 타이핑의 세계에서 지극히 정상이다. 하지만 **그 자리에서 갓 만든 리터럴**의 여분 속성은 사정이 다르다. 그 속성은 런타임에 객체에 실려 가긴 하지만, 타입 층에서는 어떤 코드도 접근할 수 없는 죽은 속성이 된다. 죽을 속성을 일부러 쓸 이유는 없으니, 높은 확률로 오타거나 착각이다.

```typescript
interface Options {
  title: string;
  darkMode?: boolean;
}
declare function createWindow(options: Options): void;

createWindow({
  title: 'Spider Solitaire',
  darkmode: true,
  // ~~~~~~ Object literal may only specify known properties,
  //        but 'darkmode' does not exist in type 'Options'.
  //        Did you mean to write 'darkMode'?
});
```

`darkMode`를 `darkmode`로 잘못 쓴 이 코드는 구조적으로는 **합법**이다. `darkmode`는 그냥 여분 속성이고, `darkMode`는 옵셔널이라 없어도 되니까. 잉여 속성 검사가 없었다면 이 버그는 조용히 런타임까지 흘러가서 "다크 모드가 안 켜져요"가 됐을 것이다. 구조적 타이핑의 구멍을 리터럴에 한해서만 틀어막는 보완 장치인 셈이다.

## 검사가 사라지는 순간들

발동 조건이 좁다는 건 빠져나갈 문이 많다는 뜻이기도 하다. 중간 변수 말고도 타입 단언을 쓰면 검사가 사라진다.

```typescript
const o = { darkmode: true, title: 'MS Hearts' } as Options; // 통과
```

같은 리터럴인데 `: Options` 선언은 잡아주고 `as Options` 단언은 통과시킨다. 개인적으로 단언보다 선언을 써야 하는 이유 중 이만큼 피부에 와닿는 게 없었다 — 단언은 이런 안전 검사들을 통째로 끄고 지나간다. 단언 이야기는 뒤에서 제대로 다룬다.

물론 정공법도 있다. 정말로 임의의 여분 속성을 받겠다는 의도라면, 우회가 아니라 인덱스 시그니처로 타입에 그 의도를 선언하면 된다(`[otherOptions: string]: unknown`).

## 전부 옵셔널이면 검사가 하나 더 붙는다

`Options`처럼 옵셔널 속성만 있는 타입을 약한(weak) 타입이라고 부르는데, 이 경우엔 아예 별도의 검사가 하나 더 있다. 공통 속성이 **하나도 없으면** 할당 자체를 막는다.

```typescript
interface LineChartOptions {
  logscale?: boolean;
  invertedYAxis?: boolean;
  areaChart?: boolean;
}
declare function setOptions(options: LineChartOptions): void;

const opts = { logScale: true }; // 대소문자 오타 (logscale이어야 함)
setOptions(opts);
//         ~~~~ Type '{ logScale: boolean; }' has no properties in common
//              with type 'LineChartOptions'
```

전부 옵셔널이면 구조적으로는 빈 객체조차 유효해서, 오타를 내도 영원히 에러가 안 난다. 그래서 이 검사는 중간 변수를 거쳐도 발동한다. 잉여 속성 검사와 달리 이건 진짜 할당 가능성 규칙의 일부다.

---

객체 리터럴이 유독 엄격하게 검사받는 건 구조적 타이핑이 오락가락해서가 아니라, **할당 가능성과는 별개인 잉여 속성 검사가 리터럴에만 추가로 발동하기 때문**이다. 두 검사를 하나로 뭉뚱그리면 "타입스크립트가 어떨 땐 열려 있고 어떨 땐 닫혀 있다"는 미신이 생긴다 — 나처럼. 그런데 "구조가 요구 조건을 만족하면 할당된다"는 규칙 자체도, 곱씹을수록 더 정확한 표현이 있을 것 같았다. → [타입은 값의 집합이다](/typescript/05-types-as-sets)
