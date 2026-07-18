/*
============================================================
 정보처리기사 실기 - Java 04. 다형성 / 오버로딩 / 형변환
 (2020~2025 기출 유형 분석 반영 / 예제는 기출 변형)
 실행: javac -encoding UTF-8 04_다형성과_형변환.java && java Ex04Poly
============================================================
 [기출 분석 결과 - 다형성 단원에서 실제로 나온 것]
  ㆍ추상클래스 + "매개변수 다른 동명 메서드"(오버로딩) 함정
  ㆍ오버로딩(int/String 버전) + 재귀 조합        - 2025년 신경향
  ㆍ부모 타입 변수의 메서드 호출 → 실제 객체 것 실행
 [판별 순서 - 이것만 지키면 안 틀린다]
  ① 인자 개수/타입으로 "어떤 시그니처인지" 확정 (컴파일 타임)
  ② 그 시그니처가 자식에서 오버라이딩됐는지 확인 (런타임)
============================================================
*/

/* ---------------------------------------------------
   [문제 1] 추상클래스 + 오버로딩 함정 (기출 변형)
   Device d = new Phone("Nova"); d.info();
   ① info() ← 인자 없는 호출 → Device의 info() 시그니처
   ② Phone에는 info(String), info(char[])뿐 → 오버라이딩 아님!
   ③ Device의 info() 실행 → name은 Device의 필드
      (생성자에서 name = super.name = val 로 양쪽 모두 "Nova")
   답: Device : Nova
   --------------------------------------------------- */
abstract class Device {
    String name;
    abstract public String info(String val);
    public String info() {
        return "Device : " + name;
    }
}
class Phone extends Device {
    private String name;                    // Device의 name과 별개
    public Phone(String val) {
        name = super.name = val;
    }
    public String info(String val) {        // 매개변수 다름 → 오버로딩
        return "Phone : " + val;
    }
    public String info(char[] val) {
        return "Phone : " + String.valueOf(val);
    }
}

/* [문제 2] 오버로딩 선택은 "참조 타입" 기준 (컴파일 타임) */
class Shape4 { }
class Circle4 extends Shape4 { }
class Printer4 {
    void print(Shape4 s)  { System.out.println("Shape 버전"); }
    void print(Circle4 c) { System.out.println("Circle 버전"); }
}

/* [문제 3] 업캐스팅/다운캐스팅/instanceof */
class Animal4 {
    void cry() { System.out.println("..."); }
}
class Cat4 extends Animal4 {
    void cry() { System.out.println("야옹"); }
    void scratch() { System.out.println("긁기"); }
}

class Ex04Poly {

    /* ---------------------------------------------------
       [문제 4] 오버로딩 + 재귀 (2025년 유형 변형 - 신경향)
       f(int)    : 팩토리얼 재귀
       f(String) : 숫자로 바꿔 f(n-2) + f(n-1) 호출
       print(f("4")) 추적:
       ① "4"는 String → f(String) 실행 (최초 1회만!)
       ② n=4 → f(2) + f(3) ← 인수가 int이므로 "int 버전" 호출
       ③ f(2)=2! = 2, f(3)=3! = 6 → 2+6 = 8
       ★ String 버전은 처음 한 번만, 내부 재귀는 전부 int 버전
       --------------------------------------------------- */
    static int f(int n) {
        if (n <= 1) return 1;
        return n * f(n - 1);
    }
    static int f(String s) {
        int n = Integer.valueOf(s);
        return f(n - 2) + f(n - 1);
    }

    public static void main(String[] args) {
        /* [문제 1] */
        Device d = new Phone("Nova");
        System.out.println(d.info());           // Device : Nova

        /* [문제 2] 참조 타입이 Shape4 → print(Shape4) 호출 */
        Shape4 x = new Circle4();
        new Printer4().print(x);                // Shape 버전

        /* [문제 3] */
        Animal4 a = new Cat4();                 // 업캐스팅(자동)
        a.cry();                                // 야옹 (실제 객체 기준)
        if (a instanceof Cat4) {
            Cat4 cat = (Cat4) a;                // 다운캐스팅(명시적)
            cat.scratch();                      // 긁기
        }
        System.out.println(a instanceof Animal4);   // true

        /* [문제 4] */
        System.out.println(f("4"));             // 8

        /* -----------------------------------------------
           [문제 5] 다형성 배열 - 요소마다 실제 객체의 메서드
           ----------------------------------------------- */
        Animal4[] zoo = { new Animal4(), new Cat4() };
        for (Animal4 each : zoo)
            each.cry();                         // ... / 야옹
    }
}

/*
============================================================
 [전체 정답 모음]
 Device : Nova / Shape 버전 / 야옹 / 긁기 / true / 8 / ... / 야옹

 [시험장 체크리스트]
 1. 호출 인자부터 본다: 시그니처 확정 → 오버라이딩 여부 확인
 2. 매개변수가 다르면 이름이 같아도 "오버로딩" - 재정의 아님
 3. int/String 오버로딩 + 재귀: 변환 버전은 최초 1회만 실행
 4. 부모 타입 변수로는 부모에 선언된 멤버만 보인다
    (다운캐스팅 전 instanceof 확인)
 5. (2024년 기출) print(Integer)/print(Number)/print(Object)처럼
    래퍼 계층으로 오버로딩된 경우도 "선언 타입" 기준:
    제네릭 T에 담긴 값은 Object로 취급 → print(Object)가 선택된다
============================================================
*/
