# -*- coding: utf-8 -*-
"""
Environment variables or constances
"""
import os
from os.path import dirname, join, realpath

get_env_param = os.environ.get

INTERVAL = 1 * 60 * 60
if get_env_param("INTERVAL"):
    try:
        INTERVAL = int(os.environ["INTERVAL"])
    except ValueError:
        pass

FILE_PATH = get_env_param("FILE_PATH", "")
if not FILE_PATH:
    FILE_PATH = join(dirname(realpath(__file__)), "filestore")

FILE_EXTENSION_ALLOWED: list = []
env_file_extension = get_env_param("FILE_EXTENSION_ALLOWED")
if not env_file_extension:
    FILE_EXTENSION_ALLOWED = ["txt", "csv", "json"]
else:
    FILE_EXTENSION_ALLOWED = env_file_extension.split(",")

PSQL_DBNAME = get_env_param("PSQL_DBNAME")

PSQL_USER = get_env_param("PSQL_USER")

PSQL_PASSWD = get_env_param("PSQL_PASSWD")

PSQL_TABLE_NAME = get_env_param("PSQL_TABLE_NAME")

ELASTIC_USERNAME = get_env_param("ELASTIC_USERNAME")

ELASTIC_PASSWORD = get_env_param("ELASTIC_PASSWORD")
