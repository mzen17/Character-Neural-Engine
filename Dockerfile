FROM python:3.10

COPY . .

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry run install

CMD ["sh", "-c", "run/serve.sh"]