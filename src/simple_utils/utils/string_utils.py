"""
String utilities for common string operations.
"""

import re
import random
import string
from typing import List, Optional


def to_snake_case(s: str) -> str:
    """
    Convert a string to snake_case.

    Args:
        s: Input string (CamelCase, PascalCase, kebab-case, etc.)

    Returns:
        A snake_case string
    """
    s = re.sub(r"[-\s]+", "_", s)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    return s.lower()


def to_camel_case(s: str) -> str:
    """
    Convert a string to camelCase.

    Args:
        s: Input string (snake_case, kebab-case, etc.)

    Returns:
        A camelCase string
    """
    s = re.sub(r"[-_\s]+", " ", s)
    words = s.split()
    if not words:
        return ""
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


def to_pascal_case(s: str) -> str:
    """
    Convert a string to PascalCase.

    Args:
        s: Input string (snake_case, kebab-case, etc.)

    Returns:
        A PascalCase string
    """
    s = re.sub(r"[-_\s]+", " ", s)
    words = s.split()
    return "".join(word.capitalize() for word in words)


def to_kebab_case(s: str) -> str:
    """
    Convert a string to kebab-case.

    Args:
        s: Input string (CamelCase, snake_case, etc.)

    Returns:
        A kebab-case string
    """
    return to_snake_case(s).replace("_", "-")


def truncate(s: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length.

    Args:
        s: Input string
        max_length: Maximum length (including suffix)
        suffix: Suffix to add when truncated (default: "...")

    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s
    return s[: max_length - len(suffix)] + suffix


def random_string(
    length: int = 8,
    chars: str = string.ascii_letters + string.digits,
) -> str:
    """
    Generate a random string.

    Args:
        length: Length of the string (default: 8)
        chars: Characters to use (default: letters and digits)

    Returns:
        A random string
    """
    return "".join(random.choice(chars) for _ in range(length))


def random_hex(length: int = 8) -> str:
    """
    Generate a random hexadecimal string.

    Args:
        length: Length of the string (default: 8)

    Returns:
        A random hex string
    """
    return "".join(random.choice("0123456789abcdef") for _ in range(length))


def slugify(s: str, separator: str = "-") -> str:
    """
    Convert a string to a URL-friendly slug.

    Args:
        s: Input string
        separator: Word separator (default: "-")

    Returns:
        A slugified string
    """
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", separator, s)
    return s.strip(separator)


def is_empty(s: Optional[str]) -> bool:
    """
    Check if a string is None or empty (after stripping whitespace).

    Args:
        s: Input string

    Returns:
        True if None or empty, False otherwise
    """
    return s is None or s.strip() == ""


def is_not_empty(s: Optional[str]) -> bool:
    """
    Check if a string is not None and not empty.

    Args:
        s: Input string

    Returns:
        True if not None and not empty, False otherwise
    """
    return not is_empty(s)


def split_words(s: str) -> List[str]:
    """
    Split a string into words, handling various case styles.

    Args:
        s: Input string (CamelCase, snake_case, kebab-case, etc.)

    Returns:
        A list of words
    """
    s = re.sub(r"[-_\s]+", " ", s)
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s)
    return s.lower().split()


def reverse(s: str) -> str:
    """
    Reverse a string.

    Args:
        s: Input string

    Returns:
        Reversed string
    """
    return s[::-1]


def remove_prefix(s: str, prefix: str) -> str:
    """
    Remove a prefix from a string if present.

    Args:
        s: Input string
        prefix: Prefix to remove

    Returns:
        String without the prefix
    """
    if s.startswith(prefix):
        return s[len(prefix) :]
    return s


def remove_suffix(s: str, suffix: str) -> str:
    """
    Remove a suffix from a string if present.

    Args:
        s: Input string
        suffix: Suffix to remove

    Returns:
        String without the suffix
    """
    if s.endswith(suffix):
        return s[: -len(suffix)]
    return s


def mask(
    s: str,
    visible_start: int = 0,
    visible_end: int = 0,
    mask_char: str = "*",
) -> str:
    """
    Mask a string, showing only specified number of characters at start/end.

    Args:
        s: Input string
        visible_start: Number of characters to show at start
        visible_end: Number of characters to show at end
        mask_char: Character to use for masking (default: "*")

    Returns:
        Masked string
    """
    if len(s) <= visible_start + visible_end:
        return s

    start = s[:visible_start] if visible_start > 0 else ""
    end = s[-visible_end:] if visible_end > 0 else ""
    masked_length = len(s) - visible_start - visible_end

    return start + (mask_char * masked_length) + end


def extract_numbers(s: str) -> List[str]:
    """
    Extract all numbers from a string.

    Args:
        s: Input string

    Returns:
        A list of number strings
    """
    return re.findall(r"-?\d+\.?\d*", s)


def contains_any(s: str, substrings: List[str]) -> bool:
    """
    Check if a string contains any of the given substrings.

    Args:
        s: Input string
        substrings: List of substrings to check

    Returns:
        True if any substring is found, False otherwise
    """
    return any(sub in s for sub in substrings)


def contains_all(s: str, substrings: List[str]) -> bool:
    """
    Check if a string contains all of the given substrings.

    Args:
        s: Input string
        substrings: List of substrings to check

    Returns:
        True if all substrings are found, False otherwise
    """
    return all(sub in s for sub in substrings)