

from functools import reduce

import numpy as np
import pandas as pd


def one_hot_encoding_unites(df):
    unites = df #.head(10)
    all_type = np.unique(
        np.array(
            reduce(lambda cur, prev: cur+prev,[[c['type'] for c in x]\
                if x is not None and len(x) > 0 else []\
                    for x in unites])))

    unites_test = np.array([dict(sorted({**item, **{key:0 for key in list(set(all_type) - set(item.keys()))}}.items()))\
        for item in [{c['type']: c['total'] \
            for c in x} if x is not None and len(x) > 0 else {} \
                for x in unites]])

    df_unites =pd.DataFrame(columns=all_type,data=[[int(item) for item in unites.values()] for unites in unites_test])

    return df_unites

def split_df_on_variable(df, split_variable, variables_interest):
    df_split = df.groupby(split_variable).apply(lambda x: x[variables_interest])
    df_split.index = df_split.index.droplevel(0)
    return df_split
    