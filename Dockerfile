ARG PYTHON_VER=3.8

FROM python:${PYTHON_VER} AS base

WORKDIR /usr/src/app

# Install poetry for dep management
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="$PATH:/root/.poetry/bin"
RUN poetry config virtualenvs.create false

# Install project manifest
COPY poetry.lock pyproject.toml ./

# Install production dependencies
RUN poetry install --no-dev

FROM base AS test

COPY . .
# # Install full dependencies
# # Copy in only pyproject.toml/poetry.lock to help with caching this layer if no updates to dependencies
COPY pyproject.toml poetry.lock ./
# --no-root declares not to install the project package since we're wanting to take advantage of caching dependency installation
# and the project is copied in and installed after this step
RUN poetry install --no-interaction --no-ansi --no-root

############
# Runs all necessary linting and code checks
RUN echo 'Running Flake8' && \
    flake8 . && \
    echo 'Running Black' && \
    black --check --diff . && \
    echo 'Running Yamllint' && \
    yamllint . && \
    echo 'Running pydocstyle' && \
    pydocstyle . && \
    echo 'Running Bandit' && \
    bandit --recursive ./ --configfile .bandit.yml

ENTRYPOINT ["pytest", "--disable-pytest-warnings", "tests"]

