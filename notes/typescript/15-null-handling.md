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

## 별칭 속에 null을 숨기지 말 것

그럼 `User | null`을 자주 쓰게 될 텐데, 반복이 귀찮다고 이런 걸 만들고 싶어진다.

```typescript
type User = { id: string; name: string } | null; // 이러지 말 것
```

책이 이걸 콕 집어 말리는 이유가 있다. 이 별칭을 쓰는 코드에서 `user: User`라고 적으면, 읽는 사람은 "user는 User구나"라고 생각하지 **null일 수 있다는 사실을 알 길이 없다.** null 가능성이 이름 뒤에 숨는 것이다. null은 항상 사용하는 자리에서 보이게 쓴다 — `user: User | null`. 타입 이름은 값의 정체를 말하고, null 여부는 그 값을 받는 자리의 사정이라는 분업이다.

## null을 주변부로 밀어낸다

도입의 `extent`로 돌아가서, 타입 에러를 고쳐보자. 그냥 고치면 이렇게 된다 — `min`과 `max` 각각에 undefined 체크를 넣고, 반환 타입은 `(number | undefined)[]`가 되고, 호출하는 쪽도 두 값을 따로따로 검사해야 한다. 그런데 `min`이 undefined면 `max`도 반드시 undefined다. **둘의 null 여부는 항상 함께 움직이는데, 타입은 그 관계를 표현하지 못하고 검사만 두 배로 시킨다.**

해법은 지난 글과 같은 발상이다. 함께 움직이는 값들을 하나로 묶고, null은 **묶음 전체에 한 번만** 붙인다.

```typescript
function extent(nums: Iterable<number>) {
  let minMax: [number, number] | null = null;
  for (const num of nums) {
    if (!minMax) {
      minMax = [num, num];
    } else {
      minMax = [Math.min(num, minMax[0]), Math.max(num, minMax[1])];
    }
  }
  return minMax; // [number, number] | null
}

const range = extent([0, 1, 2]);
if (range) {
  const [min, max] = range; // 여기서는 둘 다 확실한 number
  const span = max - min;
}
```

내부의 값들은 전부 non-null이고, null 가능성은 반환값이라는 **껍데기 한 곳**에만 존재한다. 호출부는 체크 한 번으로 전부를 얻는다. falsy 함정도 함께 사라졌다 — `!minMax`는 튜플(객체)엔 절대 참이 아니니 `[0, 0]`도 안전하다. 덧붙이면 원래 교재 예제는 else 분기에서 구조 분해로 이전 값을 꺼내는데, 검증에 쓴 TS 5.9에서는 그 형태가 순환 추론 에러(TS7022)를 내서 인덱스 접근으로 바꿨다 — 동작은 같다.

"절대 null이 아닌 시점"이 명확한 데이터라면 한 걸음 더 가서, 값이 모두 준비된 뒤에야 생성되는 클래스로 만들면 사용하는 쪽에서 null 검사가 아예 사라진다. 방향은 같다 — **null이 존재하는 영역을 초기화 단계라는 주변부로 몰아넣고, 핵심 로직은 non-null의 세계에서 돌린다.**

---

null 다루기의 요령은 없애는 게 아니라 **배치**다 — 타입 별칭 깊숙이 숨기지 말고, 개별 값마다 흩뿌리지 말고, 데이터 묶음의 바깥 껍데기 한 곳에 모아서 체크 한 번으로 끝나게 만드는 것. strictNullChecks는 그 배치 설계를 강제로 시작하게 만드는 스위치일 뿐이다.
