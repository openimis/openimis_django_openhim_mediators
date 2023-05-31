FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./mediators /code/mediators

WORKDIR /code/mediators

RUN sed -i 's/from collections import Mapping/from collections.abc import Mapping/g' manage.py

# Downgrade urllib3 to a compatible version
RUN pip install urllib3==1.26.7

RUN python manage.py makemigrations
RUN python manage.py migrate

WORKDIR /code

CMD python manage.py runserver
