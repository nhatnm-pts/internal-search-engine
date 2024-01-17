# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from elasticsearch import Elasticsearch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from os.path import join
import psycopg2
import psycopg2.extras

from constance import (
    ELASTIC_PASSWORD,
    ELASTIC_USERNAME,
    FILE_EXTENSION_ALLOWED,
    FILE_PATH,
    INTERVAL,
    PSQL_DBNAME,
    PSQL_PASSWD,
    PSQL_TABLE_NAME,
    PSQL_USER,
)
from models import SearchHit, SearchResponse

logger = logging.getLogger("uvicorn.error")


def indexing():
    indexing_path()
    indexing_postgres()


def indexing_postgres():
    if not all([PSQL_USER, PSQL_DBNAME, PSQL_PASSWD, PSQL_TABLE_NAME]):
        logger.info(
            "PSQL_TABLE_NAME, PSQL_USER, PSQL_DBNAME, PSQL_PASSWD environment"
            " variables are not set, skipped!"
        )
        return
    logger.info("Start indexing PostgreSQL database")
    try:
        conn = psycopg2.connect(
            host="postgres",
            port=5432,
            user=PSQL_USER,
            password=PSQL_PASSWD,
            dbname=PSQL_DBNAME,
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(
            f"""
                SELECT
                    booktitle,
                    bookchunkid,
                    bookchunktext
                FROM
                    {PSQL_TABLE_NAME};
            """,
        )
        result = cursor.fetchall()
        row_ids = []
        for row in result:
            row_id = f"{row.get('booktitle')}_{row.get('bookchunkid')}"
            es.index(
                index="postgres",
                id=row_id,
                body={
                    "book": row.get("booktitle"),
                    "content": row.get("bookchunktext"),
                },
            )
            row_ids.append(row_id)
        logger.info("Start removing unused indexes!")
        query = {"query": {"bool": {"must_not": [{"ids": {"values": row_ids}}]}}}
        es.delete_by_query("postgres", body=query)
        conn.close()
    except Exception as e:
        logger.error(f"PostgreSQL synchronization failed, error: {e.args}")


def indexing_path():
    if not FILE_PATH:
        logger.info("FILE_PATH environment variable is not set, skipped!")
        return
    logger.info(f"Start indexing filestore at: {FILE_PATH}")
    file_ids = []
    for root, dirs, files in os.walk(FILE_PATH):
        for file in files:
            if file.split(".")[-1] not in FILE_EXTENSION_ALLOWED:
                continue
            full_file_path = join(root, file)
            with open(file=full_file_path, mode="r") as f:
                data = f.read()
                if not data:
                    continue
                file_ids.append(full_file_path)
                es.index(
                    index="filestore",
                    id=full_file_path,
                    body={"file_name": file, "content": data},
                )
    logger.info("Start removing unused indexes!")
    query = {"query": {"bool": {"must_not": [{"ids": {"values": file_ids}}]}}}
    es.delete_by_query("filestore", body=query)


@asynccontextmanager
async def lifespan(_: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        name="Indexing Cron",
        func=indexing,
        trigger="interval",
        seconds=INTERVAL,
    )
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


es = Elasticsearch(
    hosts="http://elasticsearch:9200/",
    http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD),
    verify_certs=False,
)
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search/")
async def search(query: str) -> SearchResponse:
    es_result = es.search(
        index="_all",
        body={
            "query": {
                "query_string": {
                    "query": query,
                    "fields": ["content"],
                }
            },
            "size": 100,
            "from": 0,
            "sort": ["_score"],
        },
    )
    total_hits = es_result["hits"]["total"]["value"]
    res = []
    for doc in es_result["hits"]["hits"]:
        name = ""
        if doc["_index"] == "filestore":
            name = doc["_source"]["file_name"]
        elif doc["_index"] == "postgres":
            name = doc["_source"]["book"]
        res.append(
            SearchHit(
                id=doc["_id"],
                name=name,
                content=doc["_source"]["content"].replace("\n", "<br />"),
            )
        )
    return SearchResponse(size=total_hits if total_hits < 100 else 100, result=res)
