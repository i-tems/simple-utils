# Iceberg 사용 가이드

Apache Iceberg 카탈로그와 연동하기 위한 클라이언트입니다.

## 설치

Iceberg 기능을 사용하려면 선택적 의존성을 설치해야 합니다:

```bash
pip install simple-utils[iceberg]
```

## 기본 사용법

```python
from simple_utils.platform.iceberg import Iceberg

# Iceberg 카탈로그 연결 (기본: localhost:8181)
iceberg = Iceberg()

# 또는 커스텀 URI 지정
iceberg = Iceberg(iceberg_catalog_uri="http://your-catalog-server:8181")

# 카탈로그 접근
catalog = iceberg.catalog
```

## 카탈로그 작업

### 네임스페이스 목록 조회

```python
namespaces = catalog.list_namespaces()
print(namespaces)  # [('default',), ('my_namespace',)]
```

### 네임스페이스 생성

```python
catalog.create_namespace("my_namespace")
```

### 테이블 목록 조회

```python
tables = catalog.list_tables("my_namespace")
print(tables)  # [('my_namespace', 'table1'), ('my_namespace', 'table2')]
```

### 테이블 로드

```python
table = catalog.load_table("my_namespace.my_table")

# 테이블 스키마 확인
print(table.schema())

# 테이블 메타데이터 확인
print(table.metadata)
```

## 데이터 읽기

### Arrow Table로 읽기

```python
table = catalog.load_table("my_namespace.my_table")

# 전체 데이터 읽기
arrow_table = table.scan().to_arrow()

# 특정 컬럼만 읽기
arrow_table = table.scan(selected=["col1", "col2"]).to_arrow()

# 필터 적용
from pyiceberg.expressions import GreaterThan

arrow_table = table.scan(
    row_filter=GreaterThan("amount", 100)
).to_arrow()
```

### Pandas DataFrame으로 읽기

```python
table = catalog.load_table("my_namespace.my_table")

# Pandas DataFrame으로 변환
df = table.scan().to_pandas()
```

## 데이터 쓰기

### DataFrame 추가

```python
import pyarrow as pa

table = catalog.load_table("my_namespace.my_table")

# PyArrow Table 생성
data = pa.table({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "amount": [100, 200, 300]
})

# 데이터 추가
table.append(data)
```

### 데이터 덮어쓰기

```python
table.overwrite(data)
```

## 테이블 생성

```python
from pyiceberg.schema import Schema
from pyiceberg.types import NestedField, LongType, StringType

# 스키마 정의
schema = Schema(
    NestedField(1, "id", LongType(), required=True),
    NestedField(2, "name", StringType(), required=True),
    NestedField(3, "amount", LongType(), required=False),
)

# 테이블 생성
catalog.create_table(
    identifier="my_namespace.new_table",
    schema=schema
)
```

## 참고

- [PyIceberg 공식 문서](https://py.iceberg.apache.org/)
- [Apache Iceberg 공식 사이트](https://iceberg.apache.org/)
