from dataclasses import dataclass
from typing import Any

from bs4 import Tag


@dataclass
class BaseSerializer:
    element: Tag

    @property
    def data(self) -> Any:
        pass
