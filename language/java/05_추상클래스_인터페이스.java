/*
============================================================
 정보처리기사 실기 - Java 05. 추상 클래스 / 인터페이스
 (2020~2025 기출 유형 분석 반영 / 예제는 기출 변형)
 실행: javac -encoding UTF-8 05_추상클래스_인터페이스.java && java Ex05Abstract
============================================================
 [기출 분석 결과]
  ㆍ추상클래스는 04장의 "오버로딩 함정"과 묶여서 출제가 잦다
  ㆍ추상클래스의 생성자가 자식 생성 시 먼저 실행되는 것도 출제 포인트
  ㆍ인터페이스는 다중 구현 + 타입으로 쓰는 다형성 형태
 [비교 암기표 - 이론 문제로도 출제]
                    추상 클래스           인터페이스
   객체 생성        불가                  불가
   상속/구현        extends (단일)       implements (다중 가능)
   필드             일반 필드 가능        public static final 상수만
   메서드           일반+추상 혼합        추상 (+ default/static)
   생성자           있음                  없음
============================================================
*/

/* ---------------------------------------------------
   [문제 1] 추상 클래스 - 생성자/일반 메서드도 가진다
   new Bird5() → 추상 부모의 생성자 먼저! → "AB"
   --------------------------------------------------- */
abstract class Animal5 {
    Animal5() { System.out.print("A"); }
    abstract void cry();                        // 자식이 반드시 구현
    void breathe() { System.out.print("호흡 "); }
}
class Bird5 extends Animal5 {
    Bird5() { System.out.print("B "); }
    void cry() { System.out.println("짹짹"); }
}

/* ---------------------------------------------------
   [문제 2] 인터페이스 다중 구현
   필드는 자동 public static final, 메서드는 자동 public abstract
   구현 메서드는 반드시 public
   --------------------------------------------------- */
interface Flyable {
    int MAX_ALT = 100;
    void fly();
}
interface Swimmable {
    void swim();
}
class Duck5 implements Flyable, Swimmable {
    public void fly()  { System.out.println("날기 " + MAX_ALT); }
    public void swim() { System.out.println("수영"); }
}

/* ---------------------------------------------------
   [문제 3] 인터페이스 타입 다형성 (기출 유형)
   new는 못 하지만 "타입"으로는 사용 가능
   4*5 + 6*4/2 = 20 + 12 = 32
   --------------------------------------------------- */
interface Shape5 {
    int area();
}
class Rect5 implements Shape5 {
    int w, h;
    Rect5(int w, int h) { this.w = w; this.h = h; }
    public int area() { return w * h; }
}
class Tri5 implements Shape5 {
    int b, h;
    Tri5(int b, int h) { this.b = b; this.h = h; }
    public int area() { return b * h / 2; }
}

/* ---------------------------------------------------
   [문제 4] default 메서드 (Java 8+)
   구현 클래스가 재정의하면 재정의한 쪽 실행 (오버라이딩 규칙 동일)
   --------------------------------------------------- */
interface Greet5 {
    default String hello() { return "hello"; }
}
class Kor5 implements Greet5 {
    public String hello() { return "안녕"; }
}
class Eng5 implements Greet5 { }

/* ---------------------------------------------------
   [문제 5] enum 열거형 (2025년 유형 변형 - 신경향)
   ㆍ상수 하나가 정의될 때마다 생성자가 자동 호출되어 속성 저장
   ㆍvalues()  : 상수들을 "선언 순서대로" 담은 배열 {A, B, C}
   ㆍname()    : 상수 이름 문자열 ("B")
   ㆍordinal() : 선언 순서 번호 (A=0, B=1, C=2)
   --------------------------------------------------- */
enum Grade5 {
    A("GOLD"), B("SILVER"), C("BRONZE");
    private String label;
    Grade5(String label) { this.label = label; }
    public String label() { return label; }
}

/* ---------------------------------------------------
   [문제 6] 람다 + 함수형 인터페이스 (2025년 유형 변형 - 신경향)
   추상 메서드가 1개인 인터페이스는 람다식 (x) -> {...} 으로
   구현 객체를 만들 수 있다. run(c)는 c.apply(5)를 실행:
   ① run(f): 5 > 3 → 예외 발생 → catch → -1
   ② run((n) -> n + 4): 5+4 = 9
   -1 + 9 = 8
   --------------------------------------------------- */
interface Calc5 {
    int apply(int x) throws Exception;
}

/* ---------------------------------------------------
   [문제 7] Runnable 스레드 (기출 변형)
   implements Runnable + run() 구현 → new Thread(객체).start()
   start()가 run()을 실행시킨다 (run()을 직접 부르면 그냥 메서드 호출)
   --------------------------------------------------- */
class Miles5 implements Runnable {
    public void run() {
        System.out.println("주행 시작");
    }
}

class Ex05Abstract {

    /* [문제 6]용: 함수형 인터페이스를 받아 실행하는 메서드 */
    static int run(Calc5 c) {
        try {
            return c.apply(5);
        } catch (Exception e) {
            return -1;
        }
    }

    public static void main(String[] args) throws Exception {
        /* [문제 1] */
        Bird5 bird = new Bird5();               // AB (A 먼저!)
        bird.cry();                             // 짹짹
        // Animal5 a = new Animal5();           // 컴파일 에러: 추상 클래스

        /* [문제 2] */
        Duck5 duck = new Duck5();
        duck.fly();                             // 날기 100
        duck.swim();                            // 수영

        /* [문제 3] */
        Shape5[] shapes = { new Rect5(4, 5), new Tri5(6, 4) };
        int total = 0;
        for (Shape5 s : shapes)
            total += s.area();
        System.out.println(total);              // 32

        /* [문제 4] */
        System.out.println(new Kor5().hello()); // 안녕
        System.out.println(new Eng5().hello()); // hello

        /* [문제 5] enum: values()[1] → B → name "B", label "SILVER" */
        Grade5 g = Grade5.values()[1];
        System.out.println(g.name() + " " + g.label() + " " + g.ordinal());
                                                // B SILVER 1

        /* [문제 6] 람다: -1 + 9 = 8 */
        Calc5 f = (x) -> {
            if (x > 3) throw new Exception();
            return x * 2;
        };
        System.out.println(run(f) + run((n) -> n + 4));     // 8

        /* [문제 7] 스레드 실행 (start → run) */
        Thread t = new Thread(new Miles5());
        t.start();
        t.join();                               // 출력 순서 고정용
                                                // 주행 시작
    }
}

/*
============================================================
 [전체 정답 모음]
 AB 짹짹 / 날기 100 / 수영 / 32 / 안녕 / hello
 B SILVER 1 / 8 / 주행 시작

 [시험장 체크리스트]
 1. 추상클래스·인터페이스 모두 new 불가, 타입으로는 사용 가능
 2. 추상 클래스의 생성자도 자식 생성 시 "먼저" 실행된다
 3. 인터페이스 구현 메서드는 반드시 public
 4. extends는 하나, implements는 여러 개
    (추상클래스 문제가 어렵게 나오면 04장 오버로딩 함정과 결합)
 5. enum: values()는 선언 순서 배열, name()은 이름, ordinal()은 번호
 6. 람다 (x) -> 식 은 "추상 메서드 1개짜리 인터페이스"의 구현체
 7. 빈칸 단골: implements / extends / super / static - 호출 형태를
    보고 거꾸로 추론 (클래스명.메서드() 면 static)
============================================================
*/
