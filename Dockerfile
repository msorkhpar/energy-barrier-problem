FROM python:3.10-slim-bullseye
RUN pip install --upgrade pip
WORKDIR /app
RUN mkdir "db"

COPY requirements.txt requirements.txt
COPY main.py main.py
COPY graph_generator graph_generator
COPY lp lp
COPY persistent persistent
COPY utility utility
ENV TZ America/Indiana/Indianapolis

RUN pip3 install -r requirements.txt


CMD ["python3", "main.py"]