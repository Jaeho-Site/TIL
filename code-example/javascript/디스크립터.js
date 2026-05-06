//일반 객체의 __proto__는 접근자 프로퍼티다.
a=Object.getOwnPropertyDescriptor(Object.prototype,'__proto__');

//함수 객체의 prototype은 데이터 프로퍼티다.
b=Object.getOwnPropertyDescriptor(function(){},'prototype');

// Object.getOwnPropertyDescriptor 메서드가 반환한 프로퍼티 어트리뷰트를 객체로 표현한
// 프로퍼티 디스크립터 객체를 살펴볼때, 접근자 프로퍼티와 데이터 프로퍼티 디스크립터 객체의 
// 프로퍼티가 다른것을 알수있다.

console.log(a);

console.log(b);

obj={
    age:20,
    name:'good'
};
console.log(Object.getOwnPropertyDescriptor(obj,'age'));