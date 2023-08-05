import os

import pymysql

from .config import global_config
from .constants import TRAIN_STATUS_COMPLETED, TRAIN_STATUS_ERROR, TRAIN_STATUS_TRAINING, TRAIN_STATUS_UNKNOWN

mysql_db_name = os.environ.get('ML_CLIENT_MLP_DB_NAME', 'ml_platform')


class MysqlAccessor:
    client = None

    # @staticmethod
    # def init_client():
    #     mysql_client = pymysql.connect(host=global_config.mysql_host, port=global_config.mysql_port,
    #                                    user=global_config.mysql_user, passwd=global_config.mysql_password,
    #                                    db=mysql_db_name)
    #     MysqlAccessor.client = mysql_client

    @staticmethod
    def get_client() -> pymysql.connections.Connection:
        return pymysql.connect(host=global_config.mysql_host, port=global_config.mysql_port,
                               user=global_config.mysql_user, passwd=global_config.mysql_password,
                               db=mysql_db_name)

    @staticmethod
    def check_load_update_time(algorithm):
        cursor = MysqlAccessor.get_client().cursor()
        cursor.execute("select load_time from load_record where algorithm = '{}'".format(algorithm))
        load_time = list(cursor.fetchall())
        return load_time[0] if load_time else None

    @staticmethod
    def get_load_models(algorithm):
        cursor = MysqlAccessor.get_client().cursor()
        cursor.execute("select model_id, path from model where algorithm = '{}' and loaded = 1".format(algorithm))
        models = list(cursor.fetchall())
        return {model_id: model_path for model_id, model_path in models}

    @staticmethod
    def get_model_train_status(model_id):
        cursor = MysqlAccessor.get_client().cursor()
        cursor.execute("select status from model where model_id = '{}'".format(model_id))
        status = list(cursor.fetchall())
        if status:
            status = status[0]
            if status == 'active' or status == 'inactive':
                return TRAIN_STATUS_COMPLETED
            if status == 'error':
                return TRAIN_STATUS_ERROR
            return TRAIN_STATUS_TRAINING
        return TRAIN_STATUS_UNKNOWN

    @staticmethod
    def update_model_train_status(model_id, status):
        db = MysqlAccessor.get_client()
        cursor = db.cursor()
        cursor.execute(
            "update model set status = '{}' where model_id = '{}' and status = 'training'".format(status, model_id))
        db.commit()
