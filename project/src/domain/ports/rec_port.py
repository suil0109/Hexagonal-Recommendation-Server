from src.domain.models.dto_rec import UserInfo, RecInfo, RecResponse
from src.domain.models.entities import Rec

from typing import List
from typing import Protocol

# from abc import ABC, abstractmethod

class RecManagementPort(Protocol):
    # @abstractmethod
    def allocate_recs(self, user: UserInfo) -> List[RecInfo]:
        """Allocate Recs for Users"""
        ...

    # @abstractmethod
    def response_recs(self, recs: Rec) -> List[RecResponse]:
        """Return Recs for Users"""
        ...

    # @abstractmethod
    def predict_ctr(self, user: UserInfo, rec: List[RecInfo]) -> List[RecInfo]:
        """Predict Recs for Users"""
        ...
