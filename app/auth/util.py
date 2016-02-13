from itsdangerous import URLSafeTimedSerializer
import os

env_config = os.getenv('FLASK_CONFIG') or 'default'
ts = URLSafeTimedSerializer(env_config)  # TODO: Change this to read from app config
