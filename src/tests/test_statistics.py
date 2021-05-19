import unittest

from ..statistics import Statistics


class TestStatistics(unittest.TestCase):
    def setUp(cls):
        cls.statistics = Statistics()

    def test_is_true_positive_same_values(self):
        expected = True

        response = self.statistics.is_true_positive("FOO", "FOO")

        self.assertEqual(expected, response)

    def test_is_true_positive_same_values_not_found(self):
        expected = False

        response = self.statistics.is_true_positive("NOT_FOUND", "NOT_FOUND")

        self.assertEqual(expected, response)

    def test_is_false_positive(self):
        expected = True

        response = self.statistics.is_false_positive("FOO", "BAR")

        self.assertEqual(expected, response)

    def test_is_false_positive_expected_not_found(self):
        expected = True

        response = self.statistics.is_false_positive("NOT_FOUND", "BAR")

        self.assertEqual(expected, response)

    def test_is_true_negative(self):
        expected = True

        response = self.statistics.is_true_negative("NOT_FOUND", "NOT_FOUND")

        self.assertEqual(expected, response)

    def test_is_true_negative_expected_false(self):
        expected = False

        response = self.statistics.is_true_negative("FOO", "FOO")

        self.assertEqual(expected, response)

    def test_is_false_negative(self):
        expected = True

        response = self.statistics.is_false_negative("FOO", "NOT_FOUND")

        self.assertEqual(expected, response)

    def test_is_false_negative_false(self):
        expected = False

        response = self.statistics.is_false_negative("FOO", "BAR")

        self.assertEqual(expected, response)

    def test_calc_precision(self):
        expected = 0.625

        response = self.statistics.calc_precision(100, 60)

        self.assertEqual(expected, response)

    def test_calc_precision_division_by_zero(self):
        expected = -1

        response = self.statistics.calc_precision(-10, 10)

        self.assertEqual(expected, response)

    def test_calc_recall(self):
        expected = 0.625

        response = self.statistics.calc_recall(100, 60)

        self.assertEqual(expected, response)

    def test_calc_recall_division_by_zero(self):
        expected = -1

        response = self.statistics.calc_recall(-10, 10)

        self.assertEqual(expected, response)

    def test_f1_score(self):
        expected = 10.0

        response = self.statistics.f1_score(10, 10)

        self.assertEqual(expected, response)

    def test_f1_score_division_by_zero(self):
        expected = -1

        response = self.statistics.f1_score(-10, 10)

        self.assertEqual(expected, response)
