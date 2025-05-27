import mysql.connector

def get_db(config):
    return mysql.connector.connect(**config)