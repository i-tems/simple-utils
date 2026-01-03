"""Tests for decorators module."""

import logging
import time
import warnings

import pytest

from simple_utils import decorators


class TestRetry:
    def test_retry_success_first_attempt(self):
        call_count = 0

        @decorators.retry(max_attempts=3)
        def succeed():
            nonlocal call_count
            call_count += 1
            return "success"

        result = succeed()
        assert result == "success"
        assert call_count == 1

    def test_retry_success_after_failure(self):
        call_count = 0

        @decorators.retry(max_attempts=3, delay=0.01)
        def fail_then_succeed():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("fail")
            return "success"

        result = fail_then_succeed()
        assert result == "success"
        assert call_count == 3

    def test_retry_max_attempts_exceeded(self):
        @decorators.retry(max_attempts=2, delay=0.01)
        def always_fail():
            raise ValueError("always fails")

        with pytest.raises(ValueError, match="always fails"):
            always_fail()

    def test_retry_specific_exception(self):
        @decorators.retry(max_attempts=3, delay=0.01, exceptions=(ValueError,))
        def raise_type_error():
            raise TypeError("wrong type")

        with pytest.raises(TypeError):
            raise_type_error()

    def test_retry_on_retry_callback(self):
        retries = []

        def on_retry(exc, attempt):
            retries.append((str(exc), attempt))

        call_count = 0

        @decorators.retry(max_attempts=3, delay=0.01, on_retry=on_retry)
        def fail_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError(f"fail {call_count}")
            return "success"

        fail_twice()
        assert len(retries) == 2


class TestTiming:
    def test_timing_without_args(self, capsys):
        @decorators.timing
        def slow_func():
            time.sleep(0.01)
            return "done"

        result = slow_func()
        assert result == "done"
        captured = capsys.readouterr()
        assert "slow_func executed in" in captured.out

    def test_timing_with_logger(self, caplog):
        logger = logging.getLogger("test")

        @decorators.timing(logger=logger)
        def slow_func():
            time.sleep(0.01)
            return "done"

        with caplog.at_level(logging.INFO):
            result = slow_func()

        assert result == "done"
        assert "slow_func executed in" in caplog.text


class TestMemoize:
    def test_memoize_caches_result(self):
        call_count = 0

        @decorators.memoize
        def expensive(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        assert expensive(5) == 10
        assert expensive(5) == 10
        assert call_count == 1

    def test_memoize_different_args(self):
        call_count = 0

        @decorators.memoize
        def add(a, b):
            nonlocal call_count
            call_count += 1
            return a + b

        assert add(1, 2) == 3
        assert add(3, 4) == 7
        assert add(1, 2) == 3
        assert call_count == 2

    def test_memoize_clear_cache(self):
        call_count = 0

        @decorators.memoize
        def func(x):
            nonlocal call_count
            call_count += 1
            return x

        func(1)
        func(1)
        assert call_count == 1

        func.clear_cache()
        func(1)
        assert call_count == 2


class TestDeprecated:
    def test_deprecated_warning(self):
        @decorators.deprecated()
        def old_func():
            return "old"

        with pytest.warns(DeprecationWarning, match="old_func is deprecated"):
            result = old_func()

        assert result == "old"

    def test_deprecated_with_version(self):
        @decorators.deprecated(version="2.0")
        def old_func():
            return "old"

        with pytest.warns(DeprecationWarning, match="will be removed in version 2.0"):
            old_func()

    def test_deprecated_with_message(self):
        @decorators.deprecated(message="Use new_func instead")
        def old_func():
            return "old"

        with pytest.warns(DeprecationWarning, match="Use new_func instead"):
            old_func()


class TestSingleton:
    def test_singleton_same_instance(self):
        @decorators.singleton
        class MySingleton:
            def __init__(self, value):
                self.value = value

        a = MySingleton(1)
        b = MySingleton(2)
        assert a is b
        assert a.value == 1  # first value is preserved


class TestThrottle:
    def test_throttle(self):
        call_times = []

        @decorators.throttle(0.05)
        def throttled():
            call_times.append(time.time())

        throttled()
        throttled()
        throttled()

        # Should have delays between calls
        assert len(call_times) == 3
        assert call_times[1] - call_times[0] >= 0.04
        assert call_times[2] - call_times[1] >= 0.04


class TestLogCalls:
    def test_log_calls(self, caplog):
        logger = logging.getLogger("test")

        @decorators.log_calls(logger=logger, level=logging.INFO)
        def add(a, b):
            return a + b

        with caplog.at_level(logging.INFO):
            result = add(1, 2)

        assert result == 3
        assert "Calling add" in caplog.text
        assert "add returned 3" in caplog.text


class TestCatchExceptions:
    def test_catch_returns_default(self):
        @decorators.catch_exceptions(default="default")
        def raise_error():
            raise ValueError("error")

        result = raise_error()
        assert result == "default"

    def test_catch_specific_exception(self):
        @decorators.catch_exceptions(default="default", exceptions=(ValueError,))
        def raise_type_error():
            raise TypeError("wrong type")

        with pytest.raises(TypeError):
            raise_type_error()

    def test_catch_on_error_callback(self):
        errors = []

        @decorators.catch_exceptions(on_error=lambda e: errors.append(str(e)))
        def raise_error():
            raise ValueError("test error")

        raise_error()
        assert errors == ["test error"]


class TestRunOnce:
    def test_run_once(self):
        call_count = 0

        @decorators.run_once
        def init():
            nonlocal call_count
            call_count += 1
            return call_count

        assert init() == 1
        assert init() == 1
        assert init() == 1
        assert call_count == 1


class TestValidateArgs:
    def test_validate_args_valid(self):
        @decorators.validate_args(x=lambda x: x > 0)
        def process(x):
            return x * 2

        assert process(5) == 10

    def test_validate_args_invalid(self):
        @decorators.validate_args(x=lambda x: x > 0)
        def process(x):
            return x * 2

        with pytest.raises(ValueError, match="Invalid value for parameter 'x'"):
            process(-5)

    def test_validate_args_multiple(self):
        @decorators.validate_args(
            x=lambda x: x > 0,
            name=lambda s: len(s) > 0,
        )
        def greet(x, name):
            return f"Hello {name}, x={x}"

        assert greet(5, "World") == "Hello World, x=5"

        with pytest.raises(ValueError):
            greet(-1, "World")

        with pytest.raises(ValueError):
            greet(5, "")
