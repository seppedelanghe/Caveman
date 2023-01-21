import pickle, json
from typing import Optional

from ..base import BaseTask
from ...models.nosql import BaseRedisModel


class RedisTask(BaseTask, BaseRedisModel):
    channel: str

    def queue(self, **kwargs):
        r = self.redis_instance()
        if self.has_parent:
            parent: BaseTask = r.get(self.parent)
            super().queue(**parent.tout)
        else:
            super().queue(**kwargs)

        task: bytes = pickle.dumps(self)
        r.set(self.id, task)

        if self.instant:
            self._publish()

    def digest(self):
        super().digest()

        # update task status
        task: bytes = pickle.dumps(self)
        r = self.redis_instance()
        r.set(self.id, task)

        if self.has_children:
            # exec children
            for child_id in self.children:
                self._publish(child_id)
        
    def _publish(self, uuid: Optional[str] = None):
        r = self.redis_instance()
        message = json.dumps({
            'id': self.id if uuid is None else uuid
        })
        r.publish(self.channel, message)