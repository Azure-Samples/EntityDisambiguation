from azuresearchclient import AzureSearchClient
from constants import Constants
from statistics import Statistics

if __name__ == "__main__":
    # Create Search Index
    index_name = "INDEX_NAME"
    AZURE = AzureSearchClient()
    # Create Search Index
    AZURE.create_index(index_name)
    # insert documents into the search index (corrected spelled names)
    AZURE.insert_documents(index_name)

    STATS = Statistics()
    # target fields to be searched
    FIELDS_SET = Constants.name_search_fields
    all_subsets = STATS.utils.get_subsets(FIELDS_SET)
    # list of correct names (already uploaded to the search index)
    correct_list = STATS.utils.read_csv("names-expected.csv")
    # list of misspelled names
    misspelled_list = STATS.utils.read_csv("names-misspelled.csv")
    # making queries (with misspelled names) and measure the result
    STATS.calculate_statistics(
        correct_list, misspelled_list, all_subsets, AZURE, True
    )  # noqa: E501

    # plot the results
    SCORES = STATS.generate_f1()
    STATS.create_plot(SCORES)
