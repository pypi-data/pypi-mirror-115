import pandas as pd


def index_futures_close():
    return pd.read_csv('.\dataset\_close.csv', index_col=0, header=0)


def index_futures_adj():
    return pd.read_csv('.\dataset\_adj_close.csv', index_col=0, header=0)


def index_futures_volume():
    return pd.read_csv('.\dataset\_volume.csv', index_col=0, header=0)
