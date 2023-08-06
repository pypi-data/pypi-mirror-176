import networkx as nx
import pandas as pd
import numpy as np


def reduce_dim(df, method='spring'):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    if method == 'spring':
        G = nx.Graph(df.corr())
        pos = nx.spring_layout(G)
        df_2d = pd.DataFrame(pos).T
    else:
        raise ValueError(method)

    return df_2d
