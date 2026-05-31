// =========================
// Node.js: global
// =========================

const g1 = Object.getPrototypeOf(global);
const g2 = Object.getPrototypeOf(g1);
const g3 = Object.getPrototypeOf(g2);

console.log("g1:", g1); // {}
console.log("g2:", g2); // [Object: null prototype] {}
console.log("g3:", g3); // null

console.log({ g1, g2, g3 }); // { g1: {}, g2: [Object: null prototype] {}, g3: null }

// =========================================================
// [팩트 체크] V8 엔진의 전역 프록시(Global Proxy) 구조
// 0. 크롬 브라우저와 nodejs의 js엔진은 V8을 사용한다. 브라우저의 보안과 메모리 관리 때문에 이렇게 프록시 구조로 관리한다.
// 1. V8 엔진은 컨텍스트 격리와 보안을 위해 전역 객체를 '껍데기(Proxy)'와 '알맹이(내부 객체)'로 나눈다.
// 2. 우리가 코드에서 접근하는 `global` 식별자는 껍데기인 프록시 객체다.
// 3. 따라서 실제 프로토타입 체인은 다음과 같이 내부 객체를 한 번 거쳐간다:
//    [Global Proxy (global)] ➡️ [내부 Global Object (알맹이)] ➡️ [Object.prototype] ➡️ null
// =========================================================