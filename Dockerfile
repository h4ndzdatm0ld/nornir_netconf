ARG PYTHON_VER=3.9
ARG POETRY_VERSION=1.8.5

FROM python:${PYTHON_VER} AS base

ARG POETRY_VERSION

WORKDIR /usr/src/app

RUN pip install --upgrade pip "poetry==${POETRY_VERSION}"

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

FROM base AS test

COPY . .

RUN poetry install --no-interaction

RUN echo 'Running Ruff' && \
    ruff check . && \
    echo 'Running Black' && \
    black --check --diff . && \
    echo 'Running Yamllint' && \
    yamllint . && \
    echo 'Running Bandit' && \
    bandit --recursive ./ --configfile pyproject.toml  && \
    echo 'Running MyPy' && \
    mypy .

ENTRYPOINT ["pytest"]

CMD ["--cov=nornir_netconf/", "tests/", "-vvv"]
