# Требования
- Python 3.9+

# Установка зависимостей
```bash
pip install -r requirements.txt
```

# Запуск

```bash
python -m parser --config path_to_config
```

# Консольные параметры


| Аргумент | Описание | Обязательный | По умолчанию | Тип |
| ------ | ------ | ------ | ------ | ------ |
| --config | Путь к конфигурационному файлу парсера | False | ./config.json | str
| --help | Помощь | False | None | bool


# Тестирование

```bash
pytest tests/
```

GitHub мной не используется, актуальные репозитории:
- [NotABug](https://notabug.org/Kapustlo)
- [OneDev](https://git.kapnet.tech)
