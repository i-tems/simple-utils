"""Tests for string_utils module."""

import pytest

from simple_utils import string_utils


class TestCaseConversion:
    def test_to_snake_case_from_camel(self):
        assert string_utils.to_snake_case("camelCase") == "camel_case"

    def test_to_snake_case_from_pascal(self):
        assert string_utils.to_snake_case("PascalCase") == "pascal_case"

    def test_to_snake_case_from_kebab(self):
        assert string_utils.to_snake_case("kebab-case") == "kebab_case"

    def test_to_snake_case_with_spaces(self):
        assert string_utils.to_snake_case("hello world") == "hello_world"

    def test_to_camel_case_from_snake(self):
        assert string_utils.to_camel_case("snake_case") == "snakeCase"

    def test_to_camel_case_from_kebab(self):
        assert string_utils.to_camel_case("kebab-case") == "kebabCase"

    def test_to_camel_case_empty(self):
        assert string_utils.to_camel_case("") == ""

    def test_to_pascal_case_from_snake(self):
        assert string_utils.to_pascal_case("snake_case") == "SnakeCase"

    def test_to_pascal_case_from_camel(self):
        assert string_utils.to_pascal_case("camelCase") == "Camelcase"

    def test_to_kebab_case_from_snake(self):
        assert string_utils.to_kebab_case("snake_case") == "snake-case"

    def test_to_kebab_case_from_camel(self):
        assert string_utils.to_kebab_case("camelCase") == "camel-case"


class TestTruncate:
    def test_truncate_short_string(self):
        assert string_utils.truncate("hello", 10) == "hello"

    def test_truncate_long_string(self):
        assert string_utils.truncate("hello world", 8) == "hello..."

    def test_truncate_custom_suffix(self):
        assert string_utils.truncate("hello world", 8, suffix="..") == "hello .."

    def test_truncate_exact_length(self):
        assert string_utils.truncate("hello", 5) == "hello"


class TestRandomString:
    def test_random_string_default_length(self):
        result = string_utils.random_string()
        assert len(result) == 8

    def test_random_string_custom_length(self):
        result = string_utils.random_string(16)
        assert len(result) == 16

    def test_random_string_custom_chars(self):
        result = string_utils.random_string(10, chars="abc")
        assert all(c in "abc" for c in result)


class TestRandomHex:
    def test_random_hex_default_length(self):
        result = string_utils.random_hex()
        assert len(result) == 8

    def test_random_hex_valid_chars(self):
        result = string_utils.random_hex(100)
        assert all(c in "0123456789abcdef" for c in result)


class TestSlugify:
    def test_slugify_basic(self):
        assert string_utils.slugify("Hello World") == "hello-world"

    def test_slugify_special_chars(self):
        assert string_utils.slugify("Hello, World!") == "hello-world"

    def test_slugify_custom_separator(self):
        assert string_utils.slugify("Hello World", "_") == "hello_world"


class TestEmpty:
    def test_is_empty_none(self):
        assert string_utils.is_empty(None) is True

    def test_is_empty_empty_string(self):
        assert string_utils.is_empty("") is True

    def test_is_empty_whitespace(self):
        assert string_utils.is_empty("   ") is True

    def test_is_empty_non_empty(self):
        assert string_utils.is_empty("hello") is False

    def test_is_not_empty(self):
        assert string_utils.is_not_empty("hello") is True
        assert string_utils.is_not_empty("") is False


class TestSplitWords:
    def test_split_words_camel_case(self):
        assert string_utils.split_words("camelCase") == ["camel", "case"]

    def test_split_words_snake_case(self):
        assert string_utils.split_words("snake_case") == ["snake", "case"]

    def test_split_words_kebab_case(self):
        assert string_utils.split_words("kebab-case") == ["kebab", "case"]


class TestReverse:
    def test_reverse_string(self):
        assert string_utils.reverse("hello") == "olleh"

    def test_reverse_empty(self):
        assert string_utils.reverse("") == ""


class TestRemovePrefixSuffix:
    def test_remove_prefix_present(self):
        assert string_utils.remove_prefix("hello_world", "hello_") == "world"

    def test_remove_prefix_absent(self):
        assert string_utils.remove_prefix("hello_world", "foo_") == "hello_world"

    def test_remove_suffix_present(self):
        assert string_utils.remove_suffix("hello_world", "_world") == "hello"

    def test_remove_suffix_absent(self):
        assert string_utils.remove_suffix("hello_world", "_foo") == "hello_world"


class TestMask:
    def test_mask_default(self):
        assert string_utils.mask("1234567890") == "**********"

    def test_mask_visible_start(self):
        assert string_utils.mask("1234567890", visible_start=2) == "12********"

    def test_mask_visible_end(self):
        assert string_utils.mask("1234567890", visible_end=2) == "********90"

    def test_mask_both(self):
        assert string_utils.mask("1234567890", visible_start=2, visible_end=2) == "12******90"

    def test_mask_short_string(self):
        assert string_utils.mask("123", visible_start=2, visible_end=2) == "123"


class TestExtractNumbers:
    def test_extract_integers(self):
        assert string_utils.extract_numbers("abc123def456") == ["123", "456"]

    def test_extract_floats(self):
        assert string_utils.extract_numbers("price: 12.50") == ["12.50"]

    def test_extract_negative(self):
        assert string_utils.extract_numbers("temp: -5 degrees") == ["-5"]


class TestContains:
    def test_contains_any_found(self):
        assert string_utils.contains_any("hello world", ["hello", "foo"]) is True

    def test_contains_any_not_found(self):
        assert string_utils.contains_any("hello world", ["foo", "bar"]) is False

    def test_contains_all_found(self):
        assert string_utils.contains_all("hello world", ["hello", "world"]) is True

    def test_contains_all_not_found(self):
        assert string_utils.contains_all("hello world", ["hello", "foo"]) is False
