import time
import random
from pathlib import Path
from typing import Union, Any
from dataclasses import dataclass, field
from bs4 import BeautifulSoup

from requests import Response

from parser.utils.http import HTTP

HOST = 'https://zootovary.ru'


@dataclass
class Parser(HTTP):
    delay_range: Union[int, tuple[int, int]] = 0

    _last_request: Union[float, None] = field(default=None, init=False)

    def get_delay(self) -> int:
        if isinstance(self.delay_range, int):
            return self.delay_range

        return random.randint(*self.delay_range)

    @property
    def wait_time(self) -> float:
        if not self._last_request:
            return 0

        delay = self.get_delay()

        now = time.time()

        return max(delay - (now - self._last_request), 0)

    def get(self, uri: str) -> Response:
        wait_time = self.wait_time

        time.sleep(wait_time)

        if not uri.startswith('/'):
            uri = f'/{uri}'

        return super().get(f'{HOST}{uri}')

    def get_html(self, uri: str) -> str:
        response = self.get(uri)

        return response.text

    def get_soup(self, uri: str) -> BeautifulSoup:
        html = self.get_html(uri)

        return BeautifulSoup(html, 'html.parser')

    @property
    def data(self) -> Any:
        pass
