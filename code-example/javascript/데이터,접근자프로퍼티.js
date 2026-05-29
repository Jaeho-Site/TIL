const person = {}; // 평범한 빈 객체 생성

// ==========================================
// 데이터 프로퍼티와 어트리뷰트 설정
// ==========================================
Object.defineProperty(person, 'name', {
  value: '홍길동',       // [[Value]]에 해당
  writable: false,      // [[Writable]]: false (수정 불가 잠금!)
  enumerable: true,     // [[Enumerable]]: true (반복문 노출 허용)
  configurable: false   // [[Configurable]]: false (삭제 및 설정 변경 불가 잠금!)
});

// ==========================================
// 접근자 프로퍼티 설정
// ==========================================
let _age = 20; // 실제 데이터가 저장될 임시 변수

Object.defineProperty(person, 'ageInfo', {
  // 값을 읽을 때 동작하는 함수 ([[Get]] 내부 슬롯에 바인딩됨)
  get() {
    return `이 사람의 나이는 ${_age}살 입니다.`;
  },
  // 값을 저장할 때 동작하는 함수 ([[Set]] 내부 슬롯에 바인딩됨)
  set(newAge) {
    if (newAge < 0) {
      console.log('🚨 에러: 나이는 0보다 작을 수 없습니다!');
      return;
    }
    _age = newAge;
  },
  enumerable: true,
  configurable: true
});
console.log(person.ageInfo);