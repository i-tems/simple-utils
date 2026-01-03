
import json
import os
import shutil
from pathlib import Path
from typing import Any, List, Optional, Union


class ObjectStorage:
    """
    키 기반 접근 방식으로 데이터를 저장하는 간단한 파일 기반 객체 저장소.

    텍스트, JSON, 바이너리 데이터의 읽기/쓰기를 지원하며,
    자동 디렉토리 생성 및 키 기반 파일 구성을 제공합니다.
    """

    def __init__(self, base_path: Union[str, Path]):
        """
        객체 저장소를 초기화합니다.

        Args:
            base_path: 객체를 저장할 기본 디렉토리 경로
        """
        self._base_path = Path(base_path)
        self._base_path.mkdir(parents=True, exist_ok=True)

    @property
    def base_path(self) -> Path:
        """기본 저장소 경로를 반환합니다."""
        return self._base_path

    def _get_full_path(self, key: str) -> Path:
        """키에 대한 전체 파일 경로를 반환합니다."""
        return self._base_path / key

    def read(self, key: str) -> Union[str, dict, list]:
        """
        저장소에서 데이터를 읽습니다. 유효한 JSON이면 자동으로 파싱합니다.

        Args:
            key: 저장소 키 (상대 경로)

        Returns:
            파싱된 JSON 데이터 (dict/list) 또는 원본 문자열
        """
        path = self._get_full_path(key)
        content = path.read_text(encoding="utf-8")
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return content

    def read_text(self, key: str, encoding: str = "utf-8") -> str:
        """
        JSON 파싱 없이 텍스트로 데이터를 읽습니다.

        Args:
            key: 저장소 키 (상대 경로)
            encoding: 파일 인코딩 (기본값: "utf-8")

        Returns:
            문자열로 된 파일 내용
        """
        return self._get_full_path(key).read_text(encoding=encoding)

    def read_bytes(self, key: str) -> bytes:
        """
        바이트로 데이터를 읽습니다.

        Args:
            key: 저장소 키 (상대 경로)

        Returns:
            바이트로 된 파일 내용
        """
        return self._get_full_path(key).read_bytes()

    def write(
        self,
        key: str,
        data: Union[str, bytes, dict, list],
        encoding: str = "utf-8",
    ) -> None:
        """
        저장소에 데이터를 씁니다.

        Args:
            key: 저장소 키 (상대 경로)
            data: 쓸 데이터 (str, bytes, dict, 또는 list)
            encoding: 텍스트 데이터의 파일 인코딩 (기본값: "utf-8")

        Raises:
            TypeError: 지원하지 않는 데이터 타입인 경우
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
            raise TypeError(f"지원하지 않는 데이터 타입: {type(data).__name__}")

    def delete(self, key: str, missing_ok: bool = False) -> None:
        """
        저장소에서 키를 삭제합니다.

        Args:
            key: 저장소 키 (상대 경로)
            missing_ok: True이면 키가 없어도 에러를 발생시키지 않음
        """
        path = self._get_full_path(key)
        path.unlink(missing_ok=missing_ok)

    def exists(self, key: str) -> bool:
        """
        저장소에 키가 존재하는지 확인합니다.

        Args:
            key: 저장소 키 (상대 경로)

        Returns:
            키가 존재하면 True, 그렇지 않으면 False
        """
        return self._get_full_path(key).exists()

    def list_dirs(self) -> List[str]:
        """
        저장소 루트의 직접 하위 디렉토리를 나열합니다.

        Returns:
            디렉토리 이름 목록
        """
        return [p.name for p in self._base_path.iterdir() if p.is_dir()]

    def list_keys(self, prefix: str = "") -> List[str]:
        """
        저장소의 모든 키(파일)를 나열하며, 선택적으로 접두사로 필터링합니다.

        Args:
            prefix: 필터링할 키 접두사 (기본값: "")

        Returns:
            키 목록 (기본 경로 기준 상대 경로)
        """
        base = self._base_path / prefix if prefix else self._base_path
        if not base.exists():
            return []

        keys = []
        for path in base.rglob("*"):
            if path.is_file():
                keys.append(str(path.relative_to(self._base_path)))
        return keys
