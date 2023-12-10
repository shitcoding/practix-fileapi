MOVIE_MAPPING = {
        "dynamic": "strict",
        "properties": {
          "uuid": {
            "type": "keyword"
          },
          "imdb_rating": {
            "type": "float"
          },
          "genre": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
              "uuid": {
                "type": "keyword"
              },
              "name": {
                "type": "text",
                "analyzer": "ru_en"
              }
            }
          },
          "title": {
            "type": "text",
            "analyzer": "ru_en",
            "fields": {
              "raw": {
                "type":  "keyword"
              }
            }
          },
          "description": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "directors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
              "uuid": {
                "type": "keyword"
              },
              "full_name": {
                "type": "text",
                "analyzer": "ru_en"
              }
            }
          },
          "actors_names": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "writers_names": {
            "type": "text",
            "analyzer": "ru_en"
          },
          "actors": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
              "uuid": {
                "type": "keyword"
              },
              "full_name": {
                "type": "text",
                "analyzer": "ru_en"
              }
            }
          },
          "writers": {
            "type": "nested",
            "dynamic": "strict",
            "properties": {
              "uuid": {
                "type": "keyword"
              },
              "full_name": {
                "type": "text",
                "analyzer": "ru_en"
              }
            }
          }
        }
      }