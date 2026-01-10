import pyarrow as pa
from pyiceberg.catalog import load_catalog


class Iceberg:
    def __init__(self, iceberg_catalog_uri: str="http://localhost:8181"):
        self._catalog = load_catalog(
            "rest",
            **{
                "type": "rest",
                "uri": iceberg_catalog_uri,
            },
        )

    @property
    def catalog(self):
        return self._catalog
