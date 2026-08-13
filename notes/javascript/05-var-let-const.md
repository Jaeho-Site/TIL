---
title: var와 let/const는 뭐가 다른가
description: let은 호이스팅이 안 되는 게 아니라, 초기화가 미뤄질 뿐이다 — TDZ
---

# var와 let/const는 뭐가 다른가

[지난 글](/javascript/04-hoisting)에서 `let`도 호이스팅된다고 말했다. 그 근거가 되는 문제부터 보자.

```javascript
let foo = 1; // 전역 변수

{
  console.log(foo); // ?
  let foo = 2; // 지역 변수
}
```

"let은 호이스팅이 안 된다"고 외웠다면 답은 `1`이어야 한다. 블록 안의 `let foo`는 아직 선언 전이니, 바깥의 전역 변수 `foo`를 참조하면 되니까. 그런데 실제 결과는 이렇다.

```
ReferenceError: Cannot access 'foo' before initialization
```

에러 메시지를 잘 읽어보면 힌트가 있다. `foo is not defined`(그런 변수 없음)가 아니라 **"before initialization"**, 즉 "초기화 전에는 접근할 수 없다"고 말한다. 엔진은 블록 안에 `foo`가 선언될 것을 **이미 알고 있다.** 알고 있으니까 바깥 `foo` 대신 블록 안의 `foo`를 잡았고, 아직 초기화 전이라 에러를 던진 것이다. 이게 `let`도 호이스팅된다는 증거다.

## 차이는 "초기화 시점"이다

변수는 세 단계를 거쳐 만들어진다. **선언 → 초기화(undefined 할당) → 값 할당.** var와 let의 차이는 이 세 단계가 언제 일어나느냐다.

```javascript
// var: 평가 단계에서 선언 + 초기화가 동시에 일어난다
console.log(foo); // undefined
var foo;
foo = 1;
```

```javascript
// let: 평가 단계에서는 선언만 된다
console.log(foo); // ReferenceError
let foo; // ← 이 줄에 도달해야 초기화된다
foo = 1;
```

`let`은 스코프 시작부터 선언문에 도달하기 전까지 "선언은 됐지만 초기화는 안 된" 구간이 생기는데, 이 구간을 **TDZ**(Temporal Dead Zone, 일시적 사각지대)라고 부른다. TDZ 안에서 변수를 참조하면 `ReferenceError`가 난다.

![var와 let의 선언·초기화·할당 시점을 비교하는 타임라인. let은 스코프 시작부터 선언문까지 TDZ 구간이 있다](/images/javascript/05-tdz-timeline.png)

정리하면 이렇게 말할 수 있다. **"let도 호이스팅된다. 다만 var는 호이스팅 시점에 undefined로 초기화되지만, let은 초기화가 선언문까지 미뤄져서 그 사이(TDZ)에 참조하면 에러가 난다."** 이 한 문장이 "let은 호이스팅 안 된다"보다 정확한 이해다.

참고로 이 표현은 어디마다 갈리는것 같다. MDN에서도 let과 const의 호이스팅 여부는 정의의 문제라고 설명하고, 일부 문서에서는 let에 호이스팅이 적용되지 않는다고 표현한다. 
반면 호이스팅 용어집에서는 let/const를 TDZ를 만드는 type 3 hoisting으로 분류한다. 

결국 “let은 호이스팅된다/안 된다”라는 표현 자체보다, 선언 전부터 바인딩이 존재하지만 초기화 전까지 TDZ에 있어 접근할 수 없다는 동작을 이해하는 것이 중요하다고 생각한다.

## 그럼 var의 문제는 TDZ가 없다는 것뿐인가?

아니다. 사실 var는 문제가 세 개 더 있고, let/const는 그걸 하나씩 고친 키워드다.

**첫째, 함수 레벨 스코프.** var는 함수 몸체만 스코프로 인정한다. if문, for문 같은 블록은 스코프가 아니다.

```javascript
var i = 10;

for (var i = 0; i < 5; i++) {
  console.log(i); // 0 1 2 3 4
}

console.log(i); // 5 — 전역 i가 덮어써졌다
```

for문의 `i`가 블록에 갇히지 않고 전역으로 새어 나와, 이미 있던 `i`를 조용히 덮어쓴다. let은 블록 레벨 스코프라 이런 누출이 없다.

**둘째, 중복 선언 허용.**

```javascript
var x = 1;
var x = 100; // 에러 없이 통과

let y = 1;
let y = 100; // SyntaxError: Identifier 'y' has already been declared
```

파일이 길어지면 같은 이름을 이미 썼는지 기억하기 어렵다. var는 실수로 중복 선언해도 에러 없이 값을 덮어쓰고, let은 문법 에러로 즉시 잡아준다.

**셋째, 전역 객체 오염.** 브라우저에서 var로 선언한 전역 변수는 전역 객체 `window`의 프로퍼티가 된다.

```javascript
var x = 1;
console.log(window.x); // 1

let y = 2;
console.log(window.y); // undefined — let은 window에 붙지 않는다
```

내 변수가 `window`에 붙는다는 건, 다른 스크립트나 라이브러리의 프로퍼티와 이름이 충돌할 수 있다는 뜻이다. let/const는 전역에 선언해도 전역 객체의 프로퍼티가 되지 않는다.

## const로 선언한 객체는 왜 수정되나?

```javascript
const person = { name: 'Lee' };

person.name = 'Kim'; // 에러가 안 난다?
console.log(person); // { name: "Kim" }

person = {}; // TypeError: Assignment to constant variable.
```

const가 금지하는 건 **재할당**이지 값의 변경이 아니다. `person`이라는 변수가 잡고 있는 참조를 바꿀 수 없을 뿐, 그 참조가 가리키는 객체의 내부는 얼마든지 바뀐다. 이걸 제대로 이해하려면 원시 값과 객체가 메모리에 저장되는 방식을 알아야 하는데, 그건 데이터 타입 글에서 따로 다룰 예정이다.

개인적으로 기본값은 const, 재할당이 정말 필요할 때만 let, var는 안 쓴다는 원칙이 답이라고 생각한다. 재할당 여부가 코드를 읽는 사람에게 힌트가 되기 때문이다.

---

let은 호이스팅이 안 되는 게 아니라, **초기화가 선언문까지 미뤄질 뿐이다.** var와의 차이는 결국 "실수를 언제 발견하게 해주는가"의 차이다.

그런데 아까 TDZ 문제에서 이상한 점이 하나 있었다. 엔진은 블록 안의 `foo`와 바깥의 `foo` 중 어느 쪽을 참조할지 어떻게 정했을까? 다음 글에서 이 검색 규칙을 다룬다. → [스코프 체인은 어떻게 만들어지는가](/javascript/06-scope-chain)
