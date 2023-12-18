from src.adapters.repository.ctr_prediction_repository import CTRPredictionAlgorithm, PredicitonType, RandomPrediction
from src.adapters.repository.redis_point_respository import RedisPointRepository
from src.adapters.repository.sql_rec_repository import SQLRecRepository

from src.domain.models.dto_rec import RecResponse, UserInfo, RecInfo
from typing import List
from dataclasses import asdict



class RecService:
    def __init__(self, rec_allocation: SQLRecRepository, redis_interface: RedisPointRepository):
        self.rec_allocation = rec_allocation
        self.redis_interface = redis_interface

    def get_recs_for_user(self, user: UserInfo) -> List[RecInfo]:
        rec = self.rec_allocation.allocate_recs(user)
        recs = RandomPrediction().predict_ctr(user, rec)
        if recs:
            self.redis_interface.initialize_user_rec(user, recs)
            return recs
        return False
    
    def get_recs_for_user_with_ctr_prediction(self, user: UserInfo) -> List[RecInfo]:
        recs = self.rec_allocation.allocate_recs(user)

        # assign algorithm type by userID % 2
        algorithm = PredicitonType(user.user_id % len(PredicitonType))
        print("here")
        return CTRPredictionAlgorithm.run(algorithm, user, recs)

    def response_recs(self, recs_info: List[RecInfo]) -> List[RecResponse]:
        """
        Process a list of Rec entities and generate Rec Response

        Returns:
            List[RecResponse]: A list of RecResponse entities generated from the recs.
        """
        return [asdict(RecResponse(rec.id, rec.name, rec.image_url, rec.landing_url)) for rec in recs_info]
