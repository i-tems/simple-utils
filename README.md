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

## 라이선스

MIT License
