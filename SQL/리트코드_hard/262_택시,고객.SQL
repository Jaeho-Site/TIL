-- TRIPS: ID,CLIENT_ID,DRIVER_ID,CITY_ID,STATUS,REQUEST_AT
-- USERS : USER_ID, BANNED, ROLE
/*Day | Cancellation Rate
취소율은 해당일에 차단되지 않은 사용자가 예약한 요청 중 고객 또는 운전자가 취소한 요청 수를 차단되지 않은 사용자가 예약한 전체 요청 수로 나누어 계산합니다. 
2013년 10월 1일부터 2013년 10월 3일까지 매일 최소 한 건 이상의 운행이 기록된 차단되지 않은 사용자(고객과 운전자 모두 차단되지 않은 상태)의 요청 취소율을 구하는 솔루션을 작성하세요. 취소율은 소수점 둘째 자리까지 반올림하세요. 결과 표는 순서에 상관없이 반환하세요. 
*/

-- 사실 영어 해석을 실수해서 빙빙 돌아서 난이도를 더 올려버렸다. BANNED인 경우는 제외해버리면 되는데, BANND와 STATUS 두 조건을 같이 따지다 보니 복잡해짐

-- 정석 풀이
SELECT 
    T.REQUEST_AT AS Day,
    ROUND(
        SUM(CASE WHEN T.STATUS != 'completed' THEN 1 ELSE 0 END) / COUNT(*), 
        2
    ) AS `Cancellation Rate`
FROM TRIPS T
JOIN USERS U1 ON T.CLIENT_ID = U1.USERS_ID AND U1.BANNED = 'No'
JOIN USERS U2 ON T.DRIVER_ID = U2.USERS_ID AND U2.BANNED = 'No'
WHERE T.REQUEST_AT BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY T.REQUEST_AT;


-- 내 풀이
WITH T AS(
    SELECT T.ID,T.REQUEST_AT,
        CASE
            WHEN U1.BANNED='NO' AND U2.BANNED='NO' AND T.STATUS='cancelled_by_client' THEN 1
            WHEN U1.BANNED='NO'AND U2.BANNED='NO' AND T.STATUS='cancelled_by_DRIVER' THEN 1
            ELSE 0
        END AS C_COUNT, -- 승인된 취소 구하기
        CASE      
            WHEN U1.BANNED='YES' OR U2.BANNED='YES'  THEN 0
            ELSE 1
        END AS T_COUNT
    FROM TRIPS T
    JOIN USERS U1 ON T.CLIENT_ID=U1.USERS_ID
    JOIN USERS U2 ON T.DRIVER_ID=U2.USERS_ID
    WHERE REQUEST_AT BETWEEN '2013-10-01' AND '2013-10-03'
)
SELECT REQUEST_AT AS DAY, ROUND(SUM(C_COUNT)/SUM(T_COUNT),2) AS `Cancellation Rate`
FROM T
GROUP BY REQUEST_AT
HAVING ROUND(SUM(C_COUNT)/SUM(T_COUNT),2) IS NOT NULL