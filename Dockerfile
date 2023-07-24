FROM python:3.10

COPY . .

RUN pip install -r requirements.txt

CMD ["sh", "-c", "run/serve.sh"]