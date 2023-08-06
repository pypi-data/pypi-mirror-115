### NCBI DAtaREtrival
Retrives your NCBI search results and through Entrez in a user friendly way.

## Installation
Run the following to install:
```python
pip install ncbiget
```

## Usage

```python
# retrives results from NCBI and writes it to a csv file (Accession ID and Definition)
# query: search details         count: number of items      filename: output file name
from ncbiget import get_genbank
get_genbank(query="Klebsiella pneumoniae", count=1, filename="results.csv") # default

#to get list of unique strains from the csv file
#MAKE SURE THE FORMAT OF THE CSV FILE IS SIMILAR TO THE RESULT FILE FROM get_genbank() i.e. Descriptions should be in column 3
# filename: input file name 
from ncbiget import get_strains
get_strains(filename="results.csv") # default 

#to get fasta file of each strain
#MAKE SURE THE FORMAT OF THE CSV FILE IS SIMILAR TO THE RESULT FILE FROM get_genbank() i.e. Descriptions should be in column 3
# filename: input file name 
from ncbiget import get_fasta
get_fasta(filename="results.csv") # default
```

## Developing ncbidare

To install ncbidare along with the tools you need to develop and run tests, run the following in your virtualenv:
```bash
pip install -e .[dev]
```