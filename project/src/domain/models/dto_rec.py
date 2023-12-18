"""
Author: Su Il Lee
Version: 1.0.0
Date: 11.29.23

Hexagonal Architecture DTO Entities

This module contains as a data transfer object from domain.entities to different parts
of the architecture. 

It prevents exposure of business entities.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserInfo:
    user_id: int
    gender: str
    country: str

@dataclass
class RecInfo:
    id: int
    name: str
    image_url: str
    landing_url: str
    weight: int
    target_country: str
    target_gender: str
    point: int
    date: Optional[datetime] = None


@dataclass
class RecResponse:
    id: int
    name: str
    image_url: str
    landing_url: str


