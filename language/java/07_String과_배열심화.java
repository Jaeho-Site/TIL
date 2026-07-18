/*
============================================================
 정보처리기사 실기 - Java 07. String과 배열 심화
 (2020~2025 기출 유형 분석 반영 / 예제는 기출 변형)
 실행: javac -encoding UTF-8 07_String과_배열심화.java && java Ex07String
============================================================
 [기출 분석 결과 - 배열 응용에서 실제로 나온 것]
  ㆍ순위 구하기: 나보다 큰 값의 개수 + 1          - 유명 기출 패턴
  ㆍ2진수 변환을 "큰 배열"에 담아 앞자리 0까지 출력 (함정)
 [String 3대 포인트]
  1. == 주소 비교 / equals() 내용 비교 (리터럴은 Pool 공유)
  2. String은 불변 - 반환값 안 받으면 아무 일도 없음
  3. substring(begin, end)는 end "미포함"
============================================================
*/
/* [문제 11]용: 참조를 담는 간단한 객체 */
class Box7 {
    int v;
    Box7(int v) { this.v = v; }
}

class Ex07String {

    /* [문제 12]용: 배열은 참조 전달, String은 재대입해도 지역에서만
       (2025년 유형 변형) */
    static void change(String[] arr, String s) {
        arr[0] = s;         // 원본 배열이 바뀜 (참조 전달)
        s = "Y";            // 지역 변수 s만 바뀜 (밖의 s는 그대로)
    }

    public static void main(String[] args) {
        /* -----------------------------------------------
           [문제 1] == vs equals (최다 빈출)
           ----------------------------------------------- */
        String s1 = "java";
        String s2 = "java";
        String s3 = new String("java");
        System.out.println(s1 == s2);           // true  (Pool 공유)
        System.out.println(s1 == s3);           // false (new는 새 객체)
        System.out.println(s1.equals(s3));      // true

        /* -----------------------------------------------
           [문제 2] 불변성 함정 - 반환값을 받아야 바뀐다
           ----------------------------------------------- */
        String up = "hello";
        up.toUpperCase();                       // 반환값 버림 → 그대로
        System.out.println(up);                 // hello
        up = up.toUpperCase();
        System.out.println(up);                 // HELLO

        /* -----------------------------------------------
           [문제 3] 메서드 반환값 추적 (인덱스 표부터)
           "Information"  I(0) n(1) f(2) o(3) r(4) m(5) a(6) t(7) i(8) o(9) n(10)
           ----------------------------------------------- */
        String str = "Information";
        System.out.println(str.length());       // 11
        System.out.println(str.charAt(2));      // f
        System.out.println(str.substring(2, 5));// for (5 미포함)
        System.out.println(str.indexOf('n'));   // 1
        System.out.println(str.lastIndexOf('n'));// 10
        System.out.println(str.replace('n', 'N'));// INformatioN

        /* -----------------------------------------------
           [문제 4] split / trim
           ----------------------------------------------- */
        String csv = "red,green,blue";
        String[] parts = csv.split(",");
        System.out.println(parts.length + " " + parts[1]);  // 3 green
        System.out.println("  hi there  ".trim());          // hi there

        /* -----------------------------------------------
           [문제 5] StringBuilder - 가변, 체이닝 가능
           ----------------------------------------------- */
        StringBuilder sb = new StringBuilder("abc");
        sb.append("de").reverse();
        System.out.println(sb);                 // edcba

        /* -----------------------------------------------
           [문제 6] 문자열 ↔ 숫자
           ----------------------------------------------- */
        System.out.println(Integer.parseInt("100") + 23);   // 123
        System.out.println(String.valueOf(45) + 6);         // 456

        /* -----------------------------------------------
           [문제 7] 가변 2차원 배열 합 - 행마다 length가 다르다
           1 + (2+3) + (4+5+6) = 21
           ----------------------------------------------- */
        int[][] jag = { {1}, {2, 3}, {4, 5, 6} };
        int sum = 0;
        for (int i = 0; i < jag.length; i++)
            for (int j = 0; j < jag[i].length; j++)
                sum += jag[i][j];
        System.out.println(sum);                // 21

        /* -----------------------------------------------
           [문제 8] 배열은 참조 - 대입(=)은 같은 배열 공유
           ----------------------------------------------- */
        int[] a = {1, 2, 3};
        int[] b = a;
        b[0] = 99;
        System.out.println(a[0]);               // 99

        /* -----------------------------------------------
           [문제 9] 순위 구하기 (기출 변형 - 유명 패턴)
           rank[i] = 1 + (나보다 큰 값의 개수)
           arr = {60, 85, 30, 95, 70}
           60: 85,95,70이 큼 → 4위 / 85: 95 → 2위 / 30: 5위
           95: 1위 / 70: 85,95 → 3위
           출력: 42513 (붙여서!)
           ----------------------------------------------- */
        int[] arr = {60, 85, 30, 95, 70};
        int[] rank = new int[5];
        for (int i = 0; i < 5; i++) {
            rank[i] = 1;
            for (int j = 0; j < 5; j++)
                if (arr[i] < arr[j])
                    rank[i]++;
        }
        for (int k = 0; k < 5; k++)
            System.out.print(rank[k]);          // 42513
        System.out.println();

        /* -----------------------------------------------
           [문제 10] 2진 변환 + 앞자리 0 출력 함정 (기출 변형)
           n=12 → a[0]=0, a[1]=0, a[2]=1, a[3]=1 (나머지 기본값 0)
           i=5부터 0까지 "배열 전체"를 역순 출력하므로
           앞의 0들도 그대로 나온다: 001100 (1100 아님!)
           ----------------------------------------------- */
        int[] bits = new int[6];
        int n = 12, i2 = 0;
        while (n > 0) {
            bits[i2++] = n % 2;
            n /= 2;
        }
        for (int k = 5; k >= 0; k--)
            System.out.print(bits[k]);          // 001100
        System.out.println();

        /* -----------------------------------------------
           [문제 11] 객체 배열의 참조 교환 (2025년 유형 변형)
           배열 칸에는 "객체의 주소"가 들어 있다.
           ① t=arr[2](→box3), arr[2]=arr[0](→box1), arr[0]=t
              → 배열 칸만 바뀌고 box1~3 자체는 그대로!
           ② arr[1].v = arr[2].v → arr[2]는 지금 box1 → box2.v = 1
           box1.v=1, box2.v=1, box3.v=3 → 113
           "배열 슬롯 교환"과 "객체 필드 수정"을 구분하는 것이 전부.
           ----------------------------------------------- */
        Box7 box1 = new Box7(1);
        Box7 box2 = new Box7(2);
        Box7 box3 = new Box7(3);
        Box7[] boxes = {box1, box2, box3};
        Box7 t = boxes[2];
        boxes[2] = boxes[0];
        boxes[0] = t;
        boxes[1].v = boxes[2].v;
        System.out.println("" + box1.v + box2.v + box3.v);  // 113

        /* -----------------------------------------------
           [문제 12] String[] vs String 전달 (2025년 유형 변형)
           change(strArr, s2):
           strArr[0] = "Q"  → 원본 배열 수정됨
           s = "Y"          → 밖의 s2는 여전히 "Q"
           출력: strArr[0] + s2 = "Q" + "Q" = QQ
           ----------------------------------------------- */
        String[] strArr = {"P"};
        String s4 = "Q";
        change(strArr, s4);
        System.out.println(strArr[0] + s4);     // QQ
    }
}

/*
============================================================
 [전체 정답 모음]
 true / false / true / hello / HELLO / 11 / f / for / 1 / 10
 INformatioN / 3 green / hi there / edcba / 123 / 456 / 21 / 99
 42513 / 001100 / 113 / QQ

 [시험장 체크리스트]
 1. 리터럴끼리 ==는 true, new가 끼면 false, equals는 내용
 2. String 메서드는 반환값을 받는지부터 확인
 3. 순위 패턴: 1에서 시작해 "나보다 큰 값"마다 +1
 4. 2진 변환에서 배열 크기 > 비트 수면 앞자리 0까지 출력된다
 5. 배열/객체 인수는 원본 수정 가능, String·기본형 재대입은 지역만
 6. 객체 배열 문제는 "배열 칸의 화살표"와 "객체 상자"를 나눠 그려라
    (배열 int[]에 ==를 쓰면 주소 비교 - 내용 같아도 false)
============================================================
*/
