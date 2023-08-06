# Geocoding via LINZ Address Matching (GLAM) 

# Work in progress!

[[_TOC_]]

## Overview
This package implements methods for performing entity matching on unstructured NZ addresses to the LINZ street address database. This package does not support PO boxes or international addresses. 

## Installation 

Get the latest version of glam by installing from PyPi (not true yet)
```
pip install glam
``` 

## Usage
```
from glam.interface import Geocoder

data_dir = 'data' # Location of glam data dependencies
gc = Geocoder(data_dir)

addresses = [
  'level 10, 10 customhouse quay, wellington central',
  'third floor 18 viaduct harbour ave auckland',
]

gc.geocode_addresses(addresses)
```

Output:
```
[{'address_number': '10',
  'full_road_name_ascii': 'Customhouse Quay',
  'suburb_locality_ascii': 'Wellington Central',
  'town_city_ascii': 'Wellington',
  'postcode': '6011',
  'shape_X': '174.7784009',
  'shape_Y': '-41.28219255',
  'match_score': 100.0},
 {'address_number': '18',
  'full_road_name_ascii': 'Viaduct Harbour Avenue',
  'suburb_locality_ascii': 'Auckland Central',
  'town_city_ascii': 'Auckland',
  'postcode': '1010',
  'shape_X': '174.7577686',
  'shape_Y': '-36.8453608833',
  'match_score': 100.0}]
```

## Dependencies
- Models are packaged with the Python wheel.
- Dependencies can be downloaded from git. 
- Alternatively, dependencies can be rebuilt from the raw LINZ and PNF files the first time using the geocoder (may be slow).

  - Raw LINZ dataset can be downloaded from [here]([https://data.linz.govt.nz/layer/53353-nz-street-address/)
  - PNF file is available for purchase from NZ Post [here](https://www.nzpost.co.nz/business/sending-within-nz/quality-addressing/postcode-network-file) (optional, but postcodes will not be available without the PNF file. And it may also improve geocoding efficiency)

## Models 

The models available in GLAM are divided into _matchers_ and _parsers_. Some matchers work directly on the unstructured address strings, and others require a parser to add structure to the addresses before matching

### Matchers
- **Hybrid (recommended)** - implements a custom embedding model that exploits the structure of addresses. Requires a parser.
- **Fuzzy** - implements rule-based fuzzy matching on address components. Requires a parser.
- **Siamese** - implements a siamese RNN for address embeddings and a KD-Tree for distance calculations. Does not require a parser.

### Parsers
- **RNN (recommended)** - uses a character based RNN to classify address components
- **HMM** - implements a hidden markov model for classification of most likely address components

## Thoughts in progress
- how to fix haurua problem
  - geometric mean for letter group instead of normal mean
  - vector entry for weighted ordinals?
- Create customised embeddings by using concatenated scaled numbers and street + suburb embeddings. pre-compute trees for different embedding combinations e.g. no postcode, no numbers, etc.
  - Will have to work out how to manage scaling and weighting of different components embedding so one doesn't dominate
  - should i combine street and suburb_town_city? yes
- Use RNN for entire address embeddings
  - try introducing labels to character embeddings
  - try creating more positive examples.
  - regenerative training dataset - generate triplets that aren't correct with current weights
- libpostal exists. should i compare glam parser with this. far out it's hard to use
- conditional random fields 
 - Maximum entropy markov models

  


## Author
Liam Morris

liam.morris04@gmail.com

Please reach out if you have any questions :)