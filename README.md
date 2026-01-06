# simple-utils

일상적인 작업을 위한 간단한 파이썬 유틸리티 모음입니다.

## 설치 방법

```bash
pip install simple-utils
```

## 주요 기능

- **DateTime Utils**: 날짜 및 시간 처리 유틸리티
- **String Utils**: 문자열 처리 유틸리티
- **File Utils**: 파일 및 경로 처리 유틸리티
- **Decorators**: retry, timing 등 유용한 데코레이터
- **Object Storage**: 파일 기반 객체 저장소
- **Iceberg Client**: Trino를 통한 Iceberg 테이블 인터페이스

## 사용법

### DateTime Utils

```python
from simple_utils import datetime_utils

# 현재 타임스탬프 가져오기
ts = datetime_utils.now_timestamp()

# 날짜 문자열 파싱
dt = datetime_utils.parse_date("2024-01-15")

# datetime 포맷팅
formatted = datetime_utils.format_datetime(dt, "%Y/%m/%d")

# 날짜 범위 구하기
dates = datetime_utils.date_range("2024-01-01", "2024-01-07")
```

### String Utils

```python

from simple_utils import string_utils

# 케이스 변환
snake = string_utils.to_snake_case("HelloWorld")  # "hello_world"
camel = string_utils.to_camel_case("hello_world")  # "helloWorld"
pascal = string_utils.to_pascal_case("hello_world")  # "HelloWorld"

# 문자열 자르기
truncated = string_utils.truncate("Hello World", 8)  # "Hello..."

# 랜덤 문자열 생성
random_str = string_utils.random_string(10)
```

### File Utils

```python
from simple_utils import file_utils

# JSON 읽기/쓰기
data = file_utils.read_json("config.json")
file_utils.write_json("output.json", data)

# 디렉토리 생성 보장
file_utils.ensure_dir("/path/to/directory")

# 파일 확장자 얻기
ext = file_utils.get_extension("document.pdf")  # ".pdf"
```

### Decorators

```python
from simple_utils import decorators

# 재시도 데코레이터
@decorators.retry(max_attempts=3, delay=1.0)
def unstable_function():
    # 가끔 실패할 수 있음
    pass

# 실행 시간 측정 데코레이터
@decorators.timing
def slow_function():
    # 시간이 오래 걸리는 함수
    pass

# 결과 캐싱 데코레이터
@decorators.memoize
def expensive_calculation(x):
    return x ** 2
```

### Object Storage

파일 기반의 간단한 객체 저장소로, 텍스트, JSON, 바이너리 데이터를 키 기반으로 저장/조회/삭제할 수 있습니다.

```python
from simple_utils.storage import ObjectStorage

# 저장소 인스턴스 생성 (예: ./data 디렉토리)
storage = ObjectStorage("./data")

# 텍스트 저장 및 읽기
storage.write("hello.txt", "안녕하세요!")
print(storage.read_text("hello.txt"))  # '안녕하세요!'

# JSON 저장 및 읽기
storage.write("user.json", {"name": "홍길동", "age": 30})
user = storage.read("user.json")  # {'name': '홍길동', 'age': 30}

# 바이너리 데이터 저장 및 읽기
storage.write("image.bin", b"\x00\x01\x02")
data = storage.read_bytes("image.bin")

# 파일 존재 여부 확인
exists = storage.exists("user.json")

# 파일 삭제
storage.delete("hello.txt")

# 저장소 내 모든 파일(키) 목록 조회
all_keys = storage.list_keys()

# 특정 폴더 내 파일 목록 조회
sub_keys = storage.list_keys("images/")

# 하위 디렉토리 목록 조회
dirs = storage.list_dirs()
```

#### 주요 메서드

- `write(key, data)`: 텍스트, JSON(dict/list), 바이너리(bytes) 저장
- `read(key)`: 텍스트 또는 JSON 자동 판별하여 읽기
- `read_text(key)`: 텍스트로 읽기
- `read_bytes(key)`: 바이너리로 읽기
- `delete(key)`: 파일 삭제
- `exists(key)`: 파일 존재 여부 확인
- `list_keys(prefix)`: (옵션) prefix로 시작하는 모든 파일 목록
- `list_dirs()`: 하위 디렉토리 목록

### Iceberg Client

Trino를 통해 Iceberg 테이블과 상호작용하는 클라이언트입니다. 스키마 관리, 테이블 CRUD, 데이터 조회/삽입/수정/삭제를 지원합니다.

```bash
pip install simple-utils[iceberg]
```

```python
from simple_utils.storage import IcebergClient

# 클라이언트 생성
client = IcebergClient(
    host="localhost",
    port=7170,
    catalog="local",
    schema="data_product"
)

# 또는 context manager 사용
with IcebergClient(host="localhost", port=7170) as client:
    tables = client.list_tables()
```

#### 스키마 작업

```python
# 스키마 목록 조회
schemas = client.list_schemas()

# 스키마 생성
client.create_schema("my_schema")

# 스키마 삭제
client.drop_schema("my_schema")
```

#### 테이블 작업

```python
# 테이블 목록 조회
tables = client.list_tables()

# 테이블 존재 여부 확인
exists = client.table_exists("users")

# 테이블 생성
client.create_table("users", {
    "id": "VARCHAR",
    "name": "VARCHAR",
    "age": "INTEGER",
    "created_at": "TIMESTAMP"
})

# 파티션 테이블 생성
client.create_table("events", {
    "event_id": "VARCHAR",
    "event_date": "DATE",
    "data": "VARCHAR"
}, partitioned_by=["event_date"])

# 테이블 구조 조회
columns = client.describe_table("users")
# [{'name': 'id', 'type': 'varchar', 'nullable': True}, ...]

# 테이블 삭제
client.drop_table("users")
```

#### 데이터 조회

```python
# 전체 조회
rows = client.query("users")

# 특정 컬럼만 조회
rows = client.query("users", columns=["id", "name"])

# 조건부 조회
rows = client.query("users", where="age >= 20")

# 정렬 및 제한
rows = client.query("users", order_by="created_at DESC", limit=10)

# 복합 조회
rows = client.query(
    "users",
    columns=["id", "name"],
    where="age >= 20",
    order_by="name ASC",
    limit=100
)

# 행 수 조회
count = client.count("users")
count = client.count("users", where="age >= 20")

# 원시 SQL 실행
rows = client.query_sql("""
    SELECT u.name, COUNT(*) as order_count
    FROM users u
    JOIN orders o ON u.id = o.user_id
    GROUP BY u.name
""")
```

#### 데이터 삽입

```python
# 단일 행 삽입
client.insert("users", {"id": "1", "name": "홍길동", "age": 30})

# 다중 행 삽입
client.insert("users", [
    {"id": "2", "name": "김철수", "age": 25},
    {"id": "3", "name": "이영희", "age": 28}
])

# 대용량 배치 삽입 (100건씩 분할)
client.insert_batch("users", large_data_list, batch_size=100)
```

#### 데이터 수정/삭제

```python
# 행 업데이트
client.update("users", {"age": 31}, where="id = '1'")

# 조건부 삭제
client.delete("users", where="age < 18")

# 전체 삭제 (truncate)
client.truncate("users")
```

#### 주요 메서드

| 메서드 | 설명 |
|--------|------|
| `list_schemas()` | 카탈로그의 모든 스키마 조회 |
| `create_schema(name)` | 스키마 생성 |
| `drop_schema(name)` | 스키마 삭제 |
| `list_tables()` | 스키마의 모든 테이블 조회 |
| `table_exists(name)` | 테이블 존재 여부 확인 |
| `create_table(name, columns)` | 테이블 생성 |
| `drop_table(name)` | 테이블 삭제 |
| `describe_table(name)` | 테이블 컬럼 정보 조회 |
| `query(table, ...)` | 테이블 데이터 조회 |
| `query_sql(sql)` | 원시 SQL 실행 |
| `count(table)` | 행 수 조회 |
| `insert(table, data)` | 데이터 삽입 |
| `insert_batch(table, data)` | 배치 삽입 |
| `update(table, values, where)` | 데이터 수정 |
| `delete(table, where)` | 데이터 삭제 |
| `truncate(table)` | 테이블 전체 삭제 |
| `execute(sql)` | SQL 직접 실행 |
| `close()` | 연결 종료 |

## 라이선스

MIT License
