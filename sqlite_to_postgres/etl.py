from extraction import SQLiteExtractor
from loading import PostgresLoader


class ETL:
    def __init__(self, extractor: SQLiteExtractor, loader: PostgresLoader):
        self._extractor = extractor
        self._loader = loader

    def save_all_data(self, chunk_size: int):
        tables = ['person', 'genre', 'film_work', 'person_film_work', 'genre_film_work']

        for table in tables:
            table_size = self._extractor.get_size_table(table)

            parts = table_size // chunk_size
            current_offset = 0

            for part_num in range(parts + 1):
                data = self._extractor.extract_table(table, limit=chunk_size, offset=current_offset)
                current_offset += chunk_size
                self._loader.load_to_table(table, data)
