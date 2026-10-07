---
title: 타입에도 조건문이 있다
description: 조건부 타입이 오버로드를 대체하는 이유와 유니온 분배의 원리
---

# 타입에도 조건문이 있다

[지난 글](/typescript/17-mapped-utility-types) 끝의 질문을 실전 문제로 바꿔보자. 숫자를 받으면 숫자를, 문자열을 받으면 문자열을 반환하는 `double` 함수의 타입을 어떻게 선언해야 할까. 처음 떠오르는 건 유니온이다.

```typescript
declare function double(x: string | number): string | number;

const num = double(12);
//    ^? const num: string | number — 숫자를 넣었는데 왜 문자열일지도 모른다는 걸까
```

입력과 출력의 관계가 끊겨 있다. 그럼 오버로드로 관계를 명시하면?

```typescript
declare function double(x: number): number;
declare function double(x: string): string;

const num = double(12);   // number — 좋다
const str = double('x');  // string — 좋다

function f(x: string | number) {
  return double(x);
  //            ~ No overload matches this call.
}
```

개별 호출은 완벽해졌는데, **유니온을 넘기는 순간 무너진다.** 오버로드는 위에서부터 하나씩 대조할 뿐이라 "number거나 string"인 값이 들어갈 자리가 없다. 세 번째 오버로드를 추가하면 되지만, 입력 종류가 늘수록 조합이 폭발한다.

## 조건부 타입 — 타입 층의 삼항 연산자

이 문제의 정답으로 책이 제시하는 게 **조건부 타입**(conditional type)이다.

```typescript
declare function double<T extends string | number>(
  x: T
): T extends string ? string : number;

const num = double(12);   // number
const str = double('x');  // string

function f(x: string | number) {
  return double(x); // string | number — 통과!
}
```

`T extends string ? string : number`는 생김새 그대로 삼항 연산자다 — 조건 자리에 [부분집합 판정](/typescript/05-types-as-sets)(`extends`)이 들어간다는 것만 다르다. "`T`가 `string`의 부분집합이면 `string`, 아니면 `number`."

그런데 잠깐. `f` 안의 호출에서 `T`는 `string | number`다. `string | number`는 `string`의 부분집합이 아니니 조건은 거짓, 그럼 결과는 `number`가 나와야 하는 것 아닌가? 실제 결과는 `string | number`다. 여기에 조건부 타입의 핵심 동작이 숨어 있다.

## 유니온은 조건 위에서 분배된다

조건부 타입의 조건 자리에 벌거벗은 타입 파라미터가 있고 거기에 유니온이 들어오면, 타입스크립트는 조건을 통째로 평가하지 않는다. **유니온의 멤버 각각에 조건을 적용한 뒤 결과를 다시 유니온으로 합친다.**

![double에 들어온 string | number 유니온이 멤버별로 갈라져 각각 조건부 타입을 통과한 뒤 string | number로 다시 합쳐지는 분배 과정](/images/typescript/18-distribution.png)

수학의 분배법칙과 똑같아서 **분배**(distribution)라고 부른다. 오버로드가 유니온 앞에서 무너진 지점을 조건부 타입이 통과하는 게 정확히 이 분배 덕분이다. 각 멤버에 대한 "올바른 답"이 자동으로 합쳐지니, 오버로드를 몇 개 쌓아도 못 만들 정확도가 선언 한 줄에서 나온다.

분배는 표준 유틸리티 타입들의 동력이기도 하다. 예컨대 `Exclude`의 정의는 조건부 타입 그 자체다.

```typescript
type Exclude<T, U> = T extends U ? never : T;

type T1 = Exclude<string | Date, string | number>;
//   ^? type T1 = Date
// string → never, Date → Date 로 분배된 뒤 never가 유니온에서 소거된다
```

멤버별로 조건을 검사해 탈락자는 `never`(공집합 — 유니온에 합쳐지면 사라진다)로 바꾸는, 타입 층의 `filter`다.

다만 분배가 **항상 원하는 동작은 아니다**. "T가 정확히 이 유니온 전체일 때"를 판정하고 싶은 경우엔 분배가 오히려 오답을 만든다. 그럴 땐 조건 양변을 튜플로 감싸 `[T] extends [U]`로 쓰면 분배가 꺼진다 — 벌거벗은 타입 파라미터가 아니게 되기 때문이다. 처음 보면 주술 같지만 원리는 방금 그 문장이 전부다.

마지막으로, 조건부 타입으로 **선언**한 함수의 **구현**은 여전히 사람 몫이다. 구현부 안에서 컴파일러는 `T`가 뭔지 모른 채 조건부 반환 타입을 검증하기 어려워서, 보통 구현용 시그니처 하나를 느슨하게 두는 절충(단일 오버로드 전략)을 쓴다. 시그니처의 정밀함과 구현의 검증 사이의 트레이드오프인 셈이다.

## 문자열까지 타입으로 계산된다 — 맛보기

조건·분배까지 오면 타입 레벨 프로그래밍의 문이 거의 다 열린 것이다. 마지막 조각 하나만 맛보면, **템플릿 리터럴 타입**은 문자열 조작마저 타입 층으로 가져온다.

```typescript
type EventHandlerName<T extends string> = `on${Capitalize<T>}`;

type ClickHandler = EventHandlerName<'click'>;
//   ^? type ClickHandler = "onClick"
```

라이브러리들이 `onClick`, `onChange` 같은 핸들러 이름을 오타 없이 강제하거나, 경로 문자열 `/user/:id`에서 파라미터 이름을 추출해내는 마법의 정체가 이것이다. 조건부 타입·매핑·템플릿 리터럴이 조합되면 타입 시스템 안에서 못 만드는 게 별로 없다 — 다만 그 힘은 라이브러리 타입을 **읽을 때** 제일 자주 필요하고, 내 코드에 쓸 때는 이 정도 복잡도가 정말 필요한지부터 묻는 게 맞다.

---

여기까지 열여덟 편. 첫 글에서 "타입은 빌드 때 지워진다"로 시작한 시리즈가, 지워질 타입 위에 집합론(값의 집합, 부분집합 판정)과 함수형 언어(타입의 함수, map과 filter, 조건문)가 통째로 올라가 있는 걸 확인하며 끝났다. 사실 타입스크립트를 "자바스크립트에 타입 표기를 붙인 것"으로 알고 시작했는데, 지금은 **자바스크립트의 런타임을 모델링하는 별도의 작은 언어**가 위에 얹혀 있다고 이해하고 있다. 에러 메시지가 이상해 보이는 날엔 이 시리즈의 어느 원리가 그 뒤에 있는지 찾아보게 될 것 같다 — 대부분은 컴파일러가 아니라 내 모델이 틀려 있었다.
