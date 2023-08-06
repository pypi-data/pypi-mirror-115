from uuid import UUID
from antidote import service, Provide, inject
from pymongo.collection import Collection
from AsteriskRealtimeData.domain.entity import Entity

from AsteriskRealtimeData.infrastructure.repositories.mongo.mongo_connection import (
    MongoConnection,
)
from AsteriskRealtimeData.infrastructure.repositories.repository_interface import (
    Repository,
)


@service(singleton=True)
class MongoRespository(Repository):
    @inject
    def __init__(self, connection: Provide[MongoConnection]) -> None:
        self.connection = connection

    def save(
        self, entity: Entity, identify_field: dict,
    ):
        table = self._get_table()
        return table.replace_one(identify_field, entity.as_dict(), upsert=True,)

    def list(self):
        table = self._get_table()
        return table.find({})

    def get_by_id(self, id: UUID):
        table = self._get_table()
        return table.find_one({"id": id})

    def delete_by_id(self, id: UUID):
        table = self._get_table()
        return table.delete_one({"id": id})

    def get_by_criteria(self, search_criteria: dict):
        table = self._get_table()
        return table.find_one(search_criteria)

    def delete_by_criteria(self, search_criteria: dict):
        table = self._get_table()
        return table.delete_one(search_criteria)

    def _get_table(self) -> Collection:
        return self.connection.get_connection()[self.get_table_name()]

