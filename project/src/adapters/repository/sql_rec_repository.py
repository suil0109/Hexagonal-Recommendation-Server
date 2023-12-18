from src.infrastructure.database.models import RecModel, SessionLocal

from src.domain.ports.rec_port import RecManagementPort
from src.domain.models.dto_rec import UserInfo, RecInfo
from src.domain.models.entities import Rec

from typing import List

class SQLRecRepository(RecManagementPort):
    def __init__(self, sql_client=None):
        if sql_client is None:
            self.db = SessionLocal()
        else:
            self.db = sql_client

    def allocate_recs(self, user: UserInfo) -> List[RecInfo]:
        return self.find_by_criteria(user)
    
    def find_by_criteria(self, user: UserInfo) -> List[RecInfo]:

        query = self.db.query(RecModel)

        if user.country:
            query = query.filter(RecModel.target_country == user.country)
        if user.gender:
            query = query.filter(RecModel.target_gender == user.gender)
        query_result = query.all()
        recs = []
        
        # TODO: Improve below
        for rec in query_result:
            rec_dict = rec.__dict__
            if '_sa_instance_state' in rec_dict:
                del rec_dict['_sa_instance_state']
            if 'db' in rec_dict:
                del rec_dict['db']
            recs.append(Rec(**rec_dict))
        return recs
