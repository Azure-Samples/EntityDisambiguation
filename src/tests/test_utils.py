import os
import unittest

from utils import Utils


class TestStatistics(unittest.TestCase):
    def setUp(cls):
        cls.utils = Utils(os.path.join(os.path.join(os.pardir, "resources")))

    def test_get_subsets(self):
        expected = [('A',), ('B',), ('C',), ('A', 'B'), ('A', 'C'), ('B', 'C'), ('A', 'B', 'C')]

        response = self.utils.get_subsets(["A", "B", "C"])

        self.assertEqual(expected, response)

    def test_sort_on_f1_score(self):
        expected = [{'f1': 14}, {'f1': 12}, {'f1': 10}]

        response = self.utils.sort_on_f1_score([{"f1": 12}, {"f1": 10}, {"f1": 14}])

        self.assertEqual(expected, response)

    def test_get_maximum_rank_from_azure_search_response(self):
        expected = "BAZ"

        service_response = {"value": [
            {"@search.score": 1, "standard_lucene": "FOO"},
            {"@search.score": 3, "standard_lucene": "BAR"},
            {"@search.score": 5, "standard_lucene": "BAZ"}]}

        response = self.utils.get_maximum_rank_from_azure_search_response(service_response)

        self.assertEqual(expected, response)
