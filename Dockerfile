
ARG VERSION=0.1.0

# build package
FROM python

RUN pip install poetry

WORKDIR /app

ARG VERSION

COPY poetry.lock pyproject.toml ./

COPY ./discounterland discounterland

RUN poetry build --format wheel


# build service
FROM python

RUN pip install gunicorn

ARG VERSION

ENV PACKAGE_FILE=discounterland-${VERSION}-py3-none-any.whl

COPY --from=0 /app/dist/${PACKAGE_FILE} .

RUN pip install ${PACKAGE_FILE}

RUN rm ${PACKAGE_FILE}

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "discounterland.app.wsgi"]
