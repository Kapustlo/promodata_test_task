from dataclasses import dataclass, field

import requests
from requests import Response
from requests.adapters import HTTPAdapter, Retry


@dataclass
class HTTP:
    max_retries: int = 0
    headers: dict[str, str] = field(default_factory=dict)
    session: requests.Session = field(
        default_factory=requests.Session,
        init=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        retries = Retry(total=self.max_retries)

        self.session.mount('http://', HTTPAdapter(max_retries=retries))

    def get(self, url) -> Response:
        return self.session.get(url)
