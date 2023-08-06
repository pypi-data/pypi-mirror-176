import networkx as nx
import pandas as pd
import umap
from sklearn import decomposition, manifold


def reduce_dim(df, method='spring', **kwargs):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    if method == 'spring':
        G = nx.Graph(df.corr())
        pos = nx.spring_layout(G)
        df_2d = pd.DataFrame(pos).T

    elif method == 'umap':
        pos = umap.UMAP(**kwargs).fit_transform(df)
        df_2d = pd.DataFrame(pos)

    elif method == 'tsne':
        pos = manifold.TSNE(**kwargs).fit_transform(df)
        df_2d = pd.DataFrame(pos)

    elif method == 'pca':
        pos = decomposition.PCA(n_components=2, **kwargs).fit_transform(df)
        df_2d = pd.DataFrame(pos)

    else:
        raise ValueError(method)

    df_2d.columns = ['x', 'y']
    return df_2d
