import json
from pathlib import Path
from uuid import uuid4

import pytest
from deep_compare import CompareVariables

from tests import TMP_DIR
from parser.settings import Settings

DEFAULT_CONFIG = {
    "output_directory": "./out",
    "categories": [],
    "delay_range_s": 0,
    "max_retries": 0,
    "headers": {},
    "logs_dir": "./",
    "restart": {
      "restart_count": 0,
      "interval_m": 0
    }
}


def create_config(data):
    name = uuid4().hex

    path = TMP_DIR / f'{name}.json'

    with open(path, 'w') as file:
        file.write(json.dumps(data))

    return path


def assert_defaults(settings):
    schema = settings.schema()

    props = schema['properties']

    for key, value in props.items():
        if 'default' not in value:
            continue

        assert value['default'] == getattr(settings, key)


def assert_settings_values(settings, passed_values):
    for key, value in passed_values.items():
        s_value = getattr(settings, key)

        if isinstance(s_value, Path):
            assert s_value == Path(value)

            continue

        assert CompareVariables.compare(s_value, value)


@pytest.fixture
def empty_config():
    path = create_config(dict())

    yield path

    path.unlink()


@pytest.fixture
def default_config():
    path = create_config(DEFAULT_CONFIG)

    yield path

    path.unlink()


def test_config_gets_loaded_with_default_values_if_file_does_not_exist():
    name = f'{uuid4().hex}.json'

    fake_path = TMP_DIR / f'{name}'

    s = Settings(fake_path)

    assert_defaults(s)


def test_config_gets_loaded_with_default_values_with_empty_config(empty_config):
    s = Settings(empty_config)

    assert_defaults(s)


def test_config_gets_loaded_with_default_config(default_config):
    s = Settings(default_config)

    assert_settings_values(s, DEFAULT_CONFIG)


def test_categories_passed_as_string_gets_converted_into_list():
    config = {
        **DEFAULT_CONFIG,
        'categories': ''
    }

    path = create_config(config)

    try:
        s = Settings(path)

        assert isinstance(s.categories, list)
    finally:
        path.unlink()


def test_settings_constructor_returns_the_same_instance():
    s1 = Settings()

    s2 = Settings()

    assert id(s1) == id(s2)
