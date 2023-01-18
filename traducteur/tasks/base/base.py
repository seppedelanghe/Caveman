import marshal, types

from typing import Optional, Callable, Union

from .status import TaskStatus
from .lifetime import TaskLifetime
from ...models.base import BaseModel
from ...exceptions.tasks import TaskException

class BaseTask(BaseModel):
    action: Union[Callable, str]
    id: int = 0
    status: TaskStatus = TaskStatus.NONE
    lifetime: TaskLifetime = TaskLifetime()
    tin: Optional[dict] = None
    tout: Optional[dict] = None

    def queue(self, **kwargs):
        self.tin = kwargs
        self.serialize()
        self.status = TaskStatus.QUEUED

    def digest(self):
        try:
            self.lifetime.start()
            self.status = TaskStatus.RUNNING
            self.deserialize()
            self.tout = self.action(**self.tin)
            self.serialize()
            self.status = TaskStatus.SUCCEEDED
        except Exception as e:
            self.lifetime.error = e
            self.status = TaskStatus.FAILED
        finally:
            self.lifetime.end()


    def serialize(self):
        if isinstance(self.action, str):
            raise TaskException('Task action is already serialized!')
        self.action = marshal.dumps(self.action.__code__)

    def deserialize(self):
        if isinstance(self.action, Callable):
            raise TaskException('Task action is already deserialized!')
        self.action = types.FunctionType(marshal.loads(self.action), globals(), f"task_{self.id}")