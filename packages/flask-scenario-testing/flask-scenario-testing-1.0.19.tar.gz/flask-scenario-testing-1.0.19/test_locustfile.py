import datetime

from locust import task, HttpUser, between, SequentialTaskSet
import random
import time
from urllib.parse import urlencode


class LoadTest(SequentialTaskSet):
    _base_headers = {'Content-Type': 'application/json'}
    limit = 10
    offset = 0
    current_article = None
    query_params = {}
    session_id = None

    _recommended_articles = []
    _interesting_topics = []
    _subscribed_topics = []

    def headers(self):
        return {
            'sent-at': str(time.time())
        }

    def make_url(self, url, query_params: dict = None):
        if not query_params:
            query_params = {}

        if self.session_id:
            query_params['session'] = self.session_id

        encoded_query_string = urlencode(query_params)

        if encoded_query_string == '':
            return url

        return '{}?{}'.format(url, urlencode(query_params))

    def post(self, url, query_params: dict = None, data=None):
        url = self.make_url(url, query_params)

        return self.client.post(
            url,
            headers=self.headers(),
            data=data
        )

    def get(self, url, query_params: dict = None):
        if not url.startswith('/'):
            url = '/' + url

        url = self.make_url(url, query_params)

        return self.client.get(url)

    @task()
    def task_register(self):
        self.get('/')


class User(HttpUser):
    tasks = [LoadTest]

    wait_time = between(7, 15)
