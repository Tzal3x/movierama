# 🎥 MovieRama

Yet​ ​another social​ ​sharing​ ​platform​ ​where​ ​users​ ​can​ ​share​ ​their​ ​favorite​ ​movies.

## Installation

Create a `.env` file in the project's root directory (i.e. `/movierama/.env`)
with the following contents:

```
DB_SERVICE=postgresql
DB_USERNAME=postgres
DB_PASSWORD=<A_VERY_STRONG_PASSWORD>
DB_NAME=movierama
DB_PORT=5432

DB_HOST=postgres:5432

HASH_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
TOKEN_CREATION_SECRET_KEY=<use a token creation key>
```

⚠️ **Warning!** The field values are examples. You should use different values for safety purposes.

Then, to run the app just type on the cmd

`docker compose up -d`

## Access

Access the app on: `https://localhost:8000/`

The API documentation can be found on https://localhost:8000/docs or https://localhost:8000/redoc.

## Testing

Run the unit tests with

`$ docker exec -it movierama sh -c "pytest"`

## Screenshots

![Screenshot from 2023-07-31 01-31-48](https://github.com/Tzal3x/movierama/assets/33265837/ed01d0f6-2d62-464b-88f3-a0045a8123a2)

![Screenshot from 2023-07-31 01-32-35](https://github.com/Tzal3x/movierama/assets/33265837/023d2583-b6b8-435c-b9df-2b3f108f1d57)

## Local development

To run the app locally, you need to have Python 3.8+ installed.

Create a virtual environment:

```
python -m venv venv
```

Install the dependencies:

```
pip install -r requirements.txt
```

Setup the database:

```
docker compose up -d postgres
```

Run the migrations:

```
alembic upgrade head
```

Run the app:

```
uvicorn app.main:app --reload
```
