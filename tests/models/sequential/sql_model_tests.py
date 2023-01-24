import os
import unittest


class SqlModelTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        os.environ['SQL_CONNECTION_STRING'] = "sqlite:///test.db"

    def test_sql_model_can_init(self):
        pass

    def test_sql_model_can_save(self):
        pass

    def test_sql_model_can_update_itself(self):
        pass

    def test_sql_model_can_get(self):
        pass

    def test_sql_model_can_delete(self):
        pass

    def test_sql_model_can_map_to_other_model(self):
        pass

    def test_sql_model_can_convert_to_dict(self):
        pass

    def test_sql_model_can_get_classname(self):
        pass

    def test_sql_model_can_be_mapped_from(self):
        pass

    def test_sql_model_can_be_loaded_from_dict(self):
        pass

    def test_sql_model_can_be_loaded_from_json(self):
        pass

    def test_sql_model_can_be_paginated(self):
        pass

    def test_sql_model_can_check_if_it_exists(self):
        pass

    def test_sql_model_can_get_manager(self):
        pass
