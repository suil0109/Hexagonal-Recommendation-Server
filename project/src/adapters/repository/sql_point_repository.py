from src.infrastructure.database.models import RecModel, SessionLocal, PointHistoryDB, PointUserDB

from src.domain.models.dto_point import Point, PointInfo, PointUser
from src.domain.models.configuration import Transaction, DOES_NOT_EXITS
from src.domain.models.entities import Rec, User
from src.domain.models.dto_rec import RecInfo

from src.domain.ports.point_port import PointPort

from datetime import datetime, timedelta
from fastapi import HTTPException
from typing import List

class SQLPointRepository(PointPort):
    def __init__(self, sql_client=None):
        if sql_client is None:
            self.db = SessionLocal()
        else:
            self.db = sql_client

    def modify_point(self, point: Point) -> bool:
        query = self.db.query(RecModel).filter(RecModel.id == point.rec_id).one_or_none()

        if query:
            query.point = point.amount
            self.db.commit()
            return True
        else:
            return False

    def deposit_point(self, user_info: User, point_info: List[Point]) -> bool:
        """Deposit point for a user."""
        pass

    def deduct_point(self, point_info: PointInfo) -> bool:
        """Deduct an amount from the user's point balance."""
        table = self.db.query(PointUserDB)
        user_balance = table.filter(PointUserDB.id == point_info.user_id).one_or_none()

        if user_balance:
            if int(user_balance.balance) < point_info.point:
                return False
            balance = self.update_balance(point_info)
            self.update_history(balance, point_info)
            return True



    def allocate_recs(self, user: List[User]) -> List[RecInfo]:
        return self.find_by_criteria(user)
    
    def find_by_criteria(self, user: List[User]) -> List[RecInfo]:
        query = self.db.query(RecModel)

        if user.country:
            query = query.filter(RecModel.target_country == user.country)
        if user.gender:
            query = query.filter(RecModel.target_gender == user.gender)
        query_result = query.all()

        recs = []
        # TODO: Improve below.
        for rec in query_result:
            rec_dict = rec.__dict__
            if '_sa_instance_state' in rec_dict:
                del rec_dict['_sa_instance_state']
            if 'db' in rec_dict:
                del rec_dict['db']
            recs.append(Rec(**rec_dict))

        return recs

    def update_db_from_queue(self, task: PointInfo) -> bool:
        balance = self.update_balance(task)
        if balance >=0:
            return self.update_history(balance, task)
        return False
                
    def update_balance(self, task: PointInfo) -> int:
        current_user_balance = self.db.query(PointUserDB).filter(PointUserDB.id == task.user_id).one_or_none()

        if current_user_balance:
            # Update the balance
            new_balance = int(current_user_balance.balance) - task.point
            if task.transaction == Transaction.DEPOSIT.value:
                new_balance = int(current_user_balance.balance) + task.point
            current_user_balance.balance = new_balance
            self.db.commit()
            return new_balance
        else:

            new_user = PointUserDB(id=task.user_id, balance=task.point)
            self.db.add(new_user)
            self.db.commit()
            return task.point
        
    def update_history(self, balance, task: PointInfo) -> list:

        new_point_history = PointHistoryDB(
                    user_id=task.user_id,
                    rec_id=task.rec_id,
                    transaction=task.transaction,
                    point=task.point,
                    remaining_balance = balance,
                    timestamp=task.timestamp,
                    initialized = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        )
        self.db.add(new_point_history)
        self.db.commit()

    def get_history(self, user_info: User) -> str:
        
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        query = (
            self.db.query(PointHistoryDB)
            .filter(PointHistoryDB.user_id == user_info.user_id)
            .filter(PointHistoryDB.timestamp >= seven_days_ago)
            .order_by(PointHistoryDB.timestamp.desc())
        )
        
        transactions_data = []
        if query:
            transactions = query.all()

            transactions_data = [
                {
                    "Rec id": transaction.rec_id,
                    "Transaction": transaction.transaction,
                    "Point": transaction.point,
                    "Remaining Balance": transaction.remaining_balance,
                    "Date": transaction.timestamp.isoformat()  # Format the datetime to ISO 8601
                }
                for transaction in transactions
            ]
        
        return transactions_data
    
    def get_balance(self, user_info: User) -> PointUser:
        query = (
            self.db.query(PointUserDB)
            .filter(PointUserDB.id == user_info.user_id)
        ).one_or_none()
        if query:
            return PointUser(query.id, query.balance, query.timestamp)


        raise HTTPException(status_code=404, detail="User balance not found")
    
    def get_rec_point_amount(self, rec_id: int) -> int:
        query = (
            self.db.query(RecModel)
            .filter(RecModel.id == rec_id)
        ).one_or_none()

        if query:
            return query.point
        return DOES_NOT_EXITS

