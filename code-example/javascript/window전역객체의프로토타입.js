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

// ----------------------------------------------------------------------------
// 팩트 2. 엔진의 초기화 순서와 빌트인 함수 할당
// ----------------------------------------------------------------------------
// 1) 자바스크립트 엔진은 태초에 'Object.prototype'을 메모리에 가장 먼저 생성한다.
// 2) 이후 전역 객체(window)를 생성하여 체인을 연결한다.
// 3) 전역 객체 생성 직후, 누구나 접근할 수 있는 '일반 공개 프로퍼티'로 Object,
//    Function, Promise 등의 빌트인 생성자 함수들을 만들어 전역 객체 안에 할당한다.
console.log("팩트 2 확인 (Object):", window.Object === Object);   // 출력: true
console.log("팩트 2 확인 (Promise):", window.Promise === Promise); // 출력: true

// ----------------------------------------------------------------------------
// 팩트 3. 빌트인 생성자 함수의 프로토타입 생성 및 연결
// ----------------------------------------------------------------------------
// Function, Promise 등 빌트인 함수들이 만들어질 때 Function.prototype 등
// 각자의 프로토타입 객체도 함께 만들진다.
// 단, Object 생성자 함수가 전역 프로퍼티로 할당될 때는, 새 프로토타입을 만들지 않고
// 이미 1단계에서 만들어져 있던 태초의 'Object.prototype'을 가리키도록 연결선만 이어준다.
console.log("팩트 3 확인:", Object.prototype === window.Object.prototype); // 출력: true

// ----------------------------------------------------------------------------
// 팩트 4. 브라우저 전역 객체의 길고 복잡한 프로토타입 체인
// ----------------------------------------------------------------------------
// Node.js의 global 객체는 브라우저 API가 없는 순수 런타임 환경이므로
// Object.prototype으로 직행하는 매우 짧은 체인을 가진다. 반면 브라우저의 window는
// DOM 조작 및 이벤트 처리(addEventListener 등)를 위해 EventTarget을 상속받아야 하므로
// 프로토타입 체인이 길고 복잡하다.
/* [window] -> [Window.prototype] -> [WindowProperties] -> [EventTarget.prototype] -> [Object.prototype]
   이처럼 window는 EventTarget을 상속받기 때문에 addEventListener, dispatchEvent 같은
   이벤트 메서드를 그대로 사용할 수 있다. */
console.log("팩트 4 확인 (체인 각 단계의 정체):",
  w1.constructor.name, // 'Window'
  w3.constructor.name  // 'EventTarget'
);