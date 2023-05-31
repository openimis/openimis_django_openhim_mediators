FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

RUN mkdir /mediators
WORKDIR /mediators
COPY ./mediators /mediators

WORKDIR /code

COPY ./mediators/manage.py /code/manage.py

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD python manage.py runserver