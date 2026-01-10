import duckdb

class DuckDB():
    def __init__(self):
        self._connection = self.connect()

    @property
    def connection(self):
        return self._connection

    def connect(self, endpoint="http://iceberg-rest:8181"):
        conn = duckdb.connect()
        conn.execute("INSTALL iceberg; LOAD iceberg;")
        conn.execute("""
            ATTACH '' AS iceberg (
                TYPE iceberg,
                ENDPOINT 'http://localhost:8181',
                AUTHORIZATION_TYPE 'none'
            )
        """)
        return conn