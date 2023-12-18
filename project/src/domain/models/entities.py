"""
Author: Su Il Lee
Version: 1.0.0
Date: 11.29.23

Hexagonal Architecture Domain Entities

This module contains the domain entities for a recommendation server. 

The `Rec` dataclass represents an advertisement entity with attributes that describe its properties
and the target audience. 
The `User` dataclass manage and serve as a preference and identity properties.

"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Rec:
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
class User:
    user_id: int
    gender: str
    country: str
    balance: Optional[int]
    rate_limit: Optional[int]


# @dataclass
# class Point:
#     rec_id: int
#     amount: int
#     date: Optional[datetime] = field(default=datetime.now())

# @dataclass
# class RedisPoint:
#     user_id: str
#     rate_limit: int
#     point_remaining: int
#     recs_served: List[int] = field(default_factory=list)

# @dataclass
# class PointUser:
#     user_id: int
#     point: int
#     date: Optional[datetime] = field(default=datetime.now())

# @dataclass
# class PointDepositBase:
#     rec_id: int
#     user_id: int

# @dataclass
# class PointDeductBase:
#     user_id: int
#     point: int

# @dataclass
# class PointInfo:
#     rec_id: int
#     user_id: int
#     transaction: str
#     point: int
#     timestamp: datetime = field(default_factory=datetime.now)




# @dataclass
# class PointDepositInfo(PointDepositBase):
#     # rec_id: int
#     # user_id: int
#     transaction: str
#     point: int
#     timestamp: datetime = field(default_factory=datetime.now)

# @dataclass
# class PointDeductInfo(PointDeductBase):
#     # user_id: int
#     # point: int
#     transaction: str
#     timestamp: datetime = field(default_factory=datetime.now)

# @dataclass
# class PointBase:
#     rec_id: int
#     user_id: int
#     point: int
