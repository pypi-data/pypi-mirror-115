import pandas as pd
import os


def index_futures_close():
    dirname, _ = os.path.split(os.path.abspath(__file__))
    path = os.path.join(dirname, 'dataset', '_close.csv')
    return pd.read_csv(path, index_col=0, header=0)


def index_futures_adj():
    dirname, _ = os.path.split(os.path.abspath(__file__))
    path = os.path.join(dirname, 'dataset', '_adj_close.csv')
    return pd.read_csv(path, index_col=0, header=0)


def index_futures_volume():
    dirname, _ = os.path.split(os.path.abspath(__file__))
    path = os.path.join(dirname, 'dataset', '_volume.csv')
    return pd.read_csv(path, index_col=0, header=0)
