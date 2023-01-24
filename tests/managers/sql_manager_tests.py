import os
import unittest


class SqlManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        os.environ['SQL_CONNECTION_STRING'] = "sqlite:///test.db"

    def test_sql_manager_can_create_engine(self):
        pass

    def test_sql_manager_can_create_session(self):
        pass

    def test_sql_manager_can_insert_sql_model(self):
        pass

    def test_sql_manager_can_update_sql_model(self):
        pass

    def test_sql_manager_can_delete_sql_model(self):
        pass

    def test_sql_manager_can_get_sql_model(self):
        pass

    def test_sql_manager_can_insert_many_sql_models(self):
        pass

    def test_sql_manager_can_check_if_a_id_for_a_model_exists(self):
        pass

    def test_sql_manager_can_get_all_models_of_a_type(self):
        pass

    def test_sql_manager_can_paginate_models(self):
        pass

    def test_sql_manager_can_custom_query_models(self):
        pass
