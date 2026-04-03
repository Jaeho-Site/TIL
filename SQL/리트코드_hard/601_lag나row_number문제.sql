-- Stadium : id, visit_date, people
/*
연속된 ID를 가진 행이 3개 이상이고, 각 행의 인원수가 100명 이상인 레코드를 표시하는 솔루션을 작성하세요. 
결과 테이블은 방문일(visit_date)을 기준으로 오름차순으로 정렬되어야 합니다.
*/

-- 정석 풀이
WITH T AS (
    SELECT *,
           -- ID와 순번의 차이를 구해서 연속된 그룹(GR)을 생성
           ID - ROW_NUMBER() OVER (ORDER BY ID) AS GR
    FROM STADIUM
    WHERE PEOPLE >= 100
),
CNT AS (
    SELECT *,
           -- 각 그룹별로 몇 개의 행이 있는지 카운트
           COUNT(*) OVER (PARTITION BY GR) AS GROUP_COUNT
    FROM T
)
SELECT ID, VISIT_DATE, PEOPLE
FROM CNT
WHERE GROUP_COUNT >= 3
ORDER BY VISIT_DATE;


-- 내 풀이
SELECT ID, VISIT_DATE, PEOPLE
FROM (
    SELECT *,
           LAG(PEOPLE, 1) OVER (ORDER BY ID) AS PREV1,
           LAG(PEOPLE, 2) OVER (ORDER BY ID) AS PREV2,
           LEAD(PEOPLE, 1) OVER (ORDER BY ID) AS NEXT1,
           LEAD(PEOPLE, 2) OVER (ORDER BY ID) AS NEXT2
    FROM STADIUM
) AS TEMP
WHERE (PEOPLE >= 100 AND PREV1 >= 100 AND PREV2 >= 100) -- 내가 끝일 때
   OR (PEOPLE >= 100 AND PREV1 >= 100 AND NEXT1 >= 100) -- 내가 중간일 때
   OR (PEOPLE >= 100 AND NEXT1 >= 100 AND NEXT2 >= 100) -- 내가 시작일 때
ORDER BY VISIT_DATE;