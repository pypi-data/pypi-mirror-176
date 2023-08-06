import numpy as np
import re

letter_groups = ['ltu',
 'ajv',
 'bo',
 'akr',
 ' cs',
 'inr',
 'aew',
 'hiu',
 'bnu',
 'iwy',
 'ehy',
 'ers',
 'pqz',
 'ahp',
 ' pw',
 'lpr',
 'fmt',
 'ims',
 'hqv',
 'egn',
 'mou',
 'jot',
 ' dz',
 'kst',
 'gjl',
 'bcx',
 'fo',
 'jnx',
 'dgm']

alphabet = ' abcdefghijklmnopqrstuvwxyz'
letter_groups = list(alphabet) #overwrite

def myprod(l):
    k=1 
    for x in l:
        k*=x
    return k

def idx_geom_mean(street, lg):
    l = [f.span()[0]+1 for f in re.finditer(f'[{lg}]',street, flags=re.I)]
    prod = myprod(l)
    b = len(l)
    return b and (prod**(1/b))/len(street) or 0

def embed_text(text, scale, lgs):
    nums = re.sub('[^\d+]','',text)
    chars = re.sub('[\d+]','',text)

    embeddings = [idx_geom_mean(chars,lg)*scale for lg in lgs]
    nums = -1 if len(nums) == 0 else np.log(int(nums)+1)

    return embeddings + [nums]
    

default_weights = {
    'unit' : 0.01,
    'first_number' : 20,
    'first_number_suffix': 0.01,
    'street_name' : 10,
    'suburb_town_city' : 1,
    'postcode' : 15
}


def make_embeddings(address_components, letter_groups = letter_groups, weights = default_weights):
    
    embeddings = []
    if address_components is None or (address_components['first_number'] == 'None' and address_components['street_name'] == 'None'):
        return embeddings

    digits = re.sub('[^\d+]','',address_components.get('unit',''))
    embeddings += [int(digits)+1 if len(digits)>0 else -1]

    if address_components.get('first_number', 'None') != "None":
        embeddings.append(weights['first_number']*np.log(int(address_components['first_number'])))

    suffix = address_components.get('first_number_suffix','None')
    embeddings += [(ord(suffix[0])+1 - ord('A'))/(ord('Z')-ord('A')) if suffix not in ['None',''] else -1]

    if address_components.get('street_name','None') != "None":
        embeddings += embed_text(address_components['street_name'], weights['street_name'], letter_groups)

    if address_components.get('suburb_town_city','None') != "None":
        embeddings += [weights['suburb_town_city']*(len(set(address_components['suburb_town_city'].lower()).intersection(lg))) for lg in letter_groups]

    if address_components.get('postcode','None') != "None":
        embeddings.append(weights['postcode']*np.log(int(address_components['postcode'])))

    return embeddings



