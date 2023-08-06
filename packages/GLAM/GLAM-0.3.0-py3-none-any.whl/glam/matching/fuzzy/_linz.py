import pandas as pd
import os

from glam.utils import utils

def load_linz(path):
    linz = pd.read_csv(path, dtype = 'str').fillna('')
    linz['postcode_int'] = pd.to_numeric(linz['postcode'])
    linz['address_number_int'] = pd.to_numeric(linz['address_number'])
    return linz

def upgrade_linz(linz_path, pc_path, outpath):
    """
    upgrade the LINZ datafile for matching purposes by including extra parameters
    Requires GeoPandas
    """

    utils.check_package_dependency('geopandas')
    import geopandas as gpd
    
    pc = gpd.read_file(pc_path)

    linz = utils.load_linz(linz_path)
    linz = gpd.GeoDataFrame(linz)
    linz['geometry'] = gpd.points_from_xy(linz['shape_X'],linz['shape_Y'])
    linz = linz.set_crs('EPSG:4326')

    print('  Adding postcode column to linz dataset...')
    linz = gpd.sjoin(linz,pc,how='left',predicate='within')
    linz = linz[['address_id','road_section_id','unit_value','address_number','address_number_suffix',
                'address_number_high','full_road_name_ascii','suburb_locality_ascii','town_city_ascii','full_address_ascii','POSTCODE','shape_X','shape_Y']]
    linz = linz.rename(columns = {'POSTCODE' : 'postcode'})

    print('  Adding suburb_town_city column to linz dataset...')
    linz['suburb_town_city'] = (linz['suburb_locality_ascii'].fillna('') + ', ' + linz['town_city_ascii'].fillna(''))
    linz['suburb_town_city'] = linz['suburb_town_city'].str.replace('^, |, $', '', regex=True) # remove leading and trailing commas and spaces

    print('  Optimising datatypes...')
    linz['postcode_int'] = pd.to_numeric(linz['postcode'])
    linz['address_number_int'] = pd.to_numeric(linz['address_number'])

    print('  Saving upgraded linz file to {}'.format(outpath))
    linz.to_csv(outpath,index=False)