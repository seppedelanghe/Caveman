import pickle, json

from ..base import BaseTask
from ...models.nosql import BaseRedisModel


class RedisTask(BaseTask, BaseRedisModel):
    channel: str

    def queue(self, **kwargs):
        super().queue(**kwargs)

        message = json.dumps({
            'id': self.id
        })
        task: bytes = pickle.dumps(self)

        r = self.redis_instance()
        r.set(self.id, task)
        r.publish(self.channel, message)

    def digest(self):
        super().digest()

        task: bytes = pickle.dumps(self)

        r = self.redis_instance()
        r.set(self.id, task)