# 🎥 MovieRama
Yet​ ​another social​ ​sharing​ ​platform​ ​where​ ​users​ ​can​ ​share​ ​their​ ​favorite​ ​movies.

## Running instance 🦈
Click [here](http://164.92.162.226:8000/movies) to access a running instance of the app!

The project has been deployed with a droplet at [DigitalOcean](https://www.digitalocean.com/).
At the moment of this writting they offer free 200$ of credit for a duration of 2 months. 

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
**Warning!** The field values are examples. You should use different values for safety purposes.

Then, to run the app just type on the cmd

`docker compose up -d`

## Access
Access the app on: https://localhost:8000/

The API documentation can be found on https://localhost:8000/docs or https://localhost:8000/redoc.

## Testing
Run the unit tests with 

`$ docker exec -it movierama sh -c "pytest"`

## Homepage Screenshots

![image](https://github.com/Tzal3x/movierama/assets/33265837/516fa29f-04fd-4d5e-b3b0-3e42fc9f23ab)

![image](https://github.com/Tzal3x/movierama/assets/33265837/4c5d9bca-9e2d-480b-ae3a-d6bed855024f)
