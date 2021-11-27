FROM python

RUN pip install poetry

WORKDIR /app

# builds the python lib
COPY poetry.lock pyproject.toml ./
COPY ./discounterland discounterland
RUN poetry build --format wheel

RUN pip install dist/discounterland-0.1.0-py3-none-any.whl

ENTRYPOINT ["discounterland"]
