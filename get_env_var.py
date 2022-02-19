import environ

env = environ.Env(

    DEBUG=(bool, False)
)
environ.Env.read_env()

print(
    env('SECRET_KEY'),
    env('DEBUG'),
    env('ALLOWED_HOSTS').split(','),
    env('DB_NAME'),
    env('DB_ENGINE'),
    env('DB_USER'),
    env('DB_PASSWORD'),
    env('DB_HOST'),
    env('DB_PORT')
)