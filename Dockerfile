ARG PYTHON_VER=3.8

FROM python:${PYTHON_VER} AS base

WORKDIR /usr/src/app

RUN pip install -U pip  && \
    curl -sSL https://install.python-poetry.org  | python3 -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

# Install project manifest
COPY poetry.lock pyproject.toml ./

# Install production dependencies
RUN poetry install --no-root

FROM base AS test

COPY . .

RUN poetry install --no-interaction

# Runs all necessary linting and code checks
RUN echo 'Rnning Ruff' && \
    ruff . && \
    echo 'Running Black' && \
    black --check --diff . && \
    echo 'Running Yamllint' && \
    yamllint . && \
    echo 'Running Pylint' && \
    find . -name '*.py' | xargs pylint  && \
    # echo 'Running pydocstyle' && \
    # pydocstyle . && \
    echo 'Running Bandit' && \
    bandit --recursive ./ --configfile .bandit.yml  && \
    echo 'Running MyPy' && \
    mypy .

# Run full test suite including integration
ENTRYPOINT ["pytest"]

CMD ["--cov=nornir_netconf/", "tests/", "-vvv"]
