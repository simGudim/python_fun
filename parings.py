import pandas as pd 
import numpy as np 
from sklearn.neighbors import KDTree, NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import pickle
import math
from concurrent import futures

def candidates(dataset,search_ds, row, k, cols):
    value1 = row.iloc[:,3].to_list()[0]
    matches1 = search_ds[search_ds[cols[3]].astype('str').str[0:3] == value1]

    value2 = row.iloc[:,3].to_list()[0][0:2]
    matches2 = search_ds[search_ds[cols[3]].astype('str').str[0:2] == value2]

    value3 = row.iloc[:,3].to_list()[0][0]
    matches3 = search_ds[search_ds[cols[3]].astype('str').str[0] == value3]

    if matches1.shape[0] >= k:
        matches_idx = matches1["old_idx"].to_list()
        matches = dataset.loc[matches_idx, :]
        return matches
    elif matches2.shape[0] >= k:
        matches_idx = matches2["old_idx"].to_list()
        matches = dataset.loc[matches_idx, :]
        return matches
    elif matches3.shape[0] >= k:
        matches_idx = matches3["old_idx"].to_list()
        matches = dataset.loc[matches_idx, :]
        return matches
    elif not matches3.empty:
        matches_idx = matches3["old_idx"].to_list()
        matches = dataset.loc[matches_idx, :]
        return matches
    else:
        return search_ds
   

def steps(dataset, search_ds, search_idx, cols, k=10):
    result = []
    for i in search_idx:
        row = dataset.iloc[i:i+1, :]
        matches = candidates(dataset, search_ds, row, k, cols)
        
        
        if matches.empty:
            matches = search_ds
            tree = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(matches[cols[4:]].values)
        elif matches.shape[0] < k:
            tree = NearestNeighbors(n_neighbors=matches.shape[0], algorithm='auto').fit(matches[cols[4:]].values)
        else:
            tree = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(matches[cols[4:]].values)

        distances, idx = tree.kneighbors(row[cols[4:]])
        nn = idx.tolist()[0]
        matches_idx = matches.iloc[nn, :]["old_idx"].to_list()
        matches = dataset.loc[matches_idx, :]

        val1 = row.iloc[:,1].to_list()[0]
        matches["search_id"] = val1
        result.append(matches)

    result_df = pd.concat(result)
    return result_df

def pairings(indir, outdir, treatment, k_dist):

    dataset = pd.read_csv(indir)
    cols = dataset.columns.to_list()
    dataset["old_idx"] = dataset.index
    dataset = dataset[["old_idx"] + [cols][0]]
    cols = dataset.columns.to_list()
    dataset = dataset.fillna(0)

    scaler = MinMaxScaler().fit(dataset[cols[4:]])
    dataset[cols[4:]] = scaler.fit_transform(dataset[cols[4:]])
    search_idx = dataset.index[dataset[cols[2]] == treatment].tolist()
    print(len(search_idx))

    search_ds = dataset.loc[dataset[cols[2]] != treatment]

    max_entry = math.floor(len(search_idx) / 4)
    sources  = [search_idx[x: x + max_entry] for x in range(0, len(search_idx), max_entry)]


    return dataset, search_ds, sources, cols

def main():
    if __name__ == "__main__":
        result = []
        with futures.ProcessPoolExecutor() as executor:
            dataset, search_ds, sources, cols = pairings(r"J:\Sobeys\2020\Special_Projects\20201009_Sobeys_AI_Validation_Tracking\Tracking\Workspace_Prorated_Variables\test.csv", "", "test",  30)
            results = [executor.submit(steps, dataset, search_ds, i, cols, 30) for i in sources]
            for f in futures.as_completed(results):
                result.append(f.result())
        df = pd.concat(result)
        print(df)

main() 
