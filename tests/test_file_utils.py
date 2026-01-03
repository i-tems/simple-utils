"""Tests for file_utils module."""

import json
import tempfile
from pathlib import Path

import pytest

from simple_utils import file_utils


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


class TestReadWriteText:
    def test_write_and_read_text(self, temp_dir):
        filepath = temp_dir / "test.txt"
        content = "Hello, World!"
        file_utils.write_text(filepath, content)
        assert file_utils.read_text(filepath) == content

    def test_read_text_encoding(self, temp_dir):
        filepath = temp_dir / "test.txt"
        content = "한글 테스트"
        file_utils.write_text(filepath, content)
        assert file_utils.read_text(filepath) == content


class TestReadWriteLines:
    def test_write_and_read_lines(self, temp_dir):
        filepath = temp_dir / "test.txt"
        lines = ["line1", "line2", "line3"]
        file_utils.write_lines(filepath, lines)
        assert file_utils.read_lines(filepath) == lines


class TestReadWriteJson:
    def test_write_and_read_json_dict(self, temp_dir):
        filepath = temp_dir / "test.json"
        data = {"key": "value", "number": 42}
        file_utils.write_json(filepath, data)
        assert file_utils.read_json(filepath) == data

    def test_write_and_read_json_list(self, temp_dir):
        filepath = temp_dir / "test.json"
        data = [1, 2, 3, "four"]
        file_utils.write_json(filepath, data)
        assert file_utils.read_json(filepath) == data


class TestReadWriteBytes:
    def test_write_and_read_bytes(self, temp_dir):
        filepath = temp_dir / "test.bin"
        data = b"\x00\x01\x02\x03"
        file_utils.write_bytes(filepath, data)
        assert file_utils.read_bytes(filepath) == data


class TestDirectoryOps:
    def test_ensure_dir(self, temp_dir):
        new_dir = temp_dir / "new" / "nested" / "dir"
        result = file_utils.ensure_dir(new_dir)
        assert result.exists()
        assert result.is_dir()

    def test_ensure_parent_dir(self, temp_dir):
        filepath = temp_dir / "parent" / "child" / "file.txt"
        parent = file_utils.ensure_parent_dir(filepath)
        assert parent.exists()
        assert parent == filepath.parent


class TestPathChecks:
    def test_exists(self, temp_dir):
        filepath = temp_dir / "test.txt"
        assert file_utils.exists(filepath) is False
        filepath.touch()
        assert file_utils.exists(filepath) is True

    def test_is_file(self, temp_dir):
        filepath = temp_dir / "test.txt"
        filepath.touch()
        assert file_utils.is_file(filepath) is True
        assert file_utils.is_file(temp_dir) is False

    def test_is_dir(self, temp_dir):
        assert file_utils.is_dir(temp_dir) is True
        filepath = temp_dir / "test.txt"
        filepath.touch()
        assert file_utils.is_dir(filepath) is False


class TestPathOperations:
    def test_get_extension(self):
        assert file_utils.get_extension("/path/to/file.txt") == ".txt"
        assert file_utils.get_extension("/path/to/file.tar.gz") == ".gz"

    def test_get_stem(self):
        assert file_utils.get_stem("/path/to/file.txt") == "file"

    def test_get_name(self):
        assert file_utils.get_name("/path/to/file.txt") == "file.txt"

    def test_get_parent(self):
        assert file_utils.get_parent("/path/to/file.txt") == Path("/path/to")


class TestListFiles:
    def test_list_files(self, temp_dir):
        (temp_dir / "file1.txt").touch()
        (temp_dir / "file2.txt").touch()
        (temp_dir / "file3.py").touch()

        all_files = file_utils.list_files(temp_dir)
        assert len(all_files) == 3

        txt_files = file_utils.list_files(temp_dir, "*.txt")
        assert len(txt_files) == 2

    def test_list_files_recursive(self, temp_dir):
        (temp_dir / "subdir").mkdir()
        (temp_dir / "file1.txt").touch()
        (temp_dir / "subdir" / "file2.txt").touch()

        files = file_utils.list_files(temp_dir, "*.txt", recursive=True)
        assert len(files) == 2


class TestCopyMoveDelete:
    def test_copy_file(self, temp_dir):
        src = temp_dir / "src.txt"
        dst = temp_dir / "dst.txt"
        src.write_text("content")

        result = file_utils.copy_file(src, dst)
        assert result.exists()
        assert dst.read_text() == "content"
        assert src.exists()  # original still exists

    def test_move_file(self, temp_dir):
        src = temp_dir / "src.txt"
        dst = temp_dir / "dst.txt"
        src.write_text("content")

        result = file_utils.move_file(src, dst)
        assert result.exists()
        assert dst.read_text() == "content"
        assert not src.exists()  # original moved

    def test_delete_file(self, temp_dir):
        filepath = temp_dir / "test.txt"
        filepath.touch()
        assert filepath.exists()

        file_utils.delete_file(filepath)
        assert not filepath.exists()

    def test_delete_file_missing_ok(self, temp_dir):
        filepath = temp_dir / "nonexistent.txt"
        file_utils.delete_file(filepath, missing_ok=True)  # should not raise

    def test_delete_dir(self, temp_dir):
        subdir = temp_dir / "subdir"
        subdir.mkdir()
        (subdir / "file.txt").touch()

        file_utils.delete_dir(subdir)
        assert not subdir.exists()


class TestFileSize:
    def test_get_size(self, temp_dir):
        filepath = temp_dir / "test.txt"
        filepath.write_text("12345")
        assert file_utils.get_size(filepath) == 5

    def test_get_size_human(self, temp_dir):
        filepath = temp_dir / "test.txt"
        filepath.write_bytes(b"x" * 1024)
        result = file_utils.get_size_human(filepath)
        assert "KB" in result


class TestJoinResolvePath:
    def test_join_path(self):
        result = file_utils.join_path("path", "to", "file.txt")
        assert result == Path("path/to/file.txt")

    def test_resolve_path(self, temp_dir):
        result = file_utils.resolve_path(temp_dir / "subdir" / ".." / "file.txt")
        expected = temp_dir / "file.txt"
        assert result == expected.resolve()


class TestObjectStorage:
    def test_init_creates_directory(self, temp_dir):
        storage_path = temp_dir / "storage"
        storage = file_utils.ObjectStorage(storage_path)
        assert storage_path.exists()
        assert storage.base_path == storage_path

    def test_write_and_read_string(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        storage.write("test.txt", "hello world")
        assert storage.read("test.txt") == "hello world"

    def test_write_and_read_dict(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        data = {"name": "John", "age": 30}
        storage.write("data.json", data)
        assert storage.read("data.json") == data

    def test_write_and_read_list(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        data = [1, 2, 3, "four"]
        storage.write("list.json", data)
        assert storage.read("list.json") == data

    def test_write_and_read_bytes(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        data = b"\x00\x01\x02\x03"
        storage.write("binary.bin", data)
        assert storage.read_bytes("binary.bin") == data

    def test_read_text(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        storage.write("test.txt", "hello")
        assert storage.read_text("test.txt") == "hello"

    def test_write_nested_key(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        storage.write("dir1/dir2/file.txt", "nested content")
        assert storage.exists("dir1/dir2/file.txt")
        assert storage.read("dir1/dir2/file.txt") == "nested content"

    def test_write_unsupported_type(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        with pytest.raises(TypeError):
            storage.write("test.txt", object())

    def test_delete(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        storage.write("test.txt", "content")
        assert storage.exists("test.txt")
        storage.delete("test.txt")
        assert not storage.exists("test.txt")

    def test_delete_missing_ok(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        storage.delete("nonexistent.txt", missing_ok=True)  # should not raise

    def test_exists(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        assert storage.exists("test.txt") is False
        storage.write("test.txt", "content")
        assert storage.exists("test.txt") is True

    def test_list_dirs(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        storage.write("dir1/file1.txt", "a")
        storage.write("dir2/file2.txt", "b")
        storage.write("root.txt", "c")

        dirs = storage.list_dirs()
        assert set(dirs) == {"dir1", "dir2"}

    def test_list_keys(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        storage.write("file1.txt", "a")
        storage.write("dir/file2.txt", "b")
        storage.write("dir/subdir/file3.txt", "c")

        keys = storage.list_keys()
        assert len(keys) == 3
        assert "file1.txt" in keys
        assert "dir/file2.txt" in keys

    def test_list_keys_with_prefix(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        storage.write("data/file1.txt", "a")
        storage.write("data/file2.txt", "b")
        storage.write("other/file3.txt", "c")

        keys = storage.list_keys("data")
        assert len(keys) == 2
        assert all(k.startswith("data/") for k in keys)

    def test_list_keys_nonexistent_prefix(self, temp_dir):
        storage = file_utils.ObjectStorage(temp_dir)
        keys = storage.list_keys("nonexistent")
        assert keys == []
