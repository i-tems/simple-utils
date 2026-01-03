"""
Useful decorators for common patterns.
"""

import functools
import logging
import time
from typing import Any, Callable, Optional, Type, Union, Tuple


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None,
) -> Callable:
    """
    Retry a function on failure with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Multiplier for delay after each retry (default: 2.0)
        exceptions: Tuple of exceptions to catch (default: (Exception,))
        on_retry: Optional callback called on each retry with (exception, attempt)

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        if on_retry:
                            on_retry(e, attempt)
                        time.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception  # type: ignore

        return wrapper

    return decorator


def timing(func: Optional[Callable] = None, *, logger: Optional[logging.Logger] = None) -> Callable:
    """
    Measure and log the execution time of a function.

    Can be used with or without parentheses:
        @timing
        def func(): ...

        @timing(logger=my_logger)
        def func(): ...

    Args:
        func: The function to wrap (when used without parentheses)
        logger: Optional logger to use (default: prints to stdout)

    Returns:
        Decorated function
    """

    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = f(*args, **kwargs)
            elapsed = time.perf_counter() - start

            message = f"{f.__name__} executed in {elapsed:.4f} seconds"
            if logger:
                logger.info(message)
            else:
                print(message)

            return result

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


def memoize(func: Callable) -> Callable:
    """
    Cache the results of a function based on its arguments.

    Note: Arguments must be hashable.

    Args:
        func: The function to memoize

    Returns:
        Decorated function with caching
    """
    cache: dict = {}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    wrapper.cache = cache  # type: ignore
    wrapper.clear_cache = cache.clear  # type: ignore

    return wrapper


def deprecated(
    message: str = "",
    version: Optional[str] = None,
) -> Callable:
    """
    Mark a function as deprecated and emit a warning when called.

    Args:
        message: Optional deprecation message
        version: Optional version when the function will be removed

    Returns:
        Decorated function
    """
    import warnings

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warning_msg = f"{func.__name__} is deprecated"
            if version:
                warning_msg += f" and will be removed in version {version}"
            if message:
                warning_msg += f". {message}"
            warnings.warn(warning_msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def singleton(cls: Type) -> Type:
    """
    Make a class a singleton (only one instance can exist).

    Args:
        cls: The class to make a singleton

    Returns:
        Singleton class
    """
    instances: dict = {}

    @functools.wraps(cls)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper  # type: ignore


def throttle(interval: float) -> Callable:
    """
    Limit how often a function can be called.

    Args:
        interval: Minimum time between calls in seconds

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        last_called = [0.0]

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            elapsed = time.time() - last_called[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def debounce(wait: float) -> Callable:
    """
    Delay function execution until wait time has passed without new calls.

    Note: This is a simple synchronous implementation. For async use cases,
    consider using asyncio-based solutions.

    Args:
        wait: Time to wait in seconds before executing

    Returns:
        Decorated function
    """
    import threading

    def decorator(func: Callable) -> Callable:
        timer: Optional[threading.Timer] = None
        result: list = [None]
        lock = threading.Lock()

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal timer

            def execute():
                with lock:
                    result[0] = func(*args, **kwargs)

            with lock:
                if timer is not None:
                    timer.cancel()
                timer = threading.Timer(wait, execute)
                timer.start()

            return result[0]

        return wrapper

    return decorator


def log_calls(
    logger: Optional[logging.Logger] = None,
    level: int = logging.DEBUG,
    log_args: bool = True,
    log_result: bool = True,
) -> Callable:
    """
    Log function calls, arguments, and results.

    Args:
        logger: Logger to use (default: creates one from function name)
        level: Log level (default: DEBUG)
        log_args: Whether to log arguments (default: True)
        log_result: Whether to log the result (default: True)

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        nonlocal logger
        if logger is None:
            logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if log_args:
                args_repr = [repr(a) for a in args]
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                logger.log(level, f"Calling {func.__name__}({signature})")  # type: ignore
            else:
                logger.log(level, f"Calling {func.__name__}")  # type: ignore

            result = func(*args, **kwargs)

            if log_result:
                logger.log(level, f"{func.__name__} returned {result!r}")  # type: ignore

            return result

        return wrapper

    return decorator


def catch_exceptions(
    default: Any = None,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_error: Optional[Callable[[Exception], Any]] = None,
) -> Callable:
    """
    Catch exceptions and return a default value instead of raising.

    Args:
        default: Value to return on exception (default: None)
        exceptions: Tuple of exceptions to catch (default: (Exception,))
        on_error: Optional callback called with the exception

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                if on_error:
                    return on_error(e)
                return default

        return wrapper

    return decorator


def run_once(func: Callable) -> Callable:
    """
    Ensure a function is only executed once. Subsequent calls return the first result.

    Args:
        func: The function to wrap

    Returns:
        Decorated function
    """
    result: list = []
    called = [False]

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if not called[0]:
            result.append(func(*args, **kwargs))
            called[0] = True
        return result[0]

    return wrapper


def validate_args(**validators: Callable[[Any], bool]) -> Callable:
    """
    Validate function arguments using validator functions.

    Args:
        **validators: Keyword arguments mapping parameter names to validator functions

    Returns:
        Decorated function

    Example:
        @validate_args(x=lambda x: x > 0, name=lambda s: len(s) > 0)
        def func(x, name): ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            import inspect

            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for param_name, validator in validators.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not validator(value):
                        raise ValueError(
                            f"Invalid value for parameter '{param_name}': {value!r}"
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator
