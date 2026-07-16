/*
============================================================
 정보처리기사 실기 - Java 06. 예외 처리
 (2020~2025 기출 유형 분석 반영 / 예제는 기출 변형)
 실행: javac -encoding UTF-8 06_예외처리.java && java Ex06Exception
============================================================
 [기출 분석 결과 - 2025년 1회에도 출제된 최신 단골]
  ㆍcatch를 4~5개 나열해 두고 "몇 번째 catch가 잡는가" + finally
  ㆍ발생 예외 이름 자체를 답으로 요구하기도 함
 [실행 규칙 - 출력 순서 문제의 전부]
  1. 예외 발생 즉시 try 탈출 (아래 줄 실행 안 함)
  2. 위에서부터 검사해 맞는 catch "하나만" 실행
  3. finally는 무조건 (return보다도 먼저)
  4. catch 순서는 자식 → 부모 (거꾸로면 컴파일 에러)
 [예외 이름 - 용어 답안 대비]
  ArithmeticException(0 나누기) / ArrayIndexOutOfBoundsException
  NullPointerException / ClassCastException / NumberFormatException
============================================================
*/
class Ex06Exception {

    /* [문제 3]용: try의 return보다 finally가 먼저 */
    static int returnTest() {
        try {
            return 1;
        } finally {
            System.out.print("F");
        }
    }

    /* [문제 4]용: throw(발생) / throws(떠넘김 선언) */
    static void validate(int age) throws Exception {
        if (age < 0)
            throw new Exception("나이 오류");
        System.out.print("OK ");
    }

    public static void main(String[] args) {
        /* -----------------------------------------------
           [문제 1] 기본 실행 순서
           "A" → 10/0에서 예외 → "B" 건너뜀 → catch "C" → finally "D"
           → 처리 완료 후 계속 "E"  ⇒  ACDE
           ----------------------------------------------- */
        try {
            System.out.print("A");
            int r = 10 / 0;
            System.out.print("B");
        } catch (ArithmeticException e) {
            System.out.print("C");
        } finally {
            System.out.print("D");
        }
        System.out.println("E");                // ACDE

        /* -----------------------------------------------
           [문제 2] catch 여러 개 나열 (2025년 유형 변형)
           arr[4] = 10 / 2;
           ① 10/2는 정상(5) - 산술 예외 아님! (함정)
           ② arr[4]가 범위 초과 → ArrayIndexOutOfBoundsException
           ③ 위에서부터: Arithmetic(불일치) → ArrayIndex(일치!) "C"
           ④ 아래 catch들은 건너뜀 → finally "E"
           답: CE
           ----------------------------------------------- */
        int[] arr = new int[3];
        try {
            arr[4] = 10 / 2;
            System.out.print("A");
        } catch (ArithmeticException e) {
            System.out.print("B");
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.print("C");
        } catch (NumberFormatException e) {
            System.out.print("D");
        } catch (Exception e) {                  // 부모는 항상 마지막
            System.out.print("X");
        } finally {
            System.out.print("E");
        }
        System.out.println();                    // CE

        /* [문제 3] F 출력 후 1 반환 → F1 */
        System.out.println(returnTest());        // F1

        /* -----------------------------------------------
           [문제 4] throw / throws
           validate(20) → "OK", validate(-1) → 예외 → catch로 점프
           ----------------------------------------------- */
        try {
            validate(20);
            validate(-1);
            System.out.print("도달불가 ");
        } catch (Exception e) {
            System.out.println(e.getMessage());  // OK 나이 오류
        }

        /* -----------------------------------------------
           [문제 5] 정리: catch가 받아주면 프로그램은 계속 진행,
           아무도 안 받으면 비정상 종료 + 스택트레이스
           ----------------------------------------------- */
        System.out.println("정상 종료");
    }
}

/*
============================================================
 [전체 정답 모음]
 ACDE / CE / F1 / OK 나이 오류 / 정상 종료

 [시험장 체크리스트]
 1. 예외 발생 줄에 X표 - try의 나머지는 전부 무시
 2. catch 나열형은 "무슨 예외인지"부터 정확히 판정
    (10/2처럼 멀쩡한 연산을 섞어 산술 예외로 착각하게 만든다)
 3. finally는 무조건 + return보다 먼저
 4. throw는 발생, throws는 선언 - 철자 s 하나 차이
============================================================
*/
