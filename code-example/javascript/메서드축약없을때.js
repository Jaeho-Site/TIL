var safe = {
  password: "123",
  
  changePassword: function(newPassword) {
    // this는 금고(safe)를 가리킬 것이라고 굳게 믿고 짬
    this.password = newPassword; 
    console.log("비밀번호가 변경되었습니다: " + this.password);
  }
};

// 1. 정상적인 동작
safe.changePassword("456"); // "비밀번호가 변경되었습니다: 456"
console.log(safe.password); // "456" (잘 바뀌었음)

// ---------------------------------------------------------

// 2. 대참사 발생 (누군가 실수로 new를 붙임)
var oops = new safe.changePassword("999"); 
// 출력: "비밀번호가 변경되었습니다: 999" (변경된것 같지만)

// 하지만 금고 비밀번호를 확인해 보면...
console.log(safe.password); // "456" (엥? 안 바뀌었습니다!)

// 그럼 대체 뭐가 바뀐 걸까?
console.log(oops); // { password: "999" }