# 🎥 MovieRama

MovieRama is a social sharing platform where users can share and discover their favorite movies. Users can engage with the community by viewing shared movies, contributing their own favorites, and discussing cinematic gems.

## 💾 Installation

### Environment Setup

Firstly, create a `.env` file in the project's root directory (for example, in `/movierama/.env`) with the necessary environment variables. Replace placeholder values with your own secure credentials:

```env
DB_SERVICE=postgresql
DB_USERNAME=postgres
DB_PASSWORD=<YOUR_STRONG_PASSWORD_HERE>
DB_NAME=movierama
DB_PORT=5432
DB_HOST=postgres:5432
HASH_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
TOKEN_CREATION_SECRET_KEY=<YOUR_TOKEN_CREATION_KEY_HERE>
```

⚠️ **Warning:** Do not use the example values provided above in a production environment. Always choose secure and unique values for credentials.

### Running the Application

To launch MovieRama, open your command line interface (CLI) and run the following Docker command:

```sh
docker-compose up -d
```

This command will start the application in detached mode.

## 🌐 Accessing the Application

After starting the application, you can access MovieRama at the following URL:

- **Web App:** [https://localhost:8000/](https://localhost:8000/)

For API documentation, visit one of these URLs:

- **Swagger UI Docs:** [https://localhost:8000/docs](https://localhost:8000/docs)
- **ReDoc Docs:** [https://localhost:8000/redoc](https://localhost:8000/redoc)

## 🧪 Testing

To execute the unit tests, run the following command:

```sh
docker exec -it movierama sh -c "pytest"
```

## 📸 Screenshots

Here are some screenshots of MovieRama in action:

![Screenshot 1](https://github.com/Tzal3x/movierama/assets/screenshot_1.png)
![Screenshot 2](https://github.com/Tzal3x/movierama/assets/screenshot_2.png)

_Note: Please make sure the URLs to the screenshots are valid and publicly accessible._

## ⌨️ Local Development

If you prefer to run the application locally, ensure you have Python 3.8 or higher installed.

### Setup a Virtual Environment

Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Unix-based systems
venv\Scripts\activate     # On Windows
```

### Install Dependencies

Install the required Python packages:

```sh
pip install -r requirements.txt
```

### Start the Database

Initialize the PostgreSQL database using Docker:

```sh
docker-compose up -d postgres
```

### Apply Database Migrations

Run Alembic to apply database migrations:

```sh
alembic upgrade head
```

### Launch the Application

Start the ASGI server with:

```sh
uvicorn app.main:app --reload
```

The `--reload` flag enables hot reloading for development purposes.
