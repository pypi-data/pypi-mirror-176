from __future__ import annotations

import logging
from abc import abstractmethod
from attrs import define, field
from datetime import datetime
from typing import Sequence, Optional

from resotocore.db.async_arangodb import AsyncArangoDB
from resotocore.db.entitydb import EntityDb, ArangoEntityDb
from resotocore.ids import TaskId, TaskDescriptorId
from resotocore.message_bus import Message
from resotocore.model.typed_model import to_js
from resotocore.task.task_description import RunningTask
from resotocore.types import Json
from resotocore.util import utc

log = logging.getLogger(__name__)


@define(order=True, hash=True, frozen=True)
class RunningTaskData:
    # id of the related task
    id: TaskId
    # id of the related task descriptor
    task_descriptor_id: TaskDescriptorId
    # name of the related task descriptor
    task_descriptor_name: str
    # all messages that have been received by this task
    received_messages: Sequence[Message] = field(factory=list)
    # the name of the current state inside the finite state machine
    current_state_name: str = field(default="start")
    # the state of the current state exported as json
    current_state_snapshot: Json = field(factory=dict)
    # the timestamp when the step has been started
    task_started_at: datetime = field(factory=utc)
    # the timestamp when the step has been started
    step_started_at: datetime = field(factory=utc)

    @staticmethod
    def data(wi: RunningTask) -> RunningTaskData:
        return RunningTaskData(
            wi.id,
            wi.descriptor.id,
            wi.descriptor.name,
            wi.received_messages,
            wi.current_state.name,
            wi.current_state.export_state(),
            wi.task_started_at,
            wi.step_started_at,
        )


class RunningTaskDb(EntityDb[str, RunningTaskData]):
    @abstractmethod
    async def update_state(self, wi: RunningTask, message: Optional[Message]) -> None:
        pass

    @abstractmethod
    async def insert(self, task: RunningTask) -> RunningTaskData:
        pass


class ArangoRunningTaskDb(ArangoEntityDb[str, RunningTaskData], RunningTaskDb):
    def __init__(self, db: AsyncArangoDB, collection: str):
        super().__init__(db, collection, RunningTaskData, lambda k: k.id)

    async def update_state(self, wi: RunningTask, message: Optional[Message]) -> None:
        bind = {
            "id": f"{self.collection_name}/{wi.id}",
            "current_state_name": wi.current_state.name,
            "current_state_snapshot": wi.current_state.export_state(),
        }
        if message:
            bind["message"] = to_js(message)
            aql = self.__update_state_with_message()
        else:
            aql = self.__update_state()

        await self.db.aql(aql, bind_vars=bind)

    async def insert(self, task: RunningTask) -> RunningTaskData:
        return await self.update(RunningTaskData.data(task))

    def __update_state(self) -> str:
        return f"""
        LET doc = Document(@id)
        UPDATE doc WITH {{
            current_state_name: @current_state_name,
            current_state_snapshot: @current_state_snapshot
        }} IN {self.collection_name}
        """

    def __update_state_with_message(self) -> str:
        return f"""
        LET doc = Document(@id)
        UPDATE doc WITH {{
            current_state_name: @current_state_name,
            current_state_snapshot: @current_state_snapshot,
            received_messages: APPEND(doc.received_messages, @message)
        }} IN {self.collection_name}
        """


def running_task_db(db: AsyncArangoDB, collection: str) -> RunningTaskDb:
    return ArangoRunningTaskDb(db, collection)
