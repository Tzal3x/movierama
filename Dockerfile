FROM --platform=x86_64 python:3.10-alpine 

WORKDIR /movierama
COPY ./app /movierama/app 
COPY ./requirements.txt /movierama/requirements.txt
COPY ./alembic.ini /movierama/alembic.ini
COPY ./migrations /movierama/migrations
COPY ./templates /movierama/templates
RUN pip install --no-cache-dir --upgrade -r /movierama/requirements.txt

EXPOSE 80
