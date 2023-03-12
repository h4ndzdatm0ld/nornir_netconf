ARG PYTHON_VER=3.8

FROM python:${PYTHON_VER} AS base

WORKDIR /usr/src/app

RUN pip install -U pip  && \
    curl -sSL https://install.python-poetry.org  | python3 -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

FROM base AS test

COPY . .

RUN poetry install --no-interaction

RUN echo 'Rnning Ruff' && \
    ruff . && \
    echo 'Running Black' && \
    black --check --diff . && \
    echo 'Running Yamllint' && \
    yamllint . && \
    echo 'Running Bandit' && \
    bandit --recursive ./ --configfile .bandit.yml  && \
    echo 'Running MyPy' && \
    mypy .

ENTRYPOINT ["pytest"]

CMD ["--cov=nornir_netconf/", "tests/", "-vvv"]
