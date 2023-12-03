import datetime
import uuid
import random

TEST_MOVIE_DATA = {
    'uuid': str(uuid.uuid4()),
    'imdb_rating': 8.5,
    'genre': ['Action', 'Sci-Fi'],
    'title': 'The Star',
    'description': 'New World',
    'director': ['Stan'],
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'actors': [
        {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
        {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
    ],
    'writers': [
        {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
        {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
    ],
    'created_at': datetime.datetime.now().isoformat(),
    'updated_at': datetime.datetime.now().isoformat(),
    'film_work_type': 'movie'
}

_genres = ["Action", "Adventure", "Comedy", "Drama", "Horror"]

TEST_GENRE_DATA = [
  {
    "uuid": "0b105f87-e0a5-45dc-8ce7-f8632088f390",
    "name": "Western"
  },
  {
    "uuid": "120a21cf-9097-479e-904a-13dd7198c1dd",
    "name": "Adventure"
  },
  {
    "uuid": "1cacff68-643e-4ddd-8f57-84b62538081a",
    "name": "Drama"
  },
  {
    "uuid": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
    "name": "Romance"
  },
  {
    "uuid": "2f89e116-4827-4ff4-853c-b6e058f71e31",
    "name": "Sport"
  },
  {
    "uuid": "31cabbb5-6389-45c6-9b48-f7f173f6c40f",
    "name": "Talk-Show"
  },
  {
    "uuid": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
    "name": "Action"
  },
  {
    "uuid": "526769d7-df18-4661-9aa6-49ed24e9dfd8",
    "name": "Thriller"
  },
  {
    "uuid": "5373d043-3f41-4ea8-9947-4b746c601bbd",
    "name": "Comedy"
  },
  {
    "uuid": "55c723c1-6d90-4a04-a44b-e9792040251a",
    "name": "Family"
  }
]
