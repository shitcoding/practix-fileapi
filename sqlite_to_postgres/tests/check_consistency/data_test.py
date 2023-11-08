from datetime import datetime


class TestData:

    def test_person_data(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:
            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT * FROM person order by id")
            sqlite_data = _sqlite_cursor.fetchall()
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT * FROM person order by id")
            pg_data = _pg_cursor.fetchall()
            for row in range(len(sqlite_data)):
                assert pg_data[row]['id'] == sqlite_data[row]['id']
                assert pg_data[row]['full_name'] == sqlite_data[row]['full_name']
                assert pg_data[row]['created'] == datetime.strptime(sqlite_data[row]['created_at'] + "00",
                                                                    '%Y-%m-%d %H:%M:%S.%f%z')
                assert pg_data[row]['modified'] == datetime.strptime(sqlite_data[row]['updated_at'] + "00",
                                                                     '%Y-%m-%d %H:%M:%S.%f%z')

    def test_genre_data(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:
            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT * FROM genre order by id")
            sqlite_data = _sqlite_cursor.fetchall()
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT * FROM genre order by id")
            pg_data = _pg_cursor.fetchall()

            for row in range(len(sqlite_data)):
                assert pg_data[row]['id'] == sqlite_data[row]['id']
                assert pg_data[row]['name'] == sqlite_data[row]['name']
                assert pg_data[row]['description'] == sqlite_data[row]['description']
                assert pg_data[row]['created'] == datetime.strptime(sqlite_data[row]['created_at'] + "00",
                                                                    '%Y-%m-%d %H:%M:%S.%f%z')
                assert pg_data[row]['modified'] == datetime.strptime(sqlite_data[row]['updated_at'] + "00",
                                                                     '%Y-%m-%d %H:%M:%S.%f%z')

    def test_film_work_data(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:

            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT * FROM film_work order by id")
            sqlite_data = _sqlite_cursor.fetchall()
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT * FROM film_work order by id")
            pg_data = _pg_cursor.fetchall()

            for row in range(len(sqlite_data)):
                assert pg_data[row]['id'] == sqlite_data[row]['id']
                assert pg_data[row]['title'] == sqlite_data[row]['title']
                assert pg_data[row]['description'] == sqlite_data[row]['description']
                if sqlite_data[row]['creation_date'] is not None:
                    sqlite_data[row]['creation_date'] = datetime.strptime(sqlite_data[row]['creation_date'] + "00",
                                                                          '%Y-%m-%d %H:%M:%S.%f%z')
                assert pg_data[row]['creation_date'] == sqlite_data[row]['creation_date']
                assert pg_data[row]['file_path'] == sqlite_data[row]['file_path']
                assert pg_data[row]['rating'] == sqlite_data[row]['rating']
                assert pg_data[row]['type'] == sqlite_data[row]['type']
                assert pg_data[row]['created'] == datetime.strptime(sqlite_data[row]['created_at'] + "00",
                                                                    '%Y-%m-%d %H:%M:%S.%f%z')
                assert pg_data[row]['modified'] == datetime.strptime(sqlite_data[row]['updated_at'] + "00",
                                                                     '%Y-%m-%d %H:%M:%S.%f%z')

    def test_person_film_work_data(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:
            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT * FROM person_film_work order by id")
            sqlite_data = _sqlite_cursor.fetchall()
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT * FROM person_film_work order by id")
            pg_data = _pg_cursor.fetchall()
            for row in range(len(sqlite_data)):
                assert pg_data[row]['id'] == sqlite_data[row]['id']
                assert pg_data[row]['film_work_id'] == sqlite_data[row]['film_work_id']
                assert pg_data[row]['person_id'] == sqlite_data[row]['person_id']
                assert pg_data[row]['role'] == sqlite_data[row]['role']
                assert pg_data[row]['created'] == datetime.strptime(sqlite_data[row]['created_at'] + "00",
                                                                    '%Y-%m-%d %H:%M:%S.%f%z')

    def test_genre_film_work_data(self):
        with self.sqlite_conn as _sqlite,\
                self.pg_conn as _pg:
            _sqlite_cursor = _sqlite.cursor()
            _sqlite_cursor.execute("SELECT * FROM genre_film_work order by id")
            sqlite_data = _sqlite_cursor.fetchall()
            _pg_cursor = _pg.cursor()
            _pg_cursor.execute("SELECT * FROM genre_film_work order by id")
            pg_data = _pg_cursor.fetchall()
            for row in range(len(sqlite_data)):
                assert pg_data[row]['id'] == sqlite_data[row]['id']
                assert pg_data[row]['film_work_id'] == sqlite_data[row]['film_work_id']
                assert pg_data[row]['genre_id'] == sqlite_data[row]['genre_id']
                assert pg_data[row]['created'] == datetime.strptime(sqlite_data[row]['created_at'] + "00",
                                                                    '%Y-%m-%d %H:%M:%S.%f%z')
