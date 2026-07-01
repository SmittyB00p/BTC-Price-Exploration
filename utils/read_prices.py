import pandas as pd

def read_parquet(
        path='../price_ranges/btc_price_2016-2020.parquet'
        ):
    
    '''
    Reads parquet file from specified path.
    '''

    df = pd.read_parquet(path)

    return df