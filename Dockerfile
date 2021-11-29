# build package

FROM python

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./

COPY ./discounterland discounterland

RUN poetry build --format wheel


# build service

FROm python

RUN pip install gunicorn

COPY --from=0 /app/dist/discounterland-0.1.0-py3-none-any.whl ./

RUN pip install discounterland-0.1.0-py3-none-any.whl

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "discounterland.app.wsgi"]
