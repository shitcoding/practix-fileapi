import logging
from dataclasses import asdict

import backoff
from elastic_transport import ConnectionError
from elasticsearch import Elasticsearch as ES
from elasticsearch.helpers import bulk
from http import HTTPStatus

from data import ESData, ESGenre
from config.es_schema import SETTINGS ,FILMWORK_MAPPING, GENRE_MAPPING

logger = logging.getLogger(__name__)


class ESLoader:
    @backoff.on_exception(backoff.expo, ConnectionError)
    def __init__(self, es_server: str):
        self._es = ES(es_server)
        indexes = {'movies': FILMWORK_MAPPING,
                   'genres': GENRE_MAPPING}
        for index in indexes:
            mapping = {'settings': SETTINGS,
                       'mappings': indexes[index]}
            response = self._es.indices.create(index=index, body=mapping, ignore=HTTPStatus.BAD_REQUEST)
            if 'acknowledged' in response:
                if response['acknowledged']:
                    logging.info('Индекс создан: {}'.format(response['index']))
            elif 'error' in response:
                logger.error('Ошибка: {}'.format(response['error']['root_cause']))
            logging.info(response)

    @backoff.on_exception(backoff.expo, ConnectionError)
    def load_es_data(self, movies: list[ESData]):
        logger.info(f'Processing {len(movies)} movie:')
        actions = []
        for movie in movies:
            action = {
                '_index': 'movies',
                '_id': movie.id,
                '_source': asdict(movie),
            }
            actions.append(action)
        bulk(self._es, actions)
        logger.info(f'Transfer completed, {len(movies)} updated...')
        return len(movies)

    @backoff.on_exception(backoff.expo, ConnectionError)
    def load_es_genre(self, genres: list[ESGenre]):
        logger.info(f'Processing {len(genres)} genre:')
        actions = []
        for genre in genres:
            action = {
                '_index': 'genres',
                '_id': genre.id,
                '_source': asdict(genre),
            }
            actions.append(action)
        bulk(self._es, actions)
        logger.info(f'Transfer completed, {len(genres)} updated...')
        return len(genres)
