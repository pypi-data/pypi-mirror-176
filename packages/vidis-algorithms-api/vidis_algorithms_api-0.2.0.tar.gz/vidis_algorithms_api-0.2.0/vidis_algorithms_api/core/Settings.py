import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA_PATH = os.environ.get('DATA_PATH', r'E:\Projects\hyperspectral-project2\python_module\database\data\data')
    MARIA_DB_ADDRESS = os.environ.get('MARIA_DB_ADDRESS', 'mariadb+mariadbconnector://root:qwerty322@db:3306/main')
    AMQP_ADDRESS = os.environ.get('AMQP_ADDRESS', 'amqp://guest:guest@127.0.0.1:5672')

    TASK_DATE_FORMAT = '%d/%m/%y %H:%M:%S'
    DATA_FOLDER_NAME = '%d_%m_%Y%H_%M_%S_%f'

    CUSTOM_LAYER_FOLDER = 'custom_algorithm'
