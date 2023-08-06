
from glam.preprocessing import _preprocessing

class PreProcessor():

    def __init__(self):
        attr_list = dir(_preprocessing)
        self.cleaning_funcs = [getattr(_preprocessing,func) for func in attr_list if func[:5] == 'clean']

    def clean_addresses(self, addresses):
        '''Cleans addresses'''

        addresses = list(addresses)

        for fh in self.cleaning_funcs:
            addresses = fh(addresses)

        return addresses
        
