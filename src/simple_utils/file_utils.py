"""
File and path utilities for common file operations.
"""

import json
import os
import shutil
from pathlib import Path
from typing import Any, List, Optional, Union


def read_text(filepath: Union[str, Path], encoding: str = "utf-8") -> str:
    """
    Read a text file and return its contents.

    Args:
        filepath: Path to the file
        encoding: File encoding (default: "utf-8")

    Returns:
        File contents as a string
    """
    return Path(filepath).read_text(encoding=encoding)


def write_text(
    filepath: Union[str, Path],
    content: str,
    encoding: str = "utf-8",
) -> None:
    """
    Write text content to a file.

    Args:
        filepath: Path to the file
        content: Content to write
        encoding: File encoding (default: "utf-8")
    """
    Path(filepath).write_text(content, encoding=encoding)


def read_lines(
    filepath: Union[str, Path],
    encoding: str = "utf-8",
    strip: bool = True,
) -> List[str]:
    """
    Read a text file and return lines as a list.

    Args:
        filepath: Path to the file
        encoding: File encoding (default: "utf-8")
        strip: Whether to strip whitespace from lines (default: True)

    Returns:
        List of lines
    """
    content = read_text(filepath, encoding)
    lines = content.splitlines()
    if strip:
        lines = [line.strip() for line in lines]
    return lines


def write_lines(
    filepath: Union[str, Path],
    lines: List[str],
    encoding: str = "utf-8",
) -> None:
    """
    Write lines to a text file.

    Args:
        filepath: Path to the file
        lines: List of lines to write
        encoding: File encoding (default: "utf-8")
    """
    content = "\n".join(lines)
    write_text(filepath, content, encoding)


def read_json(filepath: Union[str, Path], encoding: str = "utf-8") -> Any:
    """
    Read a JSON file and return its contents.

    Args:
        filepath: Path to the JSON file
        encoding: File encoding (default: "utf-8")

    Returns:
        Parsed JSON data
    """
    content = read_text(filepath, encoding)
    return json.loads(content)


def write_json(
    filepath: Union[str, Path],
    data: Any,
    encoding: str = "utf-8",
    indent: int = 2,
    ensure_ascii: bool = False,
) -> None:
    """
    Write data to a JSON file.

    Args:
        filepath: Path to the JSON file
        data: Data to write
        encoding: File encoding (default: "utf-8")
        indent: JSON indentation (default: 2)
        ensure_ascii: Whether to escape non-ASCII characters (default: False)
    """
    content = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
    write_text(filepath, content, encoding)


def read_bytes(filepath: Union[str, Path]) -> bytes:
    """
    Read a file as bytes.

    Args:
        filepath: Path to the file

    Returns:
        File contents as bytes
    """
    return Path(filepath).read_bytes()


def write_bytes(filepath: Union[str, Path], data: bytes) -> None:
    """
    Write bytes to a file.

    Args:
        filepath: Path to the file
        data: Bytes to write
    """
    Path(filepath).write_bytes(data)


def ensure_dir(dirpath: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        dirpath: Path to the directory

    Returns:
        Path object of the directory
    """
    path = Path(dirpath)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent_dir(filepath: Union[str, Path]) -> Path:
    """
    Ensure the parent directory of a file exists.

    Args:
        filepath: Path to the file

    Returns:
        Path object of the parent directory
    """
    parent = Path(filepath).parent
    parent.mkdir(parents=True, exist_ok=True)
    return parent


def exists(filepath: Union[str, Path]) -> bool:
    """
    Check if a file or directory exists.

    Args:
        filepath: Path to check

    Returns:
        True if exists, False otherwise
    """
    return Path(filepath).exists()


def is_file(filepath: Union[str, Path]) -> bool:
    """
    Check if a path is a file.

    Args:
        filepath: Path to check

    Returns:
        True if it's a file, False otherwise
    """
    return Path(filepath).is_file()


def is_dir(filepath: Union[str, Path]) -> bool:
    """
    Check if a path is a directory.

    Args:
        filepath: Path to check

    Returns:
        True if it's a directory, False otherwise
    """
    return Path(filepath).is_dir()


def get_extension(filepath: Union[str, Path]) -> str:
    """
    Get the file extension (including the dot).

    Args:
        filepath: Path to the file

    Returns:
        File extension (e.g., ".txt", ".json")
    """
    return Path(filepath).suffix


def get_stem(filepath: Union[str, Path]) -> str:
    """
    Get the file name without extension.

    Args:
        filepath: Path to the file

    Returns:
        File name without extension
    """
    return Path(filepath).stem


def get_name(filepath: Union[str, Path]) -> str:
    """
    Get the file name with extension.

    Args:
        filepath: Path to the file

    Returns:
        File name with extension
    """
    return Path(filepath).name


def get_parent(filepath: Union[str, Path]) -> Path:
    """
    Get the parent directory of a path.

    Args:
        filepath: Path to the file or directory

    Returns:
        Parent directory as a Path object
    """
    return Path(filepath).parent


def list_files(
    dirpath: Union[str, Path],
    pattern: str = "*",
    recursive: bool = False,
) -> List[Path]:
    """
    List files in a directory matching a pattern.

    Args:
        dirpath: Path to the directory
        pattern: Glob pattern (default: "*")
        recursive: Whether to search recursively (default: False)

    Returns:
        List of Path objects
    """
    path = Path(dirpath)
    if recursive:
        return list(path.rglob(pattern))
    return list(path.glob(pattern))


def copy_file(
    src: Union[str, Path],
    dst: Union[str, Path],
    create_dirs: bool = True,
) -> Path:
    """
    Copy a file to a destination.

    Args:
        src: Source file path
        dst: Destination path
        create_dirs: Whether to create parent directories (default: True)

    Returns:
        Path to the copied file
    """
    src_path = Path(src)
    dst_path = Path(dst)

    if create_dirs:
        ensure_parent_dir(dst_path)

    shutil.copy2(src_path, dst_path)
    return dst_path


def move_file(
    src: Union[str, Path],
    dst: Union[str, Path],
    create_dirs: bool = True,
) -> Path:
    """
    Move a file to a destination.

    Args:
        src: Source file path
        dst: Destination path
        create_dirs: Whether to create parent directories (default: True)

    Returns:
        Path to the moved file
    """
    src_path = Path(src)
    dst_path = Path(dst)

    if create_dirs:
        ensure_parent_dir(dst_path)

    shutil.move(str(src_path), str(dst_path))
    return dst_path


def delete_file(filepath: Union[str, Path], missing_ok: bool = True) -> None:
    """
    Delete a file.

    Args:
        filepath: Path to the file
        missing_ok: Whether to ignore if file doesn't exist (default: True)
    """
    path = Path(filepath)
    if missing_ok and not path.exists():
        return
    path.unlink()


def delete_dir(
    dirpath: Union[str, Path],
    missing_ok: bool = True,
) -> None:
    """
    Delete a directory and all its contents.

    Args:
        dirpath: Path to the directory
        missing_ok: Whether to ignore if directory doesn't exist (default: True)
    """
    path = Path(dirpath)
    if missing_ok and not path.exists():
        return
    shutil.rmtree(path)


def get_size(filepath: Union[str, Path]) -> int:
    """
    Get the size of a file in bytes.

    Args:
        filepath: Path to the file

    Returns:
        File size in bytes
    """
    return Path(filepath).stat().st_size


def get_size_human(filepath: Union[str, Path]) -> str:
    """
    Get the size of a file in human-readable format.

    Args:
        filepath: Path to the file

    Returns:
        File size as a human-readable string (e.g., "1.5 MB")
    """
    size = get_size(filepath)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def join_path(*parts: Union[str, Path]) -> Path:
    """
    Join path parts into a single path.

    Args:
        *parts: Path parts to join

    Returns:
        Combined Path object
    """
    return Path(*parts)


def resolve_path(filepath: Union[str, Path]) -> Path:
    """
    Resolve a path to an absolute path.

    Args:
        filepath: Path to resolve

    Returns:
        Absolute Path object
    """
    return Path(filepath).resolve()


class ObjectStorage:
    """
    Simple file-based object storage for persisting data with key-based access.

    Supports reading/writing text, JSON, and binary data with automatic
    directory creation and key-based file organization.
    """

    def __init__(self, base_path: Union[str, Path]):
        """
        Initialize the object storage.

        Args:
            base_path: Base directory path for storing objects
        """
        self._base_path = Path(base_path)
        self._base_path.mkdir(parents=True, exist_ok=True)

    @property
    def base_path(self) -> Path:
        """Return the base storage path."""
        return self._base_path

    def _get_full_path(self, key: str) -> Path:
        """Get the full file path for a key."""
        return self._base_path / key

    def read(self, key: str) -> Union[str, dict, list]:
        """
        Read data from storage. Automatically parses JSON if valid.

        Args:
            key: Storage key (relative path)

        Returns:
            Parsed JSON data (dict/list) or raw string
        """
        path = self._get_full_path(key)
        content = path.read_text(encoding="utf-8")
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return content

    def read_text(self, key: str, encoding: str = "utf-8") -> str:
        """
        Read data as text without JSON parsing.

        Args:
            key: Storage key (relative path)
            encoding: File encoding (default: "utf-8")

        Returns:
            File contents as string
        """
        return self._get_full_path(key).read_text(encoding=encoding)

    def read_bytes(self, key: str) -> bytes:
        """
        Read data as bytes.

        Args:
            key: Storage key (relative path)

        Returns:
            File contents as bytes
        """
        return self._get_full_path(key).read_bytes()

    def write(
        self,
        key: str,
        data: Union[str, bytes, dict, list],
        encoding: str = "utf-8",
    ) -> None:
        """
        Write data to storage.

        Args:
            key: Storage key (relative path)
            data: Data to write (str, bytes, dict, or list)
            encoding: File encoding for text data (default: "utf-8")

        Raises:
            TypeError: If data type is not supported
        """
        path = self._get_full_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(data, bytes):
            path.write_bytes(data)
        elif isinstance(data, str):
            path.write_text(data, encoding=encoding)
        elif isinstance(data, (dict, list)):
            content = json.dumps(data, ensure_ascii=False, default=str)
            path.write_text(content, encoding=encoding)
        else:
            raise TypeError(f"Unsupported data type: {type(data).__name__}")

    def delete(self, key: str, missing_ok: bool = False) -> None:
        """
        Delete a key from storage.

        Args:
            key: Storage key (relative path)
            missing_ok: If True, don't raise error if key doesn't exist
        """
        path = self._get_full_path(key)
        path.unlink(missing_ok=missing_ok)

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in storage.

        Args:
            key: Storage key (relative path)

        Returns:
            True if key exists, False otherwise
        """
        return self._get_full_path(key).exists()

    def list_dirs(self) -> List[str]:
        """
        List immediate subdirectories in the storage root.

        Returns:
            List of directory names
        """
        return [p.name for p in self._base_path.iterdir() if p.is_dir()]

    def list_keys(self, prefix: str = "") -> List[str]:
        """
        List all keys (files) in storage, optionally filtered by prefix.

        Args:
            prefix: Key prefix to filter by (default: "")

        Returns:
            List of keys (relative paths from base)
        """
        base = self._base_path / prefix if prefix else self._base_path
        if not base.exists():
            return []

        keys = []
        for path in base.rglob("*"):
            if path.is_file():
                keys.append(str(path.relative_to(self._base_path)))
        return keys
