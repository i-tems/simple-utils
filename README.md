# simple-utils

A collection of simple Python utilities for everyday tasks.

## Installation

```bash
pip install simple-utils
```

## Features

- **DateTime Utils**: Date and time manipulation utilities
- **String Utils**: String processing utilities
- **File Utils**: File and path handling utilities
- **Decorators**: Useful decorators like retry, timing, etc.

## Usage

### DateTime Utils

```python
from simple_utils import datetime_utils

# Get current timestamp
ts = datetime_utils.now_timestamp()

# Parse date string
dt = datetime_utils.parse_date("2024-01-15")

# Format datetime
formatted = datetime_utils.format_datetime(dt, "%Y/%m/%d")

# Get date range
dates = datetime_utils.date_range("2024-01-01", "2024-01-07")
```

### String Utils

```python
from simple_utils import string_utils

# Convert case
snake = string_utils.to_snake_case("HelloWorld")  # "hello_world"
camel = string_utils.to_camel_case("hello_world")  # "helloWorld"
pascal = string_utils.to_pascal_case("hello_world")  # "HelloWorld"

# Truncate string
truncated = string_utils.truncate("Hello World", 8)  # "Hello..."

# Generate random string
random_str = string_utils.random_string(10)
```

### File Utils

```python
from simple_utils import file_utils

# Read/Write JSON
data = file_utils.read_json("config.json")
file_utils.write_json("output.json", data)

# Ensure directory exists
file_utils.ensure_dir("/path/to/directory")

# Get file extension
ext = file_utils.get_extension("document.pdf")  # ".pdf"
```

### Decorators

```python
from simple_utils import decorators

# Retry decorator
@decorators.retry(max_attempts=3, delay=1.0)
def unstable_function():
    # May fail sometimes
    pass

# Timing decorator
@decorators.timing
def slow_function():
    # Takes some time
    pass

# Cache decorator
@decorators.memoize
def expensive_calculation(x):
    return x ** 2
```

## License

MIT License
