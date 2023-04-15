from typing import Optional
from .base import BaseTypeFilter


class BooleanFilter(BaseTypeFilter):
    value: Optional[bool] = None
