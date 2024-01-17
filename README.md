# INTERNAL SEARCH ENGINE

## Usage:

- This is internal search engine.

- Using [Elasticsearch](https://www.elastic.co/) for file indexing

- Using [Kibana](https://www.elastic.co/kibana) for monitoring

- Using Python [FastAPI](https://fastapi.tiangolo.com/) for backend server & app scheduler

- Using Javascript [Vue](https://vuejs.org/) for frontend server

## How to set it up?

Building backend server image from Dockerfile

```bash
$ docker build . -t internal_search_engine_back_end --progress plain -f ./backend.Dockerfile
```

Building frontend server image from Dockerfile

```bash
$ docker build . -t internal_search_engine_front_end --progress plain -f ./frontend.Dockerfile
```

Running project using docker

```bash
$ docker compose up --build
```
