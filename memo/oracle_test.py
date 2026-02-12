# pip install oracledb

import oracledb
# Oracle DB 연결 정보
oracle_config = {
    'user': 'c##scott',
    'password': 'tiger',
    'dsn': 'localhost:1521/xe', # 호스트:포트/SID
}

def get_connection():
    return oracledb.connect(
        user=oracle_config['user'],
        password=oracle_config['password'],
        dsn=oracle_config['dsn'])

# 테스트용 INSERT 쿼리
insert_sql = """
INSERT INTO memo (id, author, content) VALUES (memo_seq.NEXTVAL, :author, :content)
"""

def test_oracle_insert():
    try:
        # DB 연결
        conn = get_connection()
        cur = conn.cursor()
        # INSERT 실행
        cur.execute(insert_sql, {'author': '김프로', 'content': '테스트 내용'})
        conn.commit()
        print('Insert 성공!')
    except Exception as e:
        print('오류:', e)
    finally:
        if 'cur' in locals(): #locals()는 현재 함수(또는 스코프) 안에 존재하는 모든 지역 변수들을 딕셔너리 형태로 반환하는 파이썬 내장 함수
            cur.close()
        if 'conn' in locals():
            conn.close()

def test_oracle_select():
    try:
        # DB 연결
        conn = get_connection()
        cur = conn.cursor()
        # SELECT 실행
        cur.execute("SELECT id, author, content FROM memo")
        rows = cur.fetchall()
        for row in rows:
            print(f'ID: {row[0]}, Author: {row[1]}, Content: {row[2]}')
    except Exception as e:
        print('오류:', e)
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def test_oracle_update():
    with get_connection() as conn:
        with conn.cursor() as cur:
            update_sql = "UPDATE memo SET content = :content WHERE id = :id"
            cur.execute(update_sql,{'content':"반갑습니다", 'id':2  })
            conn.commit()
            print('Update 성공!')

def test_oracle_delete():
    with get_connection() as conn:
        with conn.cursor() as cur:
            delete_sql = "DELETE FROM memo WHERE id = :id"
            cur.execute(delete_sql, {'id': 3})
            conn.commit()
            print('Delete 성공!')
if __name__ == '__main__':
    #test_oracle_insert()
    #test_oracle_select()
    #test_oracle_update()
    test_oracle_delete()    
    test_oracle_select()
