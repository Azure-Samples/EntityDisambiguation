---
page_type: sample
languages:
- python
name: "Entity Disambiguation Using Azure Search"
description: "A methodology to disambiguate misspelled entities by comparing the search retrieval performance with different custom search analyzers in a search engine"
products:
- azure search
- azure-cognitive-services
---
# EntityDisambiguation

This document proposes a methodology to disambiguate misspelled entities by comparing the search retrieval 
performance with different custom search analyzers in a search engine.
 Hence, even if the provided query contains some misspelled entities, 
 the search engine can respond to the request with higher precision and 
 recall than the default settings. This method can be applied to any 
 search engine service capable of adding custom search analyzers.
 

## Features

This project framework provides the following:

* An approach to measure the performance of the search engine in the retrieval of the misspelled personaName when the search engine uses specific or multi search analyzers.


## Getting Started

### Prerequisites

- Python 3.5.3 and above
- Create an [Azure Cognitive Search](https://docs.microsoft.com/en-ca/azure/search/search-create-service-portal)
 using azure portal and fill [config.yml](src/resources/config.yml) config file with properties

### Quick Start

(Add steps to get up and running quickly)

1.  git clone [https://github.com/Azure-Samples/EntityDisambiguation.git](https://github.com/Azure-Samples/EntityDisambiguation.git)
2. `python3 -m venv env`
3. (Unix or MacOS) `source env/bin/activate` (Windows) `env\Scripts\activate.bat`
4. `python -m pip install -r requirements.txt`
5. `cd src`
6. `python main.py`


## Demo

Figure below indicates the overall architecture from user 
speech to search the data source and respond to the user’s request.


![scenario](doc-resources/architecture.png)

### Methodology

Our approach is to measure the performance of the search engine in the retrieval 
of the misspelled personaName when the search engine uses specific or multi search analyzers.

### Usage

#### Create a Search Index and insert documents in the index:

- Search index will be created from the [index-schema.json](src/resources/index-schema.json) file
- documents are people names sourcing from [names.csv](src/resources/names.csv)

```python
from azuresearchclient import AzureSearchClient

AZURE = AzureSearchClient()
# Create Search Index
AZURE.create_index("INDEX_NAME")
# insert documents into the search index (corrected spelled names)
AZURE.insert_documents("INDEX_NAME")
```
#### Query the search index by providing misspelled names and calculate the performance

- Create a set of all analyzers(fields)
- load misspelled names from [names-misspelled.csv](src/resources/names-misspelled.csv)
- load the expected names/results from [names-expected.csv](src/resources/names-expected.csv)
- for all elements in teh subset:
- send a query to the search index providing the missepelled name and target field
    - Mark the reponse (e.g. TP, TN, FP, FN)
    - Calculate the Precision, Recall and F1 score
- statistics will be stored in [generated](src/generated) directory

```python
from constants import Constants
from statistics import Statistics

STATS = Statistics()
# target fields to be searched
FIELDS_SET = Constants.name_search_fields
all_subsets = STATS.utils.get_subsets(FIELDS_SET)
# list of correct names (already uploaded to the search index)
correct_list = STATS.utils.read_csv("names-expected.csv")
# list of misspelled names
misspelled_list = STATS.utils.read_csv("names-misspelled.csv")
# making queries (with misspelled names) and measure the result
STATS.calculate_statistics(correct_list, misspelled_list, all_subsets, AZURE, True)
```
#### Plot the F1 score for each Analyzer

```python
from statistics import Statistics

STATS = Statistics()
SCORES = STATS.generate_f1()
STATS.create_plot(SCORES)
```

![plot](doc-resources/plot.png)

#### Experiment Result

Now consider that there is a name in our search index : **Tom O'halleran**

Our speech recognition or OCR extracted this text with an incorrect spelleing: **Tom O Halleran**

We are experimenting to disambiguate this name with two set ups:
- Default analyzer setup (**standard_lucene**)

- Analyzer with best performance set up (**camelcase,url_email,text_microsoft**)

##### Default analyzer experiment

```python
from azuresearchclient import AzureSearchClient

AZURE = AzureSearchClient()
AZURE.make_search("Tom O Halleran", ["standard_lucene"])
```
**Result:**
```bash
"Tom Canada"
```

##### Analyzer with best performance experiment

```python
AZURE = AzureSearchClient()
AZURE.make_search("Tom O Halleran", ["camelcase", "url_email", "text_microsoft"])
```
**Result:**
```bash
"Tom O'halleran"
```

We can see that default setting was not successful to retrieve the most relevant result.


## Resources

- [Azure Cognitive Search](https://docs.microsoft.com/en-ca/azure/search/search-create-service-portal)
