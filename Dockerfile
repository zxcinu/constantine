FROM python:3.8-slim-bullseye as builder

COPY pyproject.toml poetry.lock poetry.toml install/

WORKDIR install/

RUN pip install -U poetry && poetry install --no-dev

FROM builder

COPY --from=builder install/ /usr/local

COPY src/* config.yml app/

WORKDIR app/

RUN adduser --system --home /app constantine

USER constantine

ENV PATH=/install/.venv/bin:${PATH}

CMD python main.py
