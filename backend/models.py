# -*- coding: utf-8 -*-
"""
Backend models
"""
from typing import List

from pydantic import BaseModel


class SearchHit(BaseModel):
    """
    Response model
    """

    id: str
    name: str
    content: str


class SearchResponse(BaseModel):
    """
    Get request model
    """

    size: int
    result: List[SearchHit]
