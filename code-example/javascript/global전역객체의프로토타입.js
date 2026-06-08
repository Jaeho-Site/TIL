// =========================
// Node.js: global
// =========================

/* 이해한 팩트 정리해보기
1. 전역객체도 결국은 객체이므로 조상은 Object.prototoype이다.
2. 엔진은 Object.prototoype을 태초에 만들고 전역객체를 생성함과 동시에 전역객체의 내부 프로퍼티로 빌트인 함수들을 만든다.
3. 빌트인 함수들(Function,Promise,Object등)이 만들어질 때 Object.prototype을 제외한 
Function.prototype등 빌트인 생성자함수의 프로토타입도 만들어진다.
4. window와 달리 node에서의 global전역 객체는 체인이 짧다. 브라우저 api가 아니므로 받아야할 체인이 크지 않음(빌트인 함수들을 담아두는 용도)
*/

/**
 * ============================================================================
 * [Node.js 전역 객체(global) 코어 개념 정리 노트]
 * ============================================================================
 */

// ----------------------------------------------------------------------------
// 팩트 1. 전역 객체의 직속 조상은 Object.prototype이다.
// ----------------------------------------------------------------------------
// 전역 객체(global)의 최종 조상은 Object.prototype이 맞다. 
// 단, V8 엔진의 특성상 global은 껍데기인 프록시(Global Proxy) 객체이므로, 
// Object.prototype으로 직행하지 않고 내부 전역 객체(Global Object)를 한 단계 거쳐서 도달한다.
// 전역 객체(global) 역시 결국은 하나의 객체 인스턴스입니다.
const g1 = Object.getPrototypeOf(global); // 내부 Global Object
const g2 = Object.getPrototypeOf(g1);     // Object.prototype

console.log("팩트 1 확인 (직속 부모는 Object.prototype인가?):", g1 === Object.prototype); // false!
console.log("팩트 1 확인 (그 위의 할아버지가 Object.prototype인가?):", g2 === Object.prototype); // true!

// ----------------------------------------------------------------------------
// 팩트 2. 엔진의 초기화 순서와 빌트인 함수 할당
// ----------------------------------------------------------------------------
// 1) 자바스크립트 엔진은 태초에 'Object.prototype'을 메모리에 가장 먼저 생성합니다.
// 2) 이후 전역 객체(global)를 생성하여 Object.prototype과 체인을 연결합니다.
// 3) 전역 객체 생성 직후, 누구나 접근할 수 있는 '일반 공개 프로퍼티'로 Object, 
//    Function, Promise 등의 빌트인 생성자 함수들을 만들어 전역 객체 안에 할당합니다.
console.log("팩트 2 확인 (Object):", global.Object === Object);   // 출력: true
console.log("팩트 2 확인 (Promise):", global.Promise === Promise); // 출력: true

// ----------------------------------------------------------------------------
// 팩트 3. 빌트인 생성자 함수의 프로토타입 생성 및 연결
// ----------------------------------------------------------------------------
// Function, Promise 등 빌트인 함수들이 만들어질 때 Function.prototype 등 
// 각자의 프로토타입 객체도 함께 만들어집니다.
// 단, Object 생성자 함수가 전역 프로퍼티로 할당될 때는, 새 프로토타입을 만들지 않고 
// 이미 1단계에서 만들어져 있던 태초의 'Object.prototype'을 가리키도록 연결선만 이어줍니다.
console.log("팩트 3 확인:", Object.prototype === global.Object.prototype); // 출력: true