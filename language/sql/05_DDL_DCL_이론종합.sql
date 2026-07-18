/*
============================================================
 정보처리기사 실기 - SQL 05. DDL / DCL / DB 이론 종합
 (2021~2026 기출 유형 분석 반영 / 예제는 기출 "변형"이며 동일 문제 아님)
============================================================
 [기출 분석 결과 - 이 유형이 실제로 나온 회차]
  ㆍCREATE TABLE 외래키 제약 5빈칸       - 2026-1 (최신!)
  ㆍON DELETE CASCADE 시나리오          - 2022-3
  ㆍGRANT 기능 서술                     - 2021-3 / REVOKE CASCADE - 2023-2
  ㆍ카디널리티/디그리                    - 2021-1 → 2024-2 재출제
  ㆍ관계대수 기호                        - 2022-3, 2023-3, 2025-2
  ㆍUNION 결과                          - 2023-3
 [명령어 3분류 - 용어 문제 단골]
  DDL: CREATE, ALTER, DROP / DML: INSERT, UPDATE, DELETE (SELECT)
  DCL: GRANT, REVOKE, COMMIT, ROLLBACK
============================================================
*/

-- ---------------------------------------------------
-- [문제 1] CREATE TABLE 외래키 제약 빈칸 (2026-1 유형 변형)
-- 2026-1에서 5빈칸으로 출제된 최신 유형. 구조 통째로 암기!
--
--   CONSTRAINT 제약이름
--     FOREIGN KEY (자식컬럼)
--       REFERENCES 부모테이블 (부모컬럼)
--
-- 빈칸: ①CONSTRAINT ②FOREIGN ③CLUB_ID ④REFERENCES ⑤CID
-- ★ ③은 "이 테이블의" 컬럼, ⑤는 "부모 테이블의" 컬럼 - 서로 이름이
--   달라도 된다는 것을 노린 함정 (2026-1도 TEAM_ID vs TEAM_ID2)
-- ---------------------------------------------------
CREATE TABLE MEMBER (
    MEM_ID   CHAR(5)     NOT NULL,
    MEM_NAME VARCHAR(20) NOT NULL,
    CLUB_ID  CHAR(3)     NOT NULL,
    PRIMARY KEY (MEM_ID),
    CONSTRAINT CLUB_FK              -- ① CONSTRAINT (제약조건에 이름 부여)
      FOREIGN KEY (CLUB_ID)         -- ② FOREIGN  ③ CLUB_ID
        REFERENCES CLUB (CID)       -- ④ REFERENCES  ⑤ CID
);

-- ---------------------------------------------------
-- [문제 2] ON DELETE CASCADE 시나리오 (2022-3 유형 변형)
-- 부모 행을 지우면 참조하던 자식 행도 "연쇄 삭제"
--
-- <학과> A01, B02, C03 (3행)
-- <학생> A01 소속 1명, B02 소속 2명, C03 소속 3명 (6행)
--        학생.학과코드는 학과를 참조, ON DELETE CASCADE
--
-- ① SELECT DISTINCT COUNT(학과코드) FROM 학생 WHERE 학과코드 = 'C03';
--    ★ 함정: COUNT(DISTINCT x)가 아니라 DISTINCT COUNT(x)!
--      COUNT부터 계산(3) → 한 행짜리 결과에 DISTINCT → 그대로 3
-- ② DELETE FROM 학과 WHERE 학과코드 = 'C03';
--    → CASCADE로 학생 3명도 함께 삭제 → 학생은 3행 남음
--    SELECT DISTINCT COUNT(학과코드) FROM 학생;  → 3
-- ---------------------------------------------------
-- 답: ① 3   ② 3

-- ---------------------------------------------------
-- [문제 3] GRANT / REVOKE (2021-3 서술 + 2023-2 CASCADE 변형)
-- GRANT 기능 서술 답: "데이터베이스 관리자가 사용자에게
--                     권한을 부여하는 데 사용하는 명령어"
-- ---------------------------------------------------
GRANT SELECT ON 사원 TO kim;                  -- kim에게 조회 권한 부여
GRANT UPDATE ON 사원 TO kim WITH GRANT OPTION; -- 남에게 재부여할 권한까지
REVOKE SELECT ON 사원 FROM kim;               -- 권한 회수
REVOKE UPDATE ON 사원 FROM kim CASCADE;       -- kim이 재부여한 권한까지 연쇄 회수
-- ★ 2023-2 빈칸 답이 CASCADE - "연쇄 회수" 키워드가 보이면 CASCADE

-- ---------------------------------------------------
-- [문제 4] 카디널리티 / 디그리 (2021-1→2024-2 재출제 유형 변형)
-- 카디널리티(Cardinality) = 튜플(행)의 수
-- 디그리(Degree)          = 속성(열)의 수
-- 암기: "카로(row)" - 카디널리티는 로(행) / 디그리는 컬럼
--
-- <수강> 테이블이 6행 × 4열이라면 → 카디널리티 6, 디그리 4
-- ---------------------------------------------------

-- ---------------------------------------------------
-- [문제 5] 관계대수 기호 (2022-3, 2023-3, 2025-2 유형)
--  σ (시그마) : Select   - 조건에 맞는 "행" 선택 (수평)
--  π (파이)   : Project  - 원하는 "열" 추출 (수직)
--  ⋈          : Join     - 두 릴레이션 결합
--  ÷          : Division - 나누기
--  ∪ / − / × : 합집합 / 차집합 / 교차곱(Cartesian Product)
-- ★ "Join = Cartesian Product 후 Select" 서술도 기출 (2023-3)
-- ---------------------------------------------------

-- ---------------------------------------------------
-- [문제 6] UNION 결과 (2023-3 유형 변형)
-- <R>의 A: 2, 4, 6   /   <S>의 A: 4, 8
-- UNION     : 중복 제거 통합 → 2, 4, 6, 8 (속성명 A, 4튜플)
-- UNION ALL : 중복 포함     → 5튜플
-- ---------------------------------------------------
SELECT A FROM R
UNION
SELECT A FROM S;
-- 답:  A
--      2
--      4
--      6
--      8

/*
============================================================
 [전체 정답 모음]
 문제1: ①CONSTRAINT ②FOREIGN ③CLUB_ID ④REFERENCES ⑤CID
 문제2: ①3 ②3
 문제3: GRANT ~ TO / REVOKE ~ FROM / 연쇄 회수 = CASCADE
 문제4: 카디널리티 6, 디그리 4
 문제5: σ=Select(행), π=Project(열), ⋈=Join, ÷=Division
 문제6: A / 2 / 4 / 6 / 8 (4튜플, UNION ALL이면 5)

 [시험장 체크리스트]
 1. CONSTRAINT 이름 FOREIGN KEY(자식컬럼) REFERENCES 부모(부모컬럼) 통암기
 2. GRANT는 TO, REVOKE는 FROM - 전치사 짝이 빈칸으로 나온다
 3. DISTINCT COUNT(x)는 COUNT(DISTINCT x)와 다르다 - 순서 함정
 4. 카디널리티=행 수, 디그리=열 수 - 매번 헷갈리면 "카로(row)"
 5. UNION은 중복 제거, UNION ALL은 중복 유지
============================================================
*/
