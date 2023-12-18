"""
Author: Su Il Lee
Version: 1.0.0
Date: 11.29.23

Hexagonal Architecture DTO Entities

This module contains as a data transfer object from domain.entities to different parts
of the architecture. 

It prevents exposure of business entities.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime



@dataclass
class PointInfo:
    rec_id: int
    user_id: int
    transaction: str
    point: int
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Point:
    rec_id: int
    amount: int
    date: Optional[datetime] = field(default=datetime.now())

@dataclass
class PointUser:
    user_id: int
    point: int
    date: Optional[datetime] = field(default=datetime.now())

@dataclass
class PointDepositBase:
    rec_id: int
    user_id: int

@dataclass
class PointDeductBase:
    user_id: int
    point: int

@dataclass
class RedisPoint:
    user_id: str
    rate_limit: int
    point_remaining: int
    recs_served: List[int] = field(default_factory=list)