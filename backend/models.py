# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import List


class SearchHit(BaseModel):
    id: str
    name: str
    content: str


class SearchResponse(BaseModel):
    size: int
    result: List[SearchHit]
