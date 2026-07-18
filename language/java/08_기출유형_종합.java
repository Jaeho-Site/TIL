/*
============================================================
 정보처리기사 실기 - Java 08. 기출 유형 종합
 (2020~2025 기출 유형 분석 반영 / 예제는 기출 변형)
 실행: javac -encoding UTF-8 08_기출유형_종합.java && java Ex08Final
============================================================
 [기출 분석 결과 - 반복 출제된 4대 패턴]
  1. 싱글톤: static 인스턴스 1개 공유 → 카운트 전부 누적
  2. 반복문 + 조건부 서식 출력 (숫자 사이 기호 끼워넣기)
  3. 재귀 추적 (홀짝 세기, 분할하며 Math.max)  - 2025년 신경향
  4. 객체/배열 참조 전달 → 원본 수정
============================================================
*/

/* ---------------------------------------------------
   [문제 1] 싱글톤 (기출 변형)
   get()은 최초 1회만 new, 이후 같은 객체 반환
   → l1, l2는 "같은 객체" → log() 5번 전부 한 곳에 누적
   --------------------------------------------------- */
class Logger {
    private static Logger inst = null;
    private int cnt = 0;

    public static Logger get() {
        if (inst == null)
            inst = new Logger();
        return inst;
    }
    public void log() { cnt++; }
    public int count() { return cnt; }
}

class Ex08Final {

    /* ---------------------------------------------------
       [문제 3] 재귀 - n까지의 홀수 개수
       홀수면 f(n-1)+1, 짝수면 f(n-1)
       f(7): 홀수 1,3,5,7 → 4
       --------------------------------------------------- */
    static int oddCount(int n) {
        if (n <= 1) return n;
        if (n % 2 == 1) return oddCount(n - 1) + 1;
        return oddCount(n - 1);
    }

    /* ---------------------------------------------------
       [문제 4] 배열 참조 전달 - 원본 수정
       --------------------------------------------------- */
    static void doubleAll(int[] arr) {
        for (int i = 0; i < arr.length; i++)
            arr[i] *= 2;
    }

    /* ---------------------------------------------------
       [문제 5] 분할 재귀 + Math.max (2025년 유형 변형 - 신경향)
       f(st, end): st>=end면 0, 아니면 mid 값 + 좌우 중 큰 쪽
       data = {2, 9, 4, 7}, f(0,3):
         mid=1, a[1]=9
         좌 f(0,1): mid=0, a[0]=2 + max(f(0,0), f(1,1)) = 2+0 = 2
         우 f(2,3): mid=2, a[2]=4 + max(f(2,2), f(3,3)) = 4+0 = 4
         → 9 + max(2, 4) = 13
       호출 트리를 그리고 "말단(st>=end)=0"부터 위로 채운다.
       --------------------------------------------------- */
    static int func(int[] a, int st, int end) {
        if (st >= end) return 0;
        int mid = (st + end) / 2;
        return a[mid] + Math.max(func(a, st, mid), func(a, mid + 1, end));
    }

    public static void main(String[] args) {
        /* [문제 1] 실행: log 5번 → 5 */
        Logger l1 = Logger.get();
        l1.log();
        l1.log();
        Logger l2 = Logger.get();
        l2.log();
        l2.log();
        l2.log();
        System.out.println(l1.count());         // 5
        System.out.println(l1 == l2);           // true (같은 객체)

        /* -----------------------------------------------
           [문제 2] 반복문 + 조건부 서식 출력 (기출 변형)
           i=1~4를 누적하며 출력하되,
           마지막(i==4)에는 "=합계", 그 외에는 "+"를 붙인다
           출력: 1+2+3+4=10  (한 줄로!)
           ----------------------------------------------- */
        int j = 0;
        for (int i = 1; i <= 4; i++) {
            j += i;
            System.out.print(i);
            if (i == 4) {
                System.out.print("=");
                System.out.print(j);
            } else {
                System.out.print("+");
            }
        }
        System.out.println();                   // 1+2+3+4=10

        /* [문제 3] */
        System.out.println(oddCount(7));        // 4

        /* [문제 4] */
        int[] nums = {1, 2, 3};
        doubleAll(nums);
        System.out.println(nums[0] + " " + nums[2]);    // 2 6

        /* [문제 5] */
        int[] data = {2, 9, 4, 7};
        System.out.println(func(data, 0, data.length - 1));    // 13

        /* -----------------------------------------------
           [문제 6] 상속 + static + 오버라이딩 총정리
           new B8() 2번: 각각 "P"(부모 먼저) "B" → PBPB
           total은 static 공유 → 2
           obj.name()은 실제 객체 → B클래스
           ----------------------------------------------- */
        A8 obj = new B8();
        new B8();
        System.out.println();                   // PBPB
        System.out.println(B8.total);           // 2
        System.out.println(obj.name());         // B클래스
    }
}

class A8 {
    A8() { System.out.print("P"); }
    String name() { return "A클래스"; }
}
class B8 extends A8 {
    static int total = 0;
    B8() { System.out.print("B"); total++; }
    String name() { return "B클래스"; }
}

/*
============================================================
 [전체 정답 모음]
 5 / true / 1+2+3+4=10 / 4 / 2 6 / 13 / PBPB / 2 / B클래스

 [시험장 최종 체크리스트 - Java 전체 요약]
 1. 싱글톤이 보이면 "전부 같은 객체, 카운트 총합"
 2. 서식 출력 문제는 print/println 구분 + 기호("+", "=")의
    위치까지 답안에 정확히 (부분 점수 없음!)
 3. 분할 재귀는 호출 트리 그림 - 말단 반환값부터 위로
 4. 생성자 순서 부모→자식, static은 공유, 메서드는 실제 객체
============================================================
*/
