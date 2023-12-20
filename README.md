## Установка проекта
### Подгатовка окружения
- Изменить имя файл .env.example на .env
- Заполнить данные в .env
- установить Python ^3.10
- установить Poetry
- выполнить команды

```bash
poetry shell
poetry install
alembic upgrade head
```

### Запуск проекта
```bash
poetry shell
uvicorn app.main:app --host 0.0.0.0 --reload
```

