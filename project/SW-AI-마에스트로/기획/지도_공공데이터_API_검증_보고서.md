# 산책온 MVP 핵심 데이터 5종 — API/데이터 실증 검증 보고서

> 작성 기준: 2026-07-05 · 실제 호출/다운로드 우선, 공식 문서 병행
> 표기 규칙 — **[실호출]** 실제 API 호출·다운로드로 검증 / **[공식문서]** 공식 페이지 명세로 검증 / **[추론]** 미검증 추정
> ToDo_Prompt.md 선정 데이터 5종을 그대로 검증 대상으로 삼음.

---

## 검증에 사용한 키 (ToDo_Prompt.md 제공값)

| 키 | 값(축약) | 실검증 결과 |
| --- | --- | --- |
| TMAP `Vector Map SDK(JS)` | `Qrqf…VCL` | **REST API에서 무효** (INVALID_API_KEY, 아래 참조) |
| 국가숲길 serviceKey | `kzO4…81w==` | **유효 + 국가숲길 서비스(15108060)에 인가됨** (실증됨) |

핵심 사전 결론 2가지(실호출 근거):
1. 제공된 **TMAP 키는 REST 오픈API에서 작동하지 않는다.** JS 지도 SDK 전용 키로 보인다.
2. 제공된 **국가숲길 키는 유효한 공공데이터포털 서비스키이며 국가숲길 POI 서비스에 정상 인가**되어 있다(가비지키=401, 내키=게이트웨이 통과). 다만 현재 제공기관 백엔드가 502 장애 상태다.

---

## 1. TMAP 보행자 경로안내 API

- **공식 URL**
  - 상품: https://openapi.sk.com/products/detail?linkMenuSeq=45 (보행자 경로안내)
  - 엔드포인트: `POST https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1`
  - 명세: https://skopenapi.readme.io/reference/보행자-경로안내
- **현재 사용 가능 여부**: **가능** (게이트웨이·서비스 정상 응답). 단, **제공된 키로는 불가.**
- **실제 호출 성공 여부**: **실패 [실호출]** — `403 INVALID_API_KEY`

**Request 예시 (실제 실행)**
```bash
curl -X POST "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json" \
  -H "Content-Type: application/json" \
  -H "appKey: QrqfJJm26I5kWsKHlI4mA7IX77yOQJ8FasRSmVCL" \
  -d '{"startX":"127.42160915252","startY":"36.35063567056",
       "endX":"127.42219024578","endY":"36.35093577665",
       "startName":"출발","endName":"도착",
       "reqCoordType":"WGS84GEO","resCoordType":"WGS84GEO","startTime":"202607051200","searchOption":"0"}'
```

**Response (실제 응답) [실호출]**
```json
{ "error": { "id": "403", "category": "gw", "code": "INVALID_API_KEY", "message": "Forbidden" } }
```
- 동일 키로 POI 검색(`GET /tmap/pois`), 헤더/쿼리파라미터/Referer 조합 등 **모든 REST 엔드포인트에서 동일하게 `INVALID_API_KEY`** 반환. 즉 특정 상품 미구독이 아니라 **키 자체가 REST 게이트웨이에서 인식되지 않음.**
- `category:"gw"`(gateway)는 요청 형식·엔드포인트는 정확히 도달했고 **키 인증 단계에서 거부**되었음을 의미 → 요청 규격은 올바름, 키만 문제.

**실패 원인 / 해결 방법 / 추가 설정**
- 원인: 제공 키는 `TMAP Vector Map SDK (JS)`용 = **클라이언트(브라우저) 벡터지도 렌더링 전용 키**. 서버-사이드 REST 경로 API용 키가 아니다. **[실호출 근거 + 추론]**
- 해결: https://openapi.sk.com 콘솔 → 해당 앱에 **"보행자 경로안내" 상품(REST)을 추가**하고, 그 앱의 `appKey`를 헤더에 사용. (SK Open API는 앱 단위 appKey에 상품을 구독하는 구조)
- 추가 설정: 서버 호출이므로 도메인/Referer 제약 없는 서버용 앱 키 사용 권장.

**프로젝트에서 사용할 필드** (공식 명세·블로그 실응답 기준 [공식문서])
- 응답은 `FeatureCollection`, 각 `Feature.geometry` = `Point`(주요지점) 또는 `LineString`(경로) → **경로 좌표 = `geometry.coordinates`** ✓
- `properties.facilityType`(노드/링크 물리속성 코드), `properties.totalDistance`, `totalTime`
- `facilityType` 코드(보고서·SK 문서 기재값, **내 키로 실응답 검증은 불가**): `0`일반도로 `1`교량 `2`터널 `3`고가도로 `4`지하도로 `5`교차로통과 `6`철도건널목 `11`건물연결통행로 **`12`보행자도로** `14`지하보도 **`15`육교** **`16`계단** **`17`경사로**
  - → ToDo 요구필드(facilityType, geometry, 경로좌표, 계단(16), 경사로(17), 보행자도로(12)) **문서상 모두 존재**. 단 라이브 응답 검증은 정상 키 확보 후 필요.
- 활용: 관절보호 모드에서 `facilityType==16(계단)/15(육교)` 구간에 가중치 페널티를 부여해 우회 경로 유도(보고서 설계와 일치).
- **무료 사용 여부**: TMAP Open API 무료 제공(과금 상품 별도). 일/월 호출 한도는 콘솔 상품별 상이 — **정확 수치 미확정 [추론]**.
- **제한사항**: 서버용 appKey 필요, 호출 쿼터, 상업 이용시 약관 확인.
- **MVP 활용 가능성**: **높음(단 키 교체 선행 필수).** 보고서가 baseline 선형경로 확보 수단으로 지목한 것은 타당.
- **보고서와 다른 점**: 보고서는 facilityType 활용을 정확히 기술. 차이는 **보고서 내용 오류가 아니라, 지급된 키가 REST용이 아니라는 운영 이슈.**

---

## 2. 전국보행자전용도로표준데이터

- **공식 URL**: https://www.data.go.kr/data/15025443/standard.do
  - 오픈API 엔드포인트: `https://api.data.go.kr/openapi/tn_pubr_public_pedestrian_road_api` **[실호출로 존재 확인]**
- **현재 사용 가능 여부**: **가능** — 파일(CSV·XML·JSON·RDF·XLS) + 오픈API. 갱신 **반기**, 수정일 2026-01-27, 제공 지자체 52개.
- **실제 호출 성공 여부**: **부분 [실호출]** — 엔드포인트 정상 응답, 단 **제공된 국가숲길 키는 이 서비스 미등록**.

**Request 예시 (실제 실행)**
```bash
curl -L "https://api.data.go.kr/openapi/tn_pubr_public_pedestrian_road_api?serviceKey={KEY}&pageNo=1&numOfRows=2&type=json"
```
**Response (실제 응답) [실호출]**
```json
{"response":{"header":{"resultCode":"30","resultMsg":"SERVICE KEY IS NOT REGISTERED ERROR."}}}
```
→ API는 **정상 가동**(표준 `response.header/body` 봉투 반환). `resultCode 30`은 "이 키가 해당 서비스에 활용신청되지 않음"을 뜻함. **별도 활용신청 + 전용 serviceKey 발급 필요.**

**프로젝트에서 사용할 필드** (공식 페이지 그리드 컬럼 실추출 [공식문서])
| ToDo 요구 | 실제 컬럼(영문/국문) | 존재 |
| --- | --- | --- |
| 위도/경도 | `peurBeginLatitude/Longitude`, `peurEndLatitude/Longitude` (시작·종료점) | ✓ |
| 보도폭 | `roadBt` (보행자전용도로폭, m) | ✓ |
| CCTV | `vidoInstallationCo` (영상정보처리기기 설치개수) | ✓ |
| 보안등 | `lmpInstallationCo` (보안등 설치개수) | ✓ |
| 보차분리 여부 | `보차분리여부`(공식 명세에 존재 확인 / 영문 API 필드명은 내 추출 범위 밖 — 미확정) | ✓ |
| (보너스) | `crslkInstallationCo`(횡단보도), `brllBlckInstallationCo`(점자블록), `veReducInstallationCo`(속도저감시설), `prtectInstallationCo`(방호울타리), `vhcleInstallationCo`(차량진입억제말뚝), `safechkDate/Result`(점검) | ✓ |

- **무료 사용 여부**: **무료.**
- **제한사항**: 그리드 파일 다운로드 5만건 제한(전체는 API 사용). API는 활용신청 승인 필요.
- **MVP 활용 가능성**: **매우 높음.** '안전/운동' 지수(보안등·CCTV·보도폭·보차분리)에 직결. 보고서가 지목한 안전 지수 산출 출처로 적합.
- **보고서와 다른 점**: **없음.** 보고서 서술(시종점 위경도, CCTV·보안등 설치개수, 보도폭, 보차분리)과 실제 컬럼이 정확히 일치.

---

## 3. 국가숲길 POI API (한국등산트레킹지원센터)

- **공식 URL**: https://www.data.go.kr/data/15108060/openapi.do
  - **엔드포인트(공식 페이지 HTML에서 실추출)**: `http://apis.data.go.kr/B553662/ntnFrtrlInfoService/getNtnFrtrlInfoList`
- **현재 사용 가능 여부**: **서비스 등록·인가 정상, 그러나 제공기관 백엔드 현재 502 장애.**
- **실제 호출 성공 여부**: **인증 통과 확인 / 데이터 취득 실패(백엔드 502) [실호출]**

**진단 근거 (실호출 매트릭스)**
| 호출 | 결과 | 해석 |
| --- | --- | --- |
| 가비지 키 → 실엔드포인트 | `401 Unauthorized` | 게이트웨이가 키 먼저 검증 |
| **내 키 → `ntnFrtrlInfoService`** | `502 Error forwarding request to backend` | **인증 통과**, 제공기관 원서버 오류 |
| 내 키 → 형제 서비스 `frtrlConvFaciInfoService` | `403 Forbidden` | 미구독 서비스는 차단됨 |
| 내 키 → `poiInfoService`(15097966) | `403 Forbidden` | 다른 데이터셋이라 미인가 |

→ 조합상 **내 키는 정확히 15108060(국가숲길 POI)에만 인가**됨이 증명됨. 502는 순수 제공기관 서버측 일시 장애.

**Request 예시 (실제 실행)**
```bash
curl "http://apis.data.go.kr/B553662/ntnFrtrlInfoService/getNtnFrtrlInfoList?serviceKey={KEY}&pageNo=1&numOfRows=3&type=json"
```
**Response (실제 응답) [실호출]**
```
Error forwarding request to backend server   (HTTP 502, 수 회 재시도 동일)
```

**프로젝트에서 사용할 필드** (공식 페이지 명세 실추출 [공식문서])
- 요청변수: `serviceKey, pageNo, numOfRows, type, frtrlId(숲길식별자), poiId, srchFrtrlNm(숲길명검색), srchPlaceTpeCd(장소유형코드검색)`
- 응답필드: `poiId(관심지점식별자)`, `frtrlId(숲길식별자)`, `frtrlNm(숲길명)`, `plcNm(장소명)`, `plcTypeCd(장소유형코드)`, `aslAltide(해발고도)`, `위도`, `경도`
- → ToDo 요구(POI, 좌표, 숲길 유형) **모두 존재** + 해발고도(경사 참고) 보너스.
- **무료 사용 여부**: **무료** (개발계정 10,000건/기간).
- **제한사항**: **현재 백엔드 502 장애** → 시간차 재시도 또는 제공기관(1566-0025) 문의 필요. 운영계정 트래픽 상향은 활용사례 등록 시.
- **MVP 활용 가능성**: **높음(장애 복구 전제).** 자연풍경/산책 목적 POI·좌표·숲길유형 확보에 적합.
- **보고서와 다른 점**: 출처·필드 정확. 보고서가 인용한 페이지(15108060)도 정확. 실제 엔드포인트명이 `ntnFrtrlInfoService`라는 점만 보고서에 미기재(정상).

---

## 4. 국가소음정보 데이터

검증 대상: **한국환경공단_국가소음정보 도로지점정보** (보고서 Works Cited #16, data.go.kr/15147975)

- **공식 URL**: https://www.data.go.kr/data/15147975/fileData.do
- **현재 사용 가능 여부**: **가능** — CSV 파일, **로그인 없이 다운로드**. 갱신 **연간**(차기 등록 2026-09-03), 제공 한국환경공단.
- **실제 호출 성공 여부**: **성공 [실호출]** — CSV 14,562 bytes, **92개 측정지점 실데이터 다운로드**.

**Request 예시 (실제 실행)**
```bash
curl -H "Referer: https://www.data.go.kr/data/15147975/fileData.do" \
  "https://www.data.go.kr/cmm/cmm/fileDownload.do?atchFileId=FILE_000000003229871&fileDetailSn=1" -o noise.csv
```
**Response (실제 데이터 일부) [실호출]**
```csv
순번,지역,측정지점,지점주소,연도,반기,8시_소음통계레벨10,8시_등가소음,8시_소형,8시_대형,8시_평균차속,
16시_소음통계레벨10,16시_등가소음,...,야간_소음통계레벨10,야간_등가소음,야간_소형,야간_대형,야간_평균차속
1,서울특별시,SK뷰 501동 옆,서울특별시 강남구 역삼동 716-1,2024,상반기,47,43,197,8,35,44,40,165,7,40,45,181,8,38,41,39,127,6,40
3,부산광역시,㈜한국주철관 앞,부산광역시 사하구 신평동 370-19,2024,상반기,48,46,152,38,40,50,54,167,57,45,49,160,48,43,42,39,72,5,50
```

**프로젝트에서 사용할 필드**
| ToDo 요구 | 실제 데이터 | 존재 |
| --- | --- | --- |
| dB | `8시/16시/평균/야간_등가소음(Leq)`, `_소음통계레벨10(L10)` | ✓ (주·야 구분까지) |
| 좌표 | **없음.** 위치는 `측정지점`(명칭) + `지점주소`(도로명/지번 텍스트) 뿐 | **✗** |
| 갱신주기 | 연간 | ✓ (연 1회) |

- **무료 사용 여부**: **무료** (로그인 불필요).
- **제한사항 / 핵심 발견 [실호출]**: **위경도 좌표가 데이터에 없다.** Spatial Join을 위해 `지점주소`를 **지오코딩**해야 좌표화 가능. 또한 표본이 전국 92지점 수준으로 **밀도가 낮아** 블록 단위 소음 태깅에는 보간(IDW/Kriging)만으로 부족할 수 있음.
- **MVP 활용 가능성**: **중간.** dB 자체는 확보되나, 좌표·밀도 한계로 '조용한 거리' 지수는 보완 데이터 병용 필요.
- **보고서와 다른 점 (중요)**:
  - 보고서는 국가소음정보를 "**포인트 기반 dB(좌표) → IDW/Kriging 보간으로 폴리곤화**"한다고 전제한다. 그러나 **실제 도로지점정보 파일에는 좌표가 없어**(주소 텍스트만) 이 전제가 그대로 성립하지 않는다. → 지오코딩 단계가 추가로 필요.
  - **대체안**:
    1. **도로교통소음_격자** (data.go.kr/59394979, 한국부동산원, CSV, "격자단위 소음도") — 격자 기반이라 좌표 매핑에 유리(단, 컬럼 상세는 **미확정 [추론]**, 별도 확인 필요).
    2. **국가소음정보시스템 격자소음지도**(mcee.go.kr, 보고서 #1) 및 지자체 소음지도(서울 3,000여건/월, 대전 야간 무장애 소음지도)로 밀도 보완.

---

## 5. AI Hub 인도보행 데이터

- **공식 URL**: https://aihub.or.kr/aidata/136 (인도보행 영상)
- **현재 사용 가능 여부**: **가능(개방).** 단 **회원가입·로그인 후 다운로드 승인** 필요, **내국인만 신청 가능.**
- **실제 호출 성공 여부**: **미수행 [공식문서]** — 다운로드는 로그인·승인 절차가 필수라 자동 호출 불가. 페이지 메타데이터로 검증.

**데이터 규모/구조 (공식 페이지 [공식문서])**
| 구성 | 규모 | 형태 |
| --- | --- | --- |
| Bounding Box | **35만 장** | 29종 장애물(이동체 13 / 고정체 16) |
| Polygon | **10만 장** | 객체 세그멘테이션 |
| Surface Masking | **5만 장** | 20종 노면 객체(재질·파손 등) |
| Depth Prediction | **17만 장** | 스테레오 카메라 disparity |
| (합계) | 약 67만 장 | — |

**프로젝트에서 사용할 필드**
- Bounding Box ✓ / Segmentation(Polygon·Surface Masking) ✓ / Depth ✓ / 데이터 규모 ✓
- **라이선스**: 내국인 신청 한정, 개인정보 비식별화·민감정보 마스킹. **연구/상업 활용 세부 조건은 AI Hub 표준 이용약관 확인 필요 [추론]**(다운로드 승인 화면에서 최종 확정).
- **무료 사용 여부**: **무료**(가입·승인 조건부).
- **제한사항**: 로그인·다운로드 승인 절차, 분할압축 파일(리눅스 병합), 내국인 한정. 모델 학습(Detectron2/YOLO 파인튜닝)에는 GPU·스토리지 자원 필요.
- **MVP 활용 가능성**: **중간(비전 파이프라인 구축 시 높음).** 노면·장애물·단차 미시 메타데이터 자동추출용. MVP 초기보다 2차 고도화에 적합.
- **보고서와 다른 점**: **없음.** 보고서 수치(BBox 35만, Polygon 10만, Surface 5만, Depth 17만, 장애물 29종)와 공식 페이지가 정확히 일치.

---

## 최종 요약표

| 데이터 | 사용 가능 | API 호출 성공 | MVP 사용 가능 | 비고 |
| --- | :---: | :---: | :---: | --- |
| **TMAP 보행자 경로안내** | ○(서비스) | **✗** | △ | 제공 키가 JS SDK용→REST 무효(INVALID_API_KEY). **서버용 앱키·보행자 상품 구독 필요** |
| **전국보행자전용도로 표준데이터** | ○ | △ | ◎ | API 정상, 제공 키 미등록(resultCode 30). **별도 활용신청 필요**. 요구필드 전부 존재 |
| **국가숲길 POI** | ○ | △ | ○ | **키 유효·인가 확인**, `ntnFrtrlInfoService` 엔드포인트 확정. **제공기관 백엔드 502 장애**로 실데이터 미취득 |
| **국가소음정보(도로지점정보)** | ○ | **○** | △ | **CSV 실다운로드 성공(92지점)**. dB 확보 O, **좌표 없음(주소만)** → 지오코딩/격자데이터 필요 |
| **AI Hub 인도보행** | ○ | — | △ | 로그인·승인·내국인 한정. 규모/구조 보고서와 일치. 2차 고도화용 |

범례: ◎매우높음 ○높음 △조건부 ✗불가 / API 호출 성공 —=해당없음(파일 승인형)

---

## 종합 팩트체크 결론

1. **보고서의 데이터 서술은 대체로 정확하다.** 특히 전국보행자전용도로 표준데이터(필드 완전 일치)와 AI Hub 인도보행(수치 완전 일치)은 실증 결과와 어긋남이 없다.
2. **가장 중요한 실증 이슈 2건**
   - **TMAP 키 문제(운영)**: 제공된 `Vector Map SDK(JS)` 키는 REST 보행자 경로 API에서 100% 거부됨. **서버용 appKey 재발급이 선행되어야** 보고서의 라우팅 파이프라인 1단계가 성립.
   - **국가소음 좌표 부재(설계)**: 보고서의 "포인트 dB→공간보간" 전제와 달리 실제 파일엔 좌표가 없음. **지오코딩 또는 격자소음 데이터로 보완**해야 함.
3. **국가숲길 키·엔드포인트는 실증적으로 유효**하며, 남은 변수는 제공기관 서버(502) 복구뿐이다.
4. 나머지 공공데이터포털 서비스(보행자전용도로 표준데이터)는 **각각 별도 활용신청·serviceKey 발급**이 필요하다(현재 국가숲길 키는 해당 서비스에 미등록).

### 근거 URL
- TMAP 상품/명세: https://openapi.sk.com/products/detail?linkMenuSeq=45 · https://skopenapi.readme.io/reference/보행자-경로안내
- 전국보행자전용도로 표준데이터: https://www.data.go.kr/data/15025443/standard.do · API `https://api.data.go.kr/openapi/tn_pubr_public_pedestrian_road_api`
- 국가숲길 POI: https://www.data.go.kr/data/15108060/openapi.do · API `http://apis.data.go.kr/B553662/ntnFrtrlInfoService/getNtnFrtrlInfoList`
- 국가소음(도로지점정보): https://www.data.go.kr/data/15147975/fileData.do · (대체) 도로교통소음_격자 https://www.data.go.kr/data/59394979/linkedData.do
- AI Hub 인도보행: https://aihub.or.kr/aidata/136
