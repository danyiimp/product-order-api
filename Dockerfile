FROM python:3.12-alpine AS base

WORKDIR /code

RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -q -r /code/requirements.txt
COPY ./app /code/app

FROM base AS testing
COPY ./requirements-dev.txt /code/requirements-dev.txt
RUN pip install --no-cache-dir -q -r /code/requirements-dev.txt
COPY ./tests /code/tests
COPY ./pytest.ini /code/pytest.ini

FROM base AS production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]