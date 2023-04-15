from typing import Sequence, Any, Optional, Union

from sqlalchemy import Column
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ..filters.base import BaseFilter
from ..filters.types import StringFilter, DatetimeFilter, NumberFilter, ExistsFilter, BooleanFilter
from ..filters.types.base import BaseTypeFilter


class QueryBuilderException(Exception):
    pass


class SQLQueryBuilder:
    def __init__(self, session: Session, cls):
        self.session = session
        self.cls = cls
        self.joined = []

        self.query = self.session.query(self.cls)

    def _add_string(self, str_filter: StringFilter, col: Column):
        if str_filter.exact:
            self.query = self.query.filter(col == str_filter.exact)
            return  # no more need for other filters

        if str_filter.includes:
            self.query = self.query.filter(col.like(f"%{str_filter.includes}%"))

        if str_filter.begin:
            self.query = self.query.filter(col.like(f"{str_filter.begin}%"))

        if str_filter.end:
            self.query = self.query.filter(col.like(f"%{str_filter.end}"))

    def _add_datetime(self, date_filter: DatetimeFilter, col: Column):
        if date_filter.start:
            self.query = self.query.filter(col > date_filter.start)

        if date_filter.end:
            self.query = self.query.filter(col < date_filter.end)

    def _add_number(self, number_filter: NumberFilter, col: Column):
        if number_filter.equal:
            self.query = self.query.filter(col == number_filter.equal)
            return  # no more need for other filters

        if number_filter.gt:
            self.query = self.query.filter(col > number_filter.gt)

        if number_filter.lt:
            self.query = self.query.filter(col < number_filter.lt)

    def _add_exists(self, exists_filter: ExistsFilter, col: Column):
        if isinstance(exists_filter.exists, bool):
            self.query = self.query.filter(col != None) if exists_filter.exists else self.query.filter(col == None)
            self.query = self.query.filter(col != "") if exists_filter.exists else self.query.filter(col == "")

    def __add_bool(self, boolean_filter: BooleanFilter, col: Column):
        if isinstance(boolean_filter.value, bool):
            self.query = self.query.filter(col == boolean_filter.value)

    def add(self, filter_cls: BaseTypeFilter, col: str, join_cls=None):
        try:
            if join_cls is not None:
                prop: Column = getattr(join_cls, col)
                if not isinstance(prop, InstrumentedAttribute):
                    raise Exception()
                if join_cls.classname not in self.joined:
                    self.query = self.query.join(join_cls)
                    self.joined.append(join_cls.classname)
            else:
                prop: Column = getattr(self.cls, col)
                if not isinstance(prop, InstrumentedAttribute):
                    raise Exception()
        except Exception as e:
            raise QueryBuilderException(f"{join_cls} has no column {col}!" if join_cls is not None else f"{self.cls} has no column {col}!")

        if isinstance(filter_cls, StringFilter):
            self._add_string(filter_cls, prop)
        elif isinstance(filter_cls, DatetimeFilter):
            self._add_datetime(filter_cls, prop)
        elif isinstance(filter_cls, NumberFilter):
            self._add_number(filter_cls, prop)
        elif isinstance(filter_cls, ExistsFilter):
            self._add_exists(filter_cls, prop)
        elif isinstance(filter_cls, BooleanFilter):
            self.__add_bool(filter_cls, prop)
        else:
            raise QueryBuilderException(f"Invalid filter provided: {type(filter_cls)}!")

        return self

    def add_multiple(self, filters: Sequence[BaseTypeFilter], columns: Sequence[str]):
        if len(filters) != len(columns):
            raise QueryBuilderException(f"Inconsistent lengths between filters and columns: {len(filters)} != {len(columns)}!")

        for f, c in zip(filters, columns):
            self.add(f, c)

        return self

    def _apply_sort(self, **kwargs):
        sort_by = kwargs.get('sort', None)
        if isinstance(sort_by, str):
            desc = kwargs.get('desc', False)
            self.query = self.query.order_by(getattr(self.cls, sort_by)) if not desc else self.query.order_by(getattr(self.cls, sort_by).desc())

    def _apply_filters(self, **kwargs):
        filters = kwargs.get('filters', None)
        if isinstance(filters, list):
            for fil in filters:
                if isinstance(fil, tuple) or isinstance(fil, list):
                    join_cls, f = fil
                    if not isinstance(f, BaseFilter):
                        raise QueryBuilderException(f"Query filter is set but is of invalid type!")

                    for col, type_filter in f.for_query().items():
                        if type_filter is None:
                            continue
                        self.add(type_filter, col, join_cls)

                elif isinstance(fil, BaseFilter):
                    for col, type_filter in fil.for_query().items():
                        if type_filter is None:
                            continue
                        self.add(type_filter, col)
                elif fil is None:
                    continue
                else:
                    raise QueryBuilderException('Invalid filter provided!')

    def build(self, **kwargs):
        self._apply_filters(**kwargs)
        self._apply_sort(**kwargs)
        return self

    def all(self) -> Sequence[Sequence[Any]]:
        return self.query.all()

    def paginate(self, page: int, per_page: int = 30) -> Sequence[Sequence[Any]]:
        return self.query.limit(per_page).offset(page * per_page).all()

    def first(self) -> Optional[Sequence[Any]]:
        return self.query.first()

    def get(self, id: Union[int, str]) -> Optional[Any]:
        return self.query.get(id)