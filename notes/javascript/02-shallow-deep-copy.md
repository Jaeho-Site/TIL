---
title: 얕은 복사와 깊은 복사는 뭐가 다른가
description: 스프레드 복사는 1층까지만 — structuredClone과 JSON 복사의 한계
---

# 얕은 복사와 깊은 복사는 뭐가 다른가

[지난 글](/javascript/01-primitive-vs-object)에서 `=` 대입은 참조만 복사한다는 걸 봤다. 그래서 객체를 진짜로 복사할 땐 스프레드(`...`)를 쓰라고 배웠는데, 이 문제에서 걸렸다.

```javascript
const original = {
  name: 'Lee',
  address: { city: 'Seoul' }
};

const copy = { ...original }; // 스프레드로 복사했다

copy.name = 'Kim';
copy.address.city = 'Busan';

console.log(original.name);         // ?
console.log(original.address.city); // ?
```

`name`은 예상대로 `'Lee'`가 유지된다. 그런데 `original.address.city`는 **`'Busan'`**이다. 분명히 복사본만 건드렸는데 원본의 중첩 객체가 따라 바뀌었다. 복사가 됐다는 건가, 안 됐다는 건가?

## 복사는 언제나 1층까지만 된다

스프레드가 하는 일을 정확히 쓰면 이렇다 — **프로퍼티를 한 층만 순회하면서, 각 프로퍼티의 "값"을 새 객체에 복사한다.** 문제는 그 값의 정체다. [지난 글](/javascript/01-primitive-vs-object)에서 봤듯:

- `name`의 값은 원시 값 `'Lee'` → 값 자체가 복사된다. 남남이 된다.
- `address`의 값은 **객체가 아니라 객체의 참조** → 참조가 복사된다. `original.address`와 `copy.address`는 **같은 객체를 가리킨다.**

겉껍데기만 새 객체이고 속의 객체들은 공유되는 것, 이걸 **얕은 복사**(shallow copy)라고 한다. 스프레드도, `Object.assign`도, 배열의 `slice`·`concat`도 전부 얕은 복사다. 중첩된 안쪽까지 전부 새로 만드는 **깊은 복사**(deep copy)는 별도의 도구가 필요하다.

사실 "얕다"는 말보다 이렇게 기억하는 게 정확했다. **복사라는 연산 자체가 원래 1층짜리다.** 참조가 담긴 칸을 복사하면 참조가 복사되는 것뿐이고, 깊은 복사란 "모든 층에서 얕은 복사를 재귀적으로 반복하는 것"에 지나지 않는다.

## 깊은 복사는 어떻게 하나

**요즘의 정답은 `structuredClone`이다.** 브라우저와 Node.js에 내장된 표준 API로, 중첩 구조 전체를 재귀적으로 복제한다.

```javascript
const copy = structuredClone(original);

copy.address.city = 'Busan';
console.log(original.address.city); // 'Seoul' — 이제 진짜 남남이다
```

`structuredClone` 이전에 널리 쓰던 우회로가 JSON 왕복이다.

```javascript
const copy = JSON.parse(JSON.stringify(original));
```

객체를 문자열로 완전히 풀었다가 다시 조립하니 참조가 남을 수 없다는 아이디어인데, **JSON이 표현 못 하는 값은 전부 사고가 난다.** 함수와 `undefined`인 프로퍼티는 사라지고, `Date`는 문자열로 변질되고, `Map`/`Set`은 빈 객체가 되고, 순환 참조(자기 자신을 참조하는 구조)는 에러를 던진다. `structuredClone`은 이 중 `Date`·`Map`·`Set`·순환 참조까지 처리한다(함수는 여전히 복제 불가 — 에러가 난다). 그 밖에 lodash의 `cloneDeep`도 실무에서 많이 보이는 선택지다.

## 실제로는 깊은 복사를 잘 안 쓴다?

여기까지 정리하고 나니 오히려 반전이 있었다. React 상태 업데이트 코드를 보면 깊은 복사가 아니라 **얕은 복사를 중첩**해서 쓴다.

```javascript
setUser({
  ...user,
  address: { ...user.address, city: 'Busan' } // 바꿀 경로만 새로 만든다
});
```

이유는 성능이다. 깊은 복사는 전체 트리를 새로 만들지만, 이 패턴은 **바뀌는 경로의 객체만 새로 만들고 나머지는 참조를 그대로 공유한다.** 안 바뀐 부분은 참조가 같으니 React가 "여기는 안 바뀌었네"를 참조 비교 한 번으로 알 수 있고, 바뀐 경로는 새 참조라서 변경이 감지된다. 얕은 복사의 "공유" 성질이 함정이 아니라 최적화 도구로 쓰이는 셈이다.

물론 그만큼 실수하기도 쉽다. 한 층이라도 스프레드를 빼먹으면 도입 문제처럼 원본(이전 상태)을 직접 수정하게 된다. 이 번거로움을 줄여주는 게 Immer 같은 라이브러리다 — 직접 수정하는 것처럼 쓰면 불변 업데이트로 바꿔준다.

---

**복사는 언제나 1층까지만 된다.** 얕은 복사는 그 사실을 받아들인 것이고, 깊은 복사는 그걸 전 층에서 재귀한 것이고, React의 불변 업데이트는 그 성질을 역이용한 것이다.

그런데 방금 "React가 참조 비교 한 번으로 안다"고 했다. 참조를 비교한다는 건 정확히 어떤 비교일까? `===`는 객체에게 무엇을 묻는 걸까? → [==와 ===는 뭐가 다른가](/javascript/03-equality)
