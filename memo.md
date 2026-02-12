# Memo 기능 정리

## 처리 흐름

1. **메모 등록**
   - 사용자가 작성자/내용 입력 후 등록 버튼 클릭
   - JS에서 AJAX로 `/memo`에 POST 요청
   - FastAPI 라우트에서 DB에 insert, 성공 메시지 반환
   - JS에서 목록을 AJAX로 다시 요청해 갱신

2. **메모 목록 조회(페이징)**
   - JS에서 `/memo/list?page=1` 등으로 AJAX 요청
   - FastAPI 라우트에서 page/size 파라미터로 DB에서 해당 범위만 조회
   - memo_list.html로 목록 fragment 반환, JS가 테이블에 삽입
   - 페이지 버튼 클릭 시 해당 페이지로 AJAX 재요청

3. **메모 삭제**
   - 목록의 삭제 버튼 클릭 시 JS에서 `/memo/{id}` DELETE 요청
   - FastAPI 라우트에서 DB에서 해당 id 삭제
   - JS에서 목록을 AJAX로 다시 요청해 갱신

## 핵심 로직

- **db_oracle.py**
  - 동기 oracledb로 DB 작업, FastAPI에서는 ThreadPoolExecutor로 비동기 래핑
  - select_memos_paged_sync(page, size): Oracle ROW_NUMBER()로 페이징
  - count_memos_sync(): 전체 개수 반환

- **app.py**
  - /memo: 메모 폼 및 전체 페이지
  - /memo/list: AJAX용 목록 fragment, page/size 파라미터 지원
  - /memo (POST): 메모 등록
  - /memo/{id} (DELETE): 메모 삭제

- **static/js/memo.js**
  - 폼 submit, 삭제, 페이지 버튼 클릭 모두 AJAX로 처리
  - 목록 갱신은 loadMemoList(page) 함수로 일원화

- **templates/memo/index.html, memo_list.html**
  - index.html: 폼+목록 테이블, memo_list.html: 목록+페이징 fragment

## 기타
- Oracle DB 페이징: ROW_NUMBER() OVER(ORDER BY ...) 사용, 바인드 변수는 :v_start, :v_end 등으로 지정
- 모든 목록/삭제/등록은 새로고침 없이 AJAX로 동작
- 스타일은 static/css/style.css에서 통일 관리
