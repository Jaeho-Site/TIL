// 1. 객체 리터럴
const obj = { name: 'Gemini' };
console.log(obj.__proto__ === Object.prototype); // true
console.log(Object.prototype.constructor === Object); // true
console.log(obj.constructor === Object); // true

// 2. 배열 리터럴
const arr =[];
console.log(arr.__proto__ === Array.prototype); // true
console.log(Array.prototype.constructor === Array); // true
console.log(arr.constructor === Array); // true

// 3. 함수 리터럴
const func = function() { console.log('hello'); };
// __proto__ 대신 권장되는 표준 메서드 사용
console.log(Object.getPrototypeOf(func) === Function.prototype); // true
console.log(Function.prototype.constructor === Function); // true
console.log(func.constructor === Function); // true

// 4. 정규 표현식 리터럴
const regex = /[a-z]/;
console.log(Object.getPrototypeOf(regex) === RegExp.prototype); // true
console.log(RegExp.prototype.constructor === RegExp); // true
console.log(regex.constructor === RegExp); // true

// 5. 원시 타입 (래퍼 객체로 인한 프로토타입 접근)
const str = "JavaScript";
console.log(str.__proto__ === String.prototype); // true
console.log(str.constructor === String); // true