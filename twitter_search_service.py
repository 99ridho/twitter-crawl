from http_client import (HTTPClient, HTTPRequestData)
from typing import (Optional, Any, Dict, List)
from config import BEARER_TOKEN
from urllib.parse import parse_qsl
import asyncio
import json

class TweetSearchData:
    def __init__(self, id: str, text: str, type: str):
        self.id = id
        self.text = text
        self.type = type

    def __repr__(self):
        return f'TweetSearchData(id = {self.id}, text = {self.text}, type = {self.type})'

class TweetSearchResponse:
    def __init__(self, data: List[TweetSearchData], next_result: str):
        self.data = data
        self.next_result = next_result

    def __repr__(self):
        return f'Response(data = {self.data}, next_result = {self.next_result})'

class TwitterSearchService:
    def __init__(self, query: str, max_item_count: int):
        self.http_client = HTTPClient()
        self.bearer_token = BEARER_TOKEN
        self.next_result_query = ''
        self.query = query
        self.max_item_count = max_item_count
        self.__lock = asyncio.Lock()

    def __make_search_data(self, tweet: Any) -> TweetSearchData:
        return TweetSearchData(
            id=tweet['id_str'],
            text=tweet['full_text'],
            type=tweet['metadata']['result_type']
        )

    async def __get_recent_tweet_search(self, params: Dict[str, any]) -> Optional[TweetSearchResponse]:
        headers: Dict[str, str] = {
            'Authorization': f'Bearer {self.bearer_token}'         
        }

        request_data = HTTPRequestData(
            'https://api.twitter.com/1.1',
            path='/search/tweets.json',
            method='GET',
            params=params,
            headers=headers
        )

        json = await self.http_client.request(request_data)
        if json is None:
            return None

        if 'next_results' not in json['search_metadata']:
            return None

        self.next_result_query = json['search_metadata']['next_results']
        tweets = list(map(self.__make_search_data, json['statuses']))
        return TweetSearchResponse(data=tweets, next_result=self.next_result_query)

    async def get_next_results(self) -> Optional[TweetSearchResponse]:
        async with self.__lock:
            param = {
                'q': f'{self.query} -filter:retweets',
                'count': self.max_item_count,
                'include_entities': 'false',
                'tweet_mode': 'extended',
                'result_type': 'mixed'
            }

            if not self.next_result_query:
                return await self.__get_recent_tweet_search(param)

            new_param = dict(parse_qsl(self.next_result_query[1:]))
            param['max_id'] = new_param['max_id']

            return await self.__get_recent_tweet_search(param)