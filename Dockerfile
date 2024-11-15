FROM python:3.12.5-slim

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==1.8.3

WORKDIR /app

# Install app dependencies
COPY pyproject.toml poetry.lock ./
RUN touch README.md
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Install the app
COPY hole_filling ./hole_filling
RUN poetry install --without dev

# Add venv/bin to path, so python could be loaded from there
ENV VIRTUAL_ENV=./.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# ENTRYPOINT ["poetry", "run", "python", "-m", "hole_filling"]
ENTRYPOINT [ "/bin/bash" ]
