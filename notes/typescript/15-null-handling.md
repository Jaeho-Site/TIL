---
title: null은 타입의 어디에 둬야 하나
description: strictNullChecks의 정체와 null을 값의 주변부로 밀어내는 설계
---

# null은 타입의 어디에 둬야 하나

[지난 글](/typescript/14-discriminated-union)에서 무효 상태의 단골 원인으로 null을 지목했다. 소재로 삼기 좋은 함수가 책에 있다. 숫자들의 최솟값과 최댓값을 구하는 함수다. 퀴즈: 이 코드에는 타입 에러와 별개로 **런타임 버그**가 하나 있다. 어디일까?

```typescript
function extent(nums: Iterable<number>) {
  let min, max;
  for (const num of nums) {
    if (!min) {
      min = num;
      max = num;
    } else {
      min = Math.min(min, num);
      max = Math.max(max, num);
    }
  }
  return [min, max];
}
```

`extent([0, 1, 2])`를 실행하면 `[0, 2]`가 아니라 `[1, 2]`가 나온다. 범인은 `if (!min)` — [좁히기 글](/typescript/08-narrowing)에서 본 falsy 함정이다. `min`이 `0`이면 "아직 초기화 안 됨"으로 오판하고 값을 리셋한다. undefined 체크를 하려던 자리에 falsy 체크를 쓴 것이다.

그럼 타입 체커는 뭘 하고 있었을까. 사실 falsy 버그 자체는 체커가 잡지 못한다 — `!min`은 어엿한 truthiness 좁히기라서, `else` 분기의 `min`은 `number`로 인정받고 조용히 통과한다. 대신 strict 모드로 컴파일하면 체커는 **다른 균열**을 잡아낸다.

```
error TS2345: Argument of type 'number | undefined' is not assignable
              to parameter of type 'number'.   // Math.max(max, num)의 max
error TS18048: 'min' is possibly 'undefined'.  // 반환값을 쓰는 쪽 — max도 같이
```

`!min`으로 좁힌 건 `min`뿐이니 `max`는 루프 안에서 `undefined` 가능성이 남아 걸리고, 반환값을 쓰는 쪽에서는 둘 다 걸린다(빈 이터러블이 들어오면 정말로 `[undefined, undefined]`가 나온다). falsy 버그를 직접 겨눈 에러는 아니지만, 이 에러들을 제대로 고치려고 구조를 손보는 과정에서 — 글 뒤에서 확인하겠지만 — falsy 버그까지 함께 해소된다. 컴파일러가 "여기 undefined 처리가 엉성하다"고 짚은 자리가 정확히 버그의 서식지였던 셈이다.

## strictNullChecks가 바꾸는 것 — 집합의 경계

이 검사를 켜는 스위치가 `strictNullChecks`(strict에 포함)다. [집합의 언어](/typescript/05-types-as-sets)로 말하면 이 옵션의 정체가 제일 선명하다. **옵션이 꺼져 있으면 `null`과 `undefined`는 모든 타입 집합의 원소다.** `number`에도, `string`에도, 내가 만든 `User`에도 소리 없이 들어 있다. 그래서 어떤 값이든 언제나 null일 수 있고, 컴파일러는 아무 경고도 못 한다 — 자바의 NullPointerException 세계와 같다.

옵션을 켜면 `null`은 원소 하나짜리 독립 집합으로 분리된다. null이 가능하다는 사실은 이제 `User | null`처럼 **타입에 명시**해야 하고, 명시한 곳에서는 좁히기로 검사를 통과해야 쓸 수 있다. "null일 수 있음"이 암묵적 전제에서 **타입 시스템이 추적하는 정보**로 승격되는 것이다.
