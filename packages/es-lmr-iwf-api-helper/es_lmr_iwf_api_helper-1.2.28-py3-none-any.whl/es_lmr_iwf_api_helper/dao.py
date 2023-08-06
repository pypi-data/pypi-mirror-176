from datetime import datetime


class CheckConnectivity:
    def check_connectivity(self):
        pass


class CrudDao(CheckConnectivity):
    def find_paged(self, page: int, size: int) -> dict:
        pass

    def find_one(self, element_id: str) -> dict:
        pass

    def find_audit(self, from_date: datetime) -> dict:
        pass

    def delete(self, element_id: str) -> dict:
        pass

    def create(self, data: dict) -> dict:
        pass

    def update(self, element_id: str, data: dict) -> dict:
        pass


class OneToOneRelationDao(CrudDao):
    def find_audit(self, from_date: datetime):
        pass

    def find_paged(self, page: int, size: int) -> dict:
        pass

    def find_one(self, element_id: str):
        pass

    def update(self, element_id: str, data: dict):
        pass
