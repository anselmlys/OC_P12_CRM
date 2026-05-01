import os
import sentry_sdk

from dotenv import load_dotenv


def init_sentry():
    '''Initialize Sentry if a DSN is configured.'''
    load_dotenv()

    sentry_dsn = os.getenv('SENTRY_DSN')
    app_env = os.getenv('APP_ENV', 'development')

    if not sentry_dsn:
        return

    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=app_env,
    )
