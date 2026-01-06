"""Trino를 통한 Iceberg 테이블 인터페이스."""

import json
from typing import Any, Dict, List, Optional, Union

try:
    from trino.dbapi import connect
except ImportError:
    connect = None


class IcebergClient:
    """
    Trino를 통해 Iceberg 테이블과 상호작용하는 클라이언트.

    스키마 자동 관리 및 배치 작업을 지원하는 간단한 CRUD 작업을 제공한다.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8080,
        user: str = "trino",
        catalog: str = "local",
        schema: str = "default",
    ):
        """
        Iceberg 클라이언트 초기화.

        Args:
            host: Trino 호스트 (기본값: "localhost")
            port: Trino 포트 (기본값: 8080)
            user: Trino 사용자 (기본값: "trino")
            catalog: Iceberg 카탈로그 이름 (기본값: "local")
            schema: 기본 스키마 이름 (기본값: "default")
        """
        if connect is None:
            raise ImportError("trino 패키지가 필요합니다: pip install trino")

        self._host = host
        self._port = port
        self._user = user
        self._catalog = catalog
        self._schema = schema
        self._conn = None

    @property
    def connection(self):
        """Trino 연결을 가져오거나 생성한다."""
        if self._conn is None:
            self._conn = connect(
                host=self._host,
                port=self._port,
                user=self._user,
                catalog=self._catalog,
                schema=self._schema,
            )
        return self._conn

    def close(self):
        """연결을 종료한다."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        self.close()

    def execute(self, sql: str, fetch: bool = True) -> Optional[List[tuple]]:
        """
        SQL 문을 실행한다.

        Args:
            sql: 실행할 SQL 문
            fetch: 결과를 가져올지 여부 (기본값: True)

        Returns:
            fetch=True인 경우 결과 튜플 리스트, 그렇지 않으면 None
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)
        if fetch:
            try:
                return cursor.fetchall()
            except Exception:
                return None
        return None

    def execute_many(self, statements: List[str]) -> None:
        """
        여러 SQL 문을 실행한다.

        Args:
            statements: 실행할 SQL 문 리스트
        """
        for sql in statements:
            self.execute(sql, fetch=False)

    def _escape(self, value: Any) -> str:
        """SQL 삽입을 위해 값을 이스케이프한다."""
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        return "'" + str(value).replace("'", "''").replace("\\", "\\\\") + "'"

    def _full_table_name(self, table: str, schema: Optional[str] = None) -> str:
        """정규화된 테이블 이름을 반환한다."""
        s = schema or self._schema
        return f"{self._catalog}.{s}.{table}"

    # 스키마 작업

    def list_schemas(self) -> List[str]:
        """카탈로그의 모든 스키마를 나열한다."""
        result = self.execute(f"SHOW SCHEMAS FROM {self._catalog}")
        return [row[0] for row in result] if result else []

    def create_schema(self, schema: str, if_not_exists: bool = True) -> None:
        """스키마를 생성한다."""
        exists = "IF NOT EXISTS " if if_not_exists else ""
        self.execute(f"CREATE SCHEMA {exists}{self._catalog}.{schema}", fetch=False)

    def drop_schema(self, schema: str, if_exists: bool = True) -> None:
        """스키마를 삭제한다."""
        exists = "IF EXISTS " if if_exists else ""
        self.execute(f"DROP SCHEMA {exists}{self._catalog}.{schema}", fetch=False)

    # 테이블 작업

    def list_tables(self, schema: Optional[str] = None) -> List[str]:
        """스키마의 모든 테이블을 나열한다."""
        s = schema or self._schema
        result = self.execute(f"SHOW TABLES FROM {self._catalog}.{s}")
        return [row[0] for row in result] if result else []

    def table_exists(self, table: str, schema: Optional[str] = None) -> bool:
        """테이블이 존재하는지 확인한다."""
        return table in self.list_tables(schema)

    def create_table(
        self,
        table: str,
        columns: Dict[str, str],
        schema: Optional[str] = None,
        if_not_exists: bool = True,
        partitioned_by: Optional[List[str]] = None,
    ) -> None:
        """
        Iceberg 테이블을 생성한다.

        Args:
            table: 테이블 이름
            columns: 컬럼명 -> 컬럼타입 딕셔너리
            schema: 스키마 이름 (기본값: 인스턴스 스키마)
            if_not_exists: IF NOT EXISTS 절 추가 (기본값: True)
            partitioned_by: 파티션 컬럼 리스트 (기본값: None)

        Example:
            client.create_table("users", {
                "id": "VARCHAR",
                "name": "VARCHAR",
                "age": "INTEGER",
                "created_at": "TIMESTAMP"
            })
        """
        full_name = self._full_table_name(table, schema)
        exists = "IF NOT EXISTS " if if_not_exists else ""
        cols = ", ".join(f"{name} {dtype}" for name, dtype in columns.items())

        sql = f"CREATE TABLE {exists}{full_name} ({cols})"
        if partitioned_by:
            sql += f" WITH (partitioning = ARRAY{partitioned_by})"

        self.execute(sql, fetch=False)

    def drop_table(
        self, table: str, schema: Optional[str] = None, if_exists: bool = True
    ) -> None:
        """테이블을 삭제한다."""
        full_name = self._full_table_name(table, schema)
        exists = "IF EXISTS " if if_exists else ""
        self.execute(f"DROP TABLE {exists}{full_name}", fetch=False)

    def describe_table(
        self, table: str, schema: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        테이블 컬럼 정보를 가져온다.

        Returns:
            'name', 'type', 'nullable' 키를 가진 딕셔너리 리스트
        """
        full_name = self._full_table_name(table, schema)
        result = self.execute(f"DESCRIBE {full_name}")
        if not result:
            return []
        return [
            {"name": row[0], "type": row[1], "nullable": row[2] == "YES"}
            for row in result
        ]

    # 데이터 작업

    def insert(
        self,
        table: str,
        data: Union[Dict[str, Any], List[Dict[str, Any]]],
        schema: Optional[str] = None,
    ) -> int:
        """
        테이블에 데이터를 삽입한다.

        Args:
            table: 테이블 이름
            data: 삽입할 단일 딕셔너리 또는 딕셔너리 리스트
            schema: 스키마 이름 (기본값: 인스턴스 스키마)

        Returns:
            삽입된 행 수
        """
        if isinstance(data, dict):
            data = [data]

        if not data:
            return 0

        full_name = self._full_table_name(table, schema)
        columns = list(data[0].keys())
        col_names = ", ".join(columns)

        values = []
        for row in data:
            vals = ", ".join(self._escape(row.get(col)) for col in columns)
            values.append(f"({vals})")

        sql = f"INSERT INTO {full_name} ({col_names}) VALUES {', '.join(values)}"
        self.execute(sql, fetch=False)
        return len(data)

    def insert_batch(
        self,
        table: str,
        data: List[Dict[str, Any]],
        schema: Optional[str] = None,
        batch_size: int = 100,
    ) -> int:
        """
        배치로 데이터를 삽입한다.

        Args:
            table: 테이블 이름
            data: 삽입할 딕셔너리 리스트
            schema: 스키마 이름 (기본값: 인스턴스 스키마)
            batch_size: 배치당 행 수 (기본값: 100)

        Returns:
            삽입된 총 행 수
        """
        total = 0
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            total += self.insert(table, batch, schema)
        return total

    def query(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        where: Optional[str] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        schema: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        테이블에서 데이터를 조회한다.

        Args:
            table: 테이블 이름
            columns: 선택할 컬럼 (기본값: 전체)
            where: WHERE 절 ('WHERE' 키워드 제외)
            order_by: ORDER BY 절 ('ORDER BY' 키워드 제외)
            limit: 최대 행 수
            schema: 스키마 이름 (기본값: 인스턴스 스키마)

        Returns:
            행을 나타내는 딕셔너리 리스트
        """
        full_name = self._full_table_name(table, schema)
        cols = ", ".join(columns) if columns else "*"

        sql = f"SELECT {cols} FROM {full_name}"
        if where:
            sql += f" WHERE {where}"
        if order_by:
            sql += f" ORDER BY {order_by}"
        if limit:
            sql += f" LIMIT {limit}"

        cursor = self.connection.cursor()
        cursor.execute(sql)

        col_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(col_names, row)) for row in rows]

    def query_sql(self, sql: str) -> List[Dict[str, Any]]:
        """
        원시 SQL을 실행하고 결과를 딕셔너리로 반환한다.

        Args:
            sql: 실행할 SQL 쿼리

        Returns:
            행을 나타내는 딕셔너리 리스트
        """
        cursor = self.connection.cursor()
        cursor.execute(sql)

        col_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(col_names, row)) for row in rows]

    def count(
        self, table: str, where: Optional[str] = None, schema: Optional[str] = None
    ) -> int:
        """테이블의 행 수를 반환한다."""
        full_name = self._full_table_name(table, schema)
        sql = f"SELECT COUNT(*) FROM {full_name}"
        if where:
            sql += f" WHERE {where}"
        result = self.execute(sql)
        return result[0][0] if result else 0

    def delete(
        self, table: str, where: str, schema: Optional[str] = None
    ) -> None:
        """
        테이블에서 행을 삭제한다.

        Args:
            table: 테이블 이름
            where: WHERE 절 (안전을 위해 필수)
            schema: 스키마 이름 (기본값: 인스턴스 스키마)
        """
        full_name = self._full_table_name(table, schema)
        self.execute(f"DELETE FROM {full_name} WHERE {where}", fetch=False)

    def truncate(self, table: str, schema: Optional[str] = None) -> None:
        """테이블의 모든 행을 삭제한다."""
        full_name = self._full_table_name(table, schema)
        self.execute(f"DELETE FROM {full_name}", fetch=False)

    def update(
        self,
        table: str,
        values: Dict[str, Any],
        where: str,
        schema: Optional[str] = None,
    ) -> None:
        """
        테이블의 행을 업데이트한다.

        Args:
            table: 테이블 이름
            values: 컬럼 -> 새 값 딕셔너리
            where: WHERE 절 (안전을 위해 필수)
            schema: 스키마 이름 (기본값: 인스턴스 스키마)
        """
        full_name = self._full_table_name(table, schema)
        set_clause = ", ".join(
            f"{col} = {self._escape(val)}" for col, val in values.items()
        )
        self.execute(f"UPDATE {full_name} SET {set_clause} WHERE {where}", fetch=False)
