from os import environ
from dotenv import load_dotenv


def create_db_url() -> str:
    load_dotenv()
    db_url = "%s://%s:%s@%s/%s" % (
        environ["DB_SERVICE"],
        environ["DB_USERNAME"],
        environ["DB_PASSWORD"],
        environ["DB_HOST"],
        environ["DB_NAME"],
    )
    return db_url


def get_security_configs() -> dict[str]:
    load_dotenv()
    return {
        "TOKEN_CREATION_SECRET_KEY": environ["TOKEN_CREATION_SECRET_KEY"],
        "HASH_ALGORITHM": environ["HASH_ALGORITHM"],
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(
            environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
        ),
    }
