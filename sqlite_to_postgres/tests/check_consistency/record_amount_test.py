"""Тесты количества записей в таблицах"""


class TestRecordAmount:
    def test_amount_person(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:
            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT count(*) FROM person")
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT count(*) FROM person")
            sqlite_data = _sqlite_cursor.fetchone()
            pg_data = _pg_cursor.fetchone()
            assert sqlite_data['count(*)'] == pg_data['count']

    def test_amount_genre(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:
            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT count(*) FROM genre")
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT count(*) FROM genre")
            sqlite_data = _sqlite_cursor.fetchone()
            pg_data = _pg_cursor.fetchone()
            assert sqlite_data['count(*)'] == pg_data['count']

    def test_amount_film_work(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:
            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT count(*) FROM film_work")
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT count(*) FROM film_work")
            sqlite_data = _sqlite_cursor.fetchone()
            pg_data = _pg_cursor.fetchone()
            assert sqlite_data['count(*)'] == pg_data['count']

    def test_amount_genre_film_work(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:
            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT count(*) FROM genre_film_work")
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT count(*) FROM genre_film_work")
            sqlite_data = _sqlite_cursor.fetchone()
            pg_data = _pg_cursor.fetchone()
            assert sqlite_data['count(*)'] == pg_data['count']

    def test_amount_person_film_work(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:
            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT count(*) FROM person_film_work")
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT count(*) FROM person_film_work")
            sqlite_data = _sqlite_cursor.fetchone()
            pg_data = _pg_cursor.fetchone()
            assert sqlite_data['count(*)'] == pg_data['count']
