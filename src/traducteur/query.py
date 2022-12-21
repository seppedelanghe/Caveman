
from typing import List
from .lib.model import BaseModel

class Query:
    '''
        Getter
    '''
    def first(self):
        pass

    def last(self):
        pass

    def exists(self):
        pass

    def get(self):
        pass

    def count(self):
        pass

    def paginate(self):
        pass


    '''
        filters    
    '''
    def where(self, **args):
        pass


class SQLQuery(Query):
    def __init__(self, table: str, columns: List[str] = []):
        self.table = table
        self.columns = columns

        self.wheres = []
        self.lim = -1

    def where(self, **args):
        matcher = "=" if len(args) == 2 else args[1]
        q = f"{args[0]} {matcher} {args[2] if len(args) == 3 else args[1]}"
        self.wheres.append(q)

    def limit(self, n: int):
        self.lim =  n


    def _columns(self):
        return "*" if len(self.columns) == 0 else ", ".join(self.columns)

    def _wheres(self):
        return f"WHERE {', '.join(self.wheres)}"

    def _build(self):
        q = f"SELECT {self._columns()} FROM {self.table} {self.wheres}"
        if self.lim != -1:
            q += f"LIMIT {self.lim}"

        q += ";"

        return q