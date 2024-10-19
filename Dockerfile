FROM python:3.10.11

WORKDIR /

RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv install --system

RUN pipenv sync

COPY . .

EXPOSE 9000

CMD [ "pipenv", "run", "python", "app.py", "develop"]