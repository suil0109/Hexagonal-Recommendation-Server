from src.domain.ports.rec_port import RecManagementPort
from src.infrastructure.configuration.config import global_config
from src.domain.models.configuration import StatusCode
from src.domain.models.dto_rec import UserInfo, RecInfo

from typing import List
from enum import Enum
import requests
import random

# TEMP = [Rec(id=1, name='campaign name 1', image_url='https://image.google.com/image_1.jpg', landing_url='https://landing.google.com/landing_1', weight=2300, target_country='KR', target_gender='M', point=2.0), Rec(id=2, name='campaign name 2', image_url='https://image.google.com/image_2.jpg', landing_url='https://landing.google.com/landing_2', weight=5500, target_country='KR', target_gender='M', point=7.0), Rec(id=3, name='campaign name 3', image_url='https://image.google.com/image_3.jpg', landing_url='https://landing.google.com/landing_3', weight=6400, target_country='KR', target_gender='M', point=5.0)]
# USER = User(1,'M',"KR")

class PredicitonType(Enum):
    RANDOM = 0
    WEIGHTED = 1

class RandomPrediction(RecManagementPort):
    def predict_ctr(self, user: UserInfo, recs: List[RecInfo]) -> List[RecInfo]:
        random.shuffle(recs)
        return recs[:min(global_config.MAX_RECS, len(recs))]
    
class WeightPrediction(RecManagementPort):

    def predict_ctr(self, user: UserInfo, recs: List[RecInfo]) -> List[RecInfo]:

        return self.random_probability_prediction(user, recs)
    
    @staticmethod
    def random_probability_prediction(user: UserInfo, recs: List[RecInfo]) ->List[RecInfo]:

        total_weight = sum(rec.weight for rec in recs)
        probabilities = [rec.weight / total_weight for rec in recs]
        return random.choices(recs, weights=probabilities, k=3)[:min(global_config.MAX_RECS, len(recs))]


class CTRPredictionAlgorithm:
    @staticmethod
    def run(strategy_type: PredicitonType, user: UserInfo, recs: List[RecInfo]) -> RecManagementPort:
        if strategy_type == PredicitonType.RANDOM:
            return RandomPrediction().predict_ctr(user, recs)
        
        elif strategy_type == PredicitonType.WEIGHTED:
            return WeightPrediction().predict_ctr(user, recs)
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")