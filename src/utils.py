"""
This file contains methods that may frequently being used in this project
"""
import json
import os
import csv
from itertools import chain, combinations

import yaml
import pandas as pd


class Utils:
    """
    This class contains methods that may frequently being used in this project
    """

    def __init__(self, resources_path):
        self.resources_path = resources_path

    def generate_reports(self, data, file_name):
        """
        This method stores data as CSV file in generated directory
        :param data:
        :param file_name:
        :return:
        """
        generated = "generated"
        self.make_directory_if_not_exists(generated)
        data_frame = pd.DataFrame(data)
        filename = os.path.join(generated, file_name + '.csv')
        data_frame.to_csv(filename)

    def read_json_from_resources(self, filename):
        """
        This method loads a json from a file
        :param filename:
        :return: a json file
        """
        full_path = os.path.join(self.resources_path, filename)
        resources = {}
        if full_path:
            with open(full_path, 'r') as file:
                resources = json.load(file)
        return resources

    def read_csv(self, filename="names.csv"):
        """
        This method reads a CSV file to a list
        :param filename:
        :return: a list containing elements per line of CSV
        """
        filename = os.path.join(self.resources_path, filename)
        with open(filename, 'r') as a_file:
            return list(csv.reader(a_file))

    def get_config(self):
        """
        this method loads a YAML config file in a dictionary
        :return: dictionary of configuration file
        """
        yaml_path = os.path.join(self.resources_path, "config.yml")
        with open(yaml_path, 'r') as configuration:
            return yaml.load(configuration, Loader=yaml.FullLoader)

    @staticmethod
    def get_maximum_rank_from_azure_search_response(response):
        """
        this method receives a response and returns the maximum ranked hits.
        it will return NOT_FOUND if response has not hits
        :param response:
        :return: a username with the maximum rank or NOT_FOUND otherwise
        """
        score = 0
        found_name = "NOT_FOUND"
        for hit in response['value']:
            if hit['@search.score'] > score:
                score = hit['@search.score']
                found_name = hit['standard_lucene']
        return found_name

    @staticmethod
    def get_subsets(iterable):
        """
        This method is to create a full subset of the elements of an iterable parameter
        :param iterable:
        :return:
        """
        list_of_set = list(iterable)
        return list(chain.from_iterable(combinations(list_of_set, r)
                                        for r in range(1, len(list_of_set) + 1)))

    @staticmethod
    def sort_on_f1_score(a_list, descending=True):
        """
        this method will sort a list on f1 score fields in Descending order
        :param a_list:
        :return: a sorted list
        """
        return sorted(a_list, key=lambda i: (i['f1']), reverse=descending)

    @staticmethod
    def make_directory_if_not_exists(directory):
        """
        this method creates a directory if it does not exists
        :param directory:
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
