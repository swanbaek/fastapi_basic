
# 오라클 DB 연동을 위한 oracledb 모듈과, 동기 DB 작업을 비동기로 처리하기 위한 ThreadPoolExecutor 사용
import oracledb
from concurrent.futures import ThreadPoolExecutor

# 오라클 DB 연동을 위한 oracledb 모듈과,
# 동기 DB 작업을 비동기로 처리하기 위한 ThreadPoolExecutor 사용.
# oracledb는 비동기(Async) 드라이버를 지원하지 않으므로,
# FastAPI의 이벤트 루프가 DB 작업 때문에 멈추지 않도록
# run_in_executor()를 활용하여 별도의 스레드풀에서 실행한다.

# run_in_executor(): asyncio의 이벤트 루프가 동기(Blocking) 함수를 비동기처럼 실행할 수 있게 해주는 함수.
#FastAPI는 비동기 기반. 근데 Oracle 드라이버 oracledb는 동기 함수만 있음. 이걸 그대로 호출하면 이벤트 루프가 멈춰버림(= 전체 서버 멈춤).
#-> 그래서 run_in_executor()로 동기 작업을 다른 스레드에서 실행시킴
# 즉 :동기 코드를 “비동기처럼” 쓰게 해주는 브릿지 역할


# 오라클 DB 접속 정보
oracle_config = {
    'user': 'c##scott',
    'password': 'tiger',
    'dsn': 'localhost:1521/xe',
}


# 동기 DB 작업을 별도 스레드에서 실행하기 위한 ThreadPoolExecutor 생성
executor = ThreadPoolExecutor()


# 오라클 DB 커넥션 생성 함수 (동기)
def get_connection():
    return oracledb.connect(
        user=oracle_config['user'],
        password=oracle_config['password'],
        dsn=oracle_config['dsn']
    )


# 메모 추가 (동기, DB 직접 접근)
def insert_memo_sync(author, content):
    sql = """
    INSERT INTO memo (id, author, content) VALUES (memo_seq.NEXTVAL, :author, :content)
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, {'author': author, 'content': content})
        conn.commit()
    finally:
        cur.close()
        conn.close()


# 메모 전체 조회 (동기, DB 직접 접근)
# 전체 메모 조회 (페이징 없는 샘플)
def select_memos_sync():
    sql = "SELECT id, author, content FROM memo ORDER BY id DESC"
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return [{'id': r[0], 'author': r[1], 'content': r[2]} for r in rows]
    finally:
        cur.close()
        conn.close()

# 페이징 처리된 메모 조회
def select_memos_paged_sync(page=1, size=10):
    start = (page - 1) * size + 1
    end = page * size
    sql = '''
    SELECT * FROM (
        SELECT id, author, content, ROW_NUMBER() OVER (ORDER BY id DESC) AS rn
        FROM memo
    ) WHERE rn BETWEEN :v_start AND :v_end
    '''
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, {'v_start': start, 'v_end': end})
        rows = cur.fetchall()
        return [{'id': r[0], 'author': r[1], 'content': r[2]} for r in rows]
    finally:
        cur.close()
        conn.close()

# 전체 메모 개수 반환
def count_memos_sync():
    sql = 'SELECT COUNT(*) FROM memo'
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        count = cur.fetchone()[0]
        return count
    finally:
        cur.close()
        conn.close()


# 메모 내용 수정 (동기, DB 직접 접근)
def update_memo_sync(id, content):
    sql = "UPDATE memo SET content = :content WHERE id = :id"
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, {'content': content, 'id': id})
        conn.commit()
    finally:
        cur.close()
        conn.close()


# 메모 삭제 (동기, DB 직접 접근)
def delete_memo_sync(id):
    sql = "DELETE FROM memo WHERE id = :id"
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, {'id': id})
        conn.commit()
    finally:
        cur.close()
        conn.close()


# FastAPI에서 await로 사용할 수 있도록 동기 함수를 비동기로 감싸는 래퍼 함수들
import asyncio

# 메모 추가 (비동기, FastAPI 라우트에서 await로 사용)
async def insert_memo(author, content):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, insert_memo_sync, author, content)

# 메모 전체 조회 (비동기, FastAPI 라우트에서 await로 사용)

# 비동기 전체 메모 조회 (페이징 없는 샘플)
async def select_memos():
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, select_memos_sync)

# 비동기 페이징 메모 조회
async def select_memos_paged(page=1, size=10):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, select_memos_paged_sync, page, size)

# 비동기 전체 메모 개수 반환
async def count_memos():
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, count_memos_sync)

# 메모 수정 (비동기, FastAPI 라우트에서 await로 사용)
async def update_memo(id, content):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, update_memo_sync, id, content)

# 메모 삭제 (비동기, FastAPI 라우트에서 await로 사용)
async def delete_memo(id):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, delete_memo_sync, id)
