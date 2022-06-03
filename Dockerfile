FROM python:3.7-alpine
WORKDIR /fakegen
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev
RUN pip install "poetry"
COPY poetry.lock pyproject.toml .
RUN poetry install
COPY /fakegen/fakegen.py .
COPY /sql/. ./sql/
CMD ["python", "fakegen.py"]
