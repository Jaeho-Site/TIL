/*
============================================================
 정보처리기사 실기 - Java 03. 상속과 오버라이딩
 (2020~2025 기출 유형 분석 반영 / 예제는 기출 변형)
 실행: javac -encoding UTF-8 03_상속과_오버라이딩.java && java Ex03Inherit
============================================================
 [기출 분석 결과 - 상속 단원에서 실제로 나온 것]
  ㆍthis()/super() 체인 + 부모/자식 동명 필드 공존 (배점 큰 단골)
  ㆍ"부모 생성자 안에서 호출한 메서드"도 오버라이딩된 자식 것이
    실행된다 + static 누적                     - 2025년 신경향
  ㆍ재귀 메서드 자체가 오버라이딩되어 재귀 호출도 자식 것으로
 [2대 원칙 - 반드시 암기]
  1. 자식 생성자는 항상 부모 생성자를 "먼저" 실행 (super() 자동)
  2. 필드는 참조 타입 기준(정적), 메서드는 실제 객체 기준(동적)
============================================================
*/

/* [문제 1] 생성자 호출 순서: 부모 → 자식 */
class Parent2 {
    Parent2() { System.out.print("P"); }
}
class Child2 extends Parent2 {
    Child2() { System.out.print("C"); }     // 첫 줄에 super() 숨어 있음
}

/* [문제 2] 필드 vs 메서드 바인딩 (최다 빈출)
   A obj = new B(); obj.x → 1(타입 기준), obj.get() → 2(객체 기준) */
class A3 {
    int x = 1;
    int get() { return x; }
}
class B3 extends A3 {
    int x = 2;
    int get() { return x; }
}

/* ---------------------------------------------------
   [문제 3] this() + super() + 동명 필드 종합 (기출 변형)
   Child3 c = new Child3(); c.getX(); 추적:
   ① 암시적 super() → Parent3() → this(30) → Parent3(int):
      this.x는 "Parent3의 x" = 30
   ② Child3 필드 초기화: Child3의 x = 200
   ③ Child3() 본문: this(700) → Child3(int): Child3의 x = 700
   ④ getX()는 오버라이딩 → Child3의 x → 700
   ★ Parent3의 x(30)와 Child3의 x(700)는 별개로 공존!
      ((Parent3) c).x 로 부모 필드를 꺼내면 30이 나온다.
   --------------------------------------------------- */
class Parent3 {
    int x = 10;
    Parent3() { this(30); }
    Parent3(int x) { this.x = x; }
    int getX() { return x; }
}
class Child3 extends Parent3 {
    int x = 200;
    Child3() { this(700); }
    Child3(int x) { this.x = x; }
    int getX() { return x; }
}

/* ---------------------------------------------------
   [문제 4] 생성자 안의 메서드도 "자식 것"이 실행 (2025년 유형 변형)
   new C4() 추적 (acc는 static 공유):
   ① 부모 P4() 먼저: acc += 1        → acc = 1
      init() 호출 → C4가 오버라이딩했으므로 "자식 init()"!
      acc += 1000                     → acc = 1001
   ② 자식 C4() 본문: acc += 100      → acc = 1101
      init() → 자식 init(): acc += 1000 → acc = 2101
   답: 2101
   ★ 부모 생성자 안이라도 실제 객체가 C4이므로 자식 메서드 실행!
   --------------------------------------------------- */
class P4 {
    static int acc = 0;
    P4() {
        acc += 1;
        init();                 // 오버라이딩된 자식 init()이 실행됨
    }
    void init() { acc += 10; }  // 이 줄은 실행될 기회가 없다
}
class C4 extends P4 {
    C4() {
        acc += 100;
        init();
    }
    @Override
    void init() { acc += 1000; }
}

/* ---------------------------------------------------
   [문제 5] 재귀 메서드의 오버라이딩 (기출 변형 - 고난도)
   Parent5 obj = new Child5(); obj.compute(5);
   compute가 오버라이딩됐으므로 "재귀 호출도 전부 자식 것"!
   자식 규칙: f(n) = f(n-1) - f(n-3), f(n<=1) = n
   f(2) = f(1) - f(-1) = 1 - (-1) = 2   ← 음수 인수도 base로!
   f(3) = f(2) - f(0)  = 2 - 0 = 2
   f(4) = f(3) - f(1)  = 2 - 1 = 1
   f(5) = f(4) - f(2)  = 1 - 2 = -1
   --------------------------------------------------- */
class Parent5 {
    int compute(int n) {
        if (n <= 1) return n;
        return compute(n - 1) + compute(n - 2);
    }
}
class Child5 extends Parent5 {
    int compute(int n) {
        if (n <= 1) return n;
        return compute(n - 1) - compute(n - 3);
    }
}

/* ---------------------------------------------------
   [문제 6] static 메서드는 오버라이딩되지 않는다 (2025년 유형 변형)
   SP ref = new SC();
   ref.x(3)  : 인스턴스 메서드 → 실제 객체(SC) 기준 → 3*10 = 30
   ref.id()  : static 메서드  → "참조 타입(SP)" 기준 → "P" !!
   static은 클래스 소속이라 가려질(hiding) 뿐, 동적 바인딩이 없다.
   --------------------------------------------------- */
class SP {
    int x(int i) { return i * 2; }
    static String id() { return "P"; }
}
class SC extends SP {
    int x(int i) { return i * 10; }         // 오버라이딩 (동적)
    static String id() { return "C"; }      // 하이딩 (정적!)
}

/* [문제 7] super로 부모 멤버 접근 */
class Animal3 {
    String sound() { return "..."; }
}
class Dog3 extends Animal3 {
    String sound() { return "멍멍"; }
    String both() { return super.sound() + sound(); }
}

class Ex03Inherit {
    public static void main(String[] args) {
        /* [문제 1] */
        new Child2();
        System.out.println();                   // PC

        /* [문제 2] */
        A3 obj = new B3();
        System.out.println(obj.x);              // 1
        System.out.println(obj.get());          // 2
        System.out.println(((B3) obj).x);       // 2

        /* [문제 3] */
        Child3 c = new Child3();
        System.out.println(c.getX());           // 700
        System.out.println(((Parent3) c).x);    // 30

        /* [문제 4] */
        new C4();
        System.out.println(P4.acc);             // 2101

        /* [문제 5] */
        Parent5 p5 = new Child5();
        System.out.println(p5.compute(5));      // -1

        /* [문제 6] */
        SP ref = new SC();
        System.out.println(ref.x(3) + ref.id());    // 30P (30C 아님!)

        /* [문제 7] */
        System.out.println(new Dog3().both());  // ...멍멍
    }
}

/*
============================================================
 [전체 정답 모음]
 PC / 1 / 2 / 2 / 700 / 30 / 2101 / -1 / 30P / ...멍멍

 [시험장 체크리스트]
 1. new 자식()이 보이면 "부모 생성자 먼저" - 호출 사슬에 번호
 2. 필드는 참조 타입, 메서드는 실제 객체 (캐스팅하면 필드도 바뀜)
 3. 부모 생성자 "안"의 메서드 호출도 자식 오버라이딩이 이긴다
 4. 오버라이딩된 재귀는 재귀 호출까지 전부 자식 규칙으로 - 표를
    f(1)부터 다시 채워라 (음수 인수는 base 조건으로 그대로 반환)
 5. static 메서드·필드는 오버라이딩이 아니라 하이딩 - 참조 타입!
============================================================
*/
