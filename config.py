
from dotenv import load_dotenv

from decouple import config

load_dotenv()

connection_param = {

    "dev": {
        "DB_DATABASE_NAME": config('DB_DATABASE_NAME'),
        'DB_HOST': config('DB_HOST'),
        'DB_USER': config('DB_USERNAME'),
        'DB_PASS': config('DB_PASSWORD'),
    }

}
