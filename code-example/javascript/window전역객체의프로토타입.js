// =========================
// Browser: window 전역객체
// =========================

/* 이해한 팩트 정리해보기
1. 전역객체도 결국은 객체이므로 조상은 Object.prototype이다.
2. 엔진은 Object.prototype을 태초에 만들고 전역객체를 생성함과 동시에 전역객체의 내부 프로퍼티로 빌트인 함수들을 만든다.
3. 빌트인 함수들(Function,Promise,Object등)이 만들어질 때 Object.prototype을 제외한
Function.prototype등 빌트인 생성자함수의 프로토타입도 만들어진다.
4. node의 global과 달리 브라우저의 window는 DOM/이벤트 처리를 위해 체인이 길다.
   (window -> Window.prototype -> WindowProperties -> EventTarget.prototype -> Object.prototype)
*/


/**
 * ============================================================================
 * [브라우저 전역 객체(window) 코어 개념 정리 노트]
 * ============================================================================
 */

// ----------------------------------------------------------------------------
// 팩트 1. 전역 객체의 최종 조상은 Object.prototype이다. (단, 체인이 길다)
// ----------------------------------------------------------------------------
// window 역시 결국은 하나의 객체 인스턴스이므로 최종 조상은 Object.prototype이다.
// 단, node의 global이 한두 단계 만에 Object.prototype에 도달하는 것과 달리,
// window는 DOM/이벤트 처리를 위한 여러 단계를 거쳐서 도달한다.
// window -> Window.prototype -> WindowProperties -> EventTarget.prototype -> Object.prototype
const w1 = Object.getPrototypeOf(window);  // Window.prototype
const w2 = Object.getPrototypeOf(w1);      // WindowProperties
const w3 = Object.getPrototypeOf(w2);      // EventTarget.prototype
const w4 = Object.getPrototypeOf(w3);      // Object.prototype

console.log("팩트 1 확인 (직속 부모가 Object.prototype인가?):", w1 === Object.prototype); // false!
console.log("팩트 1 확인 (여러 단계 위에 Object.prototype이 있는가?):", w4 === Object.prototype); // true!
