FROM python:3.9-slim

ENV PYTHONPATH=/

COPY . /backend

WORKDIR /backend

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 7040

WORKDIR ../

CMD ["python", "backend/core/application.py"]