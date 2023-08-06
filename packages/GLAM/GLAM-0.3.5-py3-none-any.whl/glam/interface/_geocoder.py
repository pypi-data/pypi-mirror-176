import os
import importlib

from typing import List

from glam import parsing, matching, preprocessing

class Geocoder():
    '''
    A class for interacting with geocoding methods 

    ...

    Attributes
    ----------
    data_dir : str
        data directory for glam dependencies
    matcher : Matcher
        Matcher to be used when geocoding addresses
    parser : Parser
        Parser to be used for parsing addresses or when geocoding (if required by the matcher)

    Methods
    ---------
    geocode_addresses(addresses: List[str]) -> List[dict]
        Geocode a list of unstructured addresses
    parse_addresses(addresses: List[str]) -> List[dict]
        Parse a list of unstructured addresses 
    '''

    def __init__(self, data_dir, matcher = "Embedding", parser = 'RNN') -> None:
        self.data_dir = data_dir
        self._set_parser(parser)
        self._set_matcher(matcher)

    def __repr__(self) -> str:
        repr = f'Geocoder\n Data directory: {self.data_dir}\n Matcher: {self.matcher.type}\n Parser: {self.parser.type}'
        return repr

    def _set_parser(self, parser: str) -> None:
        """Sets parser to be used when geocoding addresses (if required by the chosen matcher)"""

        parser_switch = {
            'rnn' : parsing.RNNParser,
            'crf' : parsing.HMMParser
        }
    
        self.parser = parser_switch[parser.lower()]()

    def _set_matcher(self, matcher: str) -> None:
        """Sets matcher to be used when geocoding addresses"""
        
        matcher_switch = {
            'fuzzy' : matching.FuzzyMatcher,
            'embedding' : matching.EmbeddedMatcher,
            'siamese' : matching.SiameseMatcher
        }
    
        self.matcher = matcher_switch[matcher.lower()](self.data_dir)

    def preprocess_addresses(self, addresses: List) -> List:
        processor = preprocessing.PreProcessor()
        return processor.clean_addresses(addresses)

    def parse_addresses(self, addresses: List) -> List:
        return self.parser.parse_addresses(addresses)

    def match_addresses(self, addresses: List) -> List:
        return self.matcher.match_addresses(addresses, build_dependencies = True)

    def geocode_addresses(self, addresses: List, preprocess: bool=True):

        if preprocess:
            addresses = self.preprocess_addresses(addresses)

        if self.matcher._requires_parser:
            addresses = self.parse_addresses(addresses)

        addresses = self.match_addresses(addresses)

        return addresses

def data_dir_validation(data_dir):
    expected_linz_location = os.path.join(data_dir,'nz-street_address.csv')
    print(os.path.isdir(data_dir), os.path.isfile(expected_linz_location))
    return (os.path.isdir(data_dir) and os.path.isfile(expected_linz_location))


