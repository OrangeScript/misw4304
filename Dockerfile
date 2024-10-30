FROM python:3.10.11

WORKDIR /

RUN pip install pipenv

COPY Pipfile* ./

RUN pipenv shell

RUN pipenv install

RUN pipenv sync

COPY . .

EXPOSE 9000

CMD [ "pipenv", "run", "python", "application.py", "production"]
