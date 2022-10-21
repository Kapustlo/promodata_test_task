import json
from pathlib import Path
from functools import partial
from typing import TypeVar, Any, Union

from pydantic import BaseSettings, Field

from .utils import Singleton

T = TypeVar('T', bound='Settings')

DEFAULT_CONFIG_PATH = 'config.json'


def normalize_config(data: dict[str, Any]) -> dict[str, Any]:
    if isinstance(data.get('categories'), str):
        data['categories'] = data.pop('categories').split(',')

    return data


def get_config(
    settings: BaseSettings,
    config_path: Union[str, Path] = DEFAULT_CONFIG_PATH
) -> dict[str, Any]:
    path = Path(config_path)

    if not path.exists():
        return dict()

    text = path.read_text()

    data = json.loads(text)

    return normalize_config(data)


class Settings(Singleton, BaseSettings):
    output_directory: Path = Field(default_factory=partial(Path, 'out'))
    categories: list[str] = Field(default_factory=list)
    delay_range_s: Union[tuple[int, int], int] = 0
    max_retries: int = 0
    headers: dict[str, str] = Field(default_factory=dict)
    logs_dir: Union[Path, None] = None
    restart: Union[dict[str, int], None] = None

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings
        ):
            config_path = env_settings.env_file or DEFAULT_CONFIG_PATH

            return (
                init_settings,
                partial(get_config, config_path=config_path),
                env_settings,
                file_secret_settings
            )
