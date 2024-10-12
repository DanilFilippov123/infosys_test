FROM python:3.12-bookworm
LABEL authors="danil"

RUN apt update && apt install libpq-dev

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "run.sh"]