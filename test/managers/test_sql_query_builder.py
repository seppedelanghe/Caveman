import os
import unittest


class SqlQueryBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        os.environ['SQL_CONNECTION_STRING'] = "sqlite:///test.db"

    def test_sql_query_builder_can_init(self):
        pass

    def test_sql_query_builder_can_add_string(self):
        pass

    def test_sql_query_builder_can_add_number(self):
        pass

    def test_sql_query_builder_can_add_datetime(self):
        pass

    def test_sql_query_builder_can_add_exists(self):
        pass

    def test_sql_query_builder_can_add_filter(self):
        pass

    def test_sql_query_builder_can_add_multiple_filter(self):
        pass

    def test_sql_query_builder_can_build_from_kwargs(self):
        pass

    def test_sql_query_builder_can_query_all(self):
        pass

    def test_sql_query_builder_can_paginate(self):
        pass

    def test_sql_query_builder_can_get_first(self):
        pass
