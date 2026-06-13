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