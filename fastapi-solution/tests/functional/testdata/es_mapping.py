MOVIE_MAPPING = {
    "mappings": {
        "properties": {
            "uuid": {"type": "keyword"},
            "imdb_rating": {"type": "float"},
            "genre": {"type": "keyword"},
            "title": {"type": "text"},
            "description": {"type": "text"},
            "director": {"type": "keyword"},
            "actors_names": {"type": "keyword"},
            "writers_names": {"type": "keyword"},
            "actors": {
                "type": "nested",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "keyword"}
                }
            },
            "writers": {
                "type": "nested",
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "keyword"}
                }
            },
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"},
            "film_work_type": {"type": "keyword"}
        }
    }
}
