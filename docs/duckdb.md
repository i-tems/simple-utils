# DuckDB 사용 가이드

Iceberg 테이블과 연동 가능한 DuckDB 클라이언트입니다.

## 설치

```bash
pip install simple-utils[iceberg]
```

DuckDB는 자동으로 설치됩니다.

## 기본 사용법

```python
from simple_utils.platform.duckdb import DuckDB

# DuckDB 연결 (Iceberg 확장 자동 로드)
db = DuckDB()

# 커넥션 접근
conn = db.connection
```

## SQL 쿼리 실행

### 기본 쿼리

```python
db = DuckDB()
conn = db.connection

# SELECT 쿼리
result = conn.execute("SELECT * FROM iceberg.my_namespace.my_table").fetchall()

# DataFrame으로 변환
df = conn.execute("SELECT * FROM iceberg.my_namespace.my_table").df()
```

### 집계 쿼리

```python
# 집계 쿼리
result = conn.execute("""
    SELECT
        category,
        COUNT(*) as count,
        SUM(amount) as total
    FROM iceberg.my_namespace.my_table
    GROUP BY category
""").df()
```

### 조건 쿼리

```python
# WHERE 조건
result = conn.execute("""
    SELECT *
    FROM iceberg.my_namespace.my_table
    WHERE amount > 100
    AND created_at >= '2024-01-01'
""").df()
```

## Iceberg 테이블 작업

### 테이블 목록 조회

```python
# 네임스페이스의 테이블 목록
tables = conn.execute("SHOW TABLES FROM iceberg.my_namespace").fetchall()
```

### 테이블 스키마 확인

```python
# 테이블 구조 확인
schema = conn.execute("DESCRIBE iceberg.my_namespace.my_table").df()
```

### 테이블 생성

```python
conn.execute("""
    CREATE TABLE iceberg.my_namespace.new_table (
        id BIGINT,
        name VARCHAR,
        amount DOUBLE
    )
""")
```

### 데이터 삽입

```python
# 직접 삽입
conn.execute("""
    INSERT INTO iceberg.my_namespace.my_table
    VALUES (1, 'Alice', 100.0)
""")

# SELECT로 삽입
conn.execute("""
    INSERT INTO iceberg.my_namespace.target_table
    SELECT * FROM iceberg.my_namespace.source_table
    WHERE amount > 50
""")
```

## Pandas 연동

### DataFrame에서 쿼리

```python
import pandas as pd

# Pandas DataFrame 생성
df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"]
})

# DataFrame을 DuckDB에서 직접 쿼리
result = conn.execute("SELECT * FROM df WHERE id > 1").df()
```

### 결과를 DataFrame으로

```python
# 쿼리 결과를 Pandas DataFrame으로 변환
df = conn.execute("""
    SELECT *
    FROM iceberg.my_namespace.my_table
    LIMIT 1000
""").df()
```

## 고급 기능

### 조인 쿼리

```python
result = conn.execute("""
    SELECT
        a.id,
        a.name,
        b.category
    FROM iceberg.my_namespace.users a
    JOIN iceberg.my_namespace.categories b
        ON a.category_id = b.id
""").df()
```

### 윈도우 함수

```python
result = conn.execute("""
    SELECT
        id,
        name,
        amount,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) as rank
    FROM iceberg.my_namespace.my_table
""").df()
```

### CTE (Common Table Expression)

```python
result = conn.execute("""
    WITH ranked AS (
        SELECT
            *,
            ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) as rn
        FROM iceberg.my_namespace.my_table
    )
    SELECT * FROM ranked WHERE rn = 1
""").df()
```

## 참고

- [DuckDB 공식 문서](https://duckdb.org/docs/)
- [DuckDB Iceberg 확장](https://duckdb.org/docs/extensions/iceberg.html)
