FROM python:3.10-slim-bullseye
RUN pip install --upgrade pip
RUN useradd -m solver
USER solver
WORKDIR /home/solver
RUN mkdir "db"

COPY --chown=lp_user:lp_user requirements.txt requirements.txt
COPY --chown=lp_user:lp_user main.py main.py
COPY --chown=lp_user:lp_user graph_generator graph_generator
COPY --chown=lp_user:lp_user lp lp
COPY --chown=lp_user:lp_user persistent persistent
ENV TZ America/Indiana/Indianapolis


RUN pip3 install --user -r requirements.txt
ENV PATH="/home/solver/.local/bin:${PATH}"

CMD ["python3", "main.py"]