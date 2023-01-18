from typing import Optional

from ..base import BaseTask

class ChainBuilder:
    def __init__(self):
        self.tasks = {}

    def add(self, task: BaseTask):
        pass

    def remove(self, task: BaseTask):
        pass

    def build(self):
        pass

    def run(self, task_input: Optional[dict] = None) -> dict:
        pass
