FROM python:3.10

WORKDIR /sxcne

COPY . .

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

CMD ["sh", "-c", "./scripts/serve.sh"]
