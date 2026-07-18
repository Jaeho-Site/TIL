// =========================
// Node.js: global
// =========================

const g1 = Object.getPrototypeOf(global);
const g2 = Object.getPrototypeOf(g1);
const g3 = Object.getPrototypeOf(g2);

console.log("g1:", g1);
console.log("g2:", g2);
console.log("g3:", g3);

console.log({ g1, g2, g3});

// =========================================================
// 사실 1: 빌트인 생성자 함수는 전역 객체의 프로퍼티이다.
// =========================================================

// 우리가 평소에 쓰는 Object, Function은 사실 전역 객체 안에 들어있는 녀석들이다.
console.log(globalThis.Object === Object);     // 출력: true
console.log(globalThis.Function === Function); // 출력: true

// =========================================================
// 사실 2: 전역 객체의 프로토타입 체인 꼭대기에는 Object.prototype이 있다.
// =========================================================

// isPrototypeOf() 메서드는 특정 객체가 체인 상에 존재하는지 확인한다.
// "Object.prototype이 globalThis의 조상님입니까?"
console.log(Object.prototype.isPrototypeOf(globalThis)); // 출력: true

// =========================================================
// 🔍 보너스: 전역 객체의 프로토타입 체인을 직접 거슬러 올라가 보기
// =========================================================

let currentProto = Object.getPrototypeOf(globalThis);
let chain = "globalThis";

// 체인이 null에 도달할 때까지 계속 부모를 찾아 올라간다.
while (currentProto !== null) {
  if (currentProto === Object.prototype) {
    chain += " ➡️ [도착: Object.prototype]";
  } else {
    // 중간에 거치는 브라우저/Node 내부 프로토타입들 (예: Window.prototype)
    chain += " ➡️ (내부 프로토타입)"; 
  }
  currentProto = Object.getPrototypeOf(currentProto);
}

chain += " ➡️ null";
console.log(chain);
// 브라우저 출력 예시: 
// "globalThis ➡️ (내부 프로토타입) ➡️ (내부 프로토타입) ➡️ (내부 프로토타입) ➡️ [도착: Object.prototype] ➡️ null"