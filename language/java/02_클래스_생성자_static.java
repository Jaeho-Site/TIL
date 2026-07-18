/*
============================================================
 정보처리기사 실기 - Java 02. 클래스 / 생성자 / static
 (2020~2025 기출 유형 분석 반영 / 예제는 기출 변형)
 실행: javac -encoding UTF-8 02_클래스_생성자_static.java && java Ex02Class
============================================================
 [기출 분석 결과 - 클래스 단원에서 실제로 나온 것]
  ㆍstatic 필드 공유/누적 (싱글톤 포함 - 08장에서 종합)
  ㆍ생성자로 초기화 → 밖에서 필드 재대입 → 메서드 호출 순서 추적
  ㆍthis(), 초기화 블록의 실행 순서
============================================================
*/

/* [문제 1] static 카운터 - 모든 객체가 공유하며 누적 */
class CounterEx {
    static int count = 0;   // 클래스에 1개
    int id;                 // 객체마다 1개
    CounterEx() {
        count++;
        id = count;
    }
}

/* [문제 2] 초기화 실행 순서 (기출 유형)
   static 블록: 클래스 최초 사용 시 1회
   인스턴스 블록 → 생성자: 객체 생성 때마다
   new 2번 → 1 2 3 2 3 */
class InitOrder {
    static { System.out.print("1"); }
    { System.out.print("2"); }
    InitOrder() { System.out.print("3"); }
}

/* [문제 3] this()로 생성자 체이닝
   Score() → this(60)이 먼저 실행(B) → 본문(A) → "BA", value=60 */
class Score {
    int value;
    Score() {
        this(60);
        System.out.print("A");
    }
    Score(int v) {
        value = v;
        System.out.print("B");
    }
}

/* ---------------------------------------------------
   [문제 4] 필드 재대입 후 메서드 호출 (기출 변형 - 단골)
   ① new Acc(2) → this.a = 2
   ② obj.a = 4  → 밖에서 필드를 덮어씀! (함정의 핵심)
   ③ obj.func() 실행 시점의 a는 4:
      b = 2 + 4*1 + 4*2 + 4*3 = 26
      return a + b = 30
   ④ obj.a + b = 4 + 30 = 34
   "생성자 값이 아니라 호출 시점의 필드 값"으로 계산한다.
   --------------------------------------------------- */
class Acc {
    int a;
    Acc(int a) { this.a = a; }
    int func() {
        int b = 2;
        for (int i = 1; i < a; i++)
            b += a * i;
        return a + b;
    }
}

/* [문제 5] static 메서드의 제약 */
class Calc {
    static int base = 10;
    int bonus = 5;
    static int addBase(int n) {
        return n + base;        // static끼리 OK
        // return n + bonus;    // 컴파일 에러: 인스턴스 멤버 접근 불가
    }
    int addAll(int n) {
        return n + base + bonus;
    }
}

class Ex02Class {
    public static void main(String[] args) {
        /* [문제 1] */
        CounterEx c1 = new CounterEx();
        CounterEx c2 = new CounterEx();
        CounterEx c3 = new CounterEx();
        System.out.println(CounterEx.count);        // 3
        System.out.println(c1.id + " " + c3.id);    // 1 3

        /* [문제 2] */
        new InitOrder();
        new InitOrder();
        System.out.println();                       // 12323

        /* [문제 3] */
        Score s = new Score();
        System.out.println(" " + s.value);          // BA 60

        /* [문제 4] */
        Acc obj = new Acc(2);
        obj.a = 4;
        int b = obj.func();
        System.out.println(obj.a + b);              // 34

        /* [문제 5] */
        System.out.println(Calc.addBase(1));        // 11
        System.out.println(new Calc().addAll(1));   // 16
    }
}

/*
============================================================
 [전체 정답 모음]
 3 / 1 3 / 12323 / BA 60 / 34 / 11 / 16

 [시험장 체크리스트]
 1. static 필드 = 전 객체 공유·누적
 2. 순서: static블록(1회) → 인스턴스블록 → 생성자(매번)
 3. this(...)로 호출된 생성자가 "먼저" 끝난다
 4. 생성자 이후 필드를 재대입했다면, 메서드는 "재대입된 값"으로
    계산한다 - 필드의 최신 값을 추적표에 유지할 것
============================================================
*/
