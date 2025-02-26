FROM python:3.12-slim

WORKDIR .

RUN pip install --no-cache poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY bot ./bot

# Команда для запуска приложения
CMD ["poetry", "run", "python", "bot/main.py"]