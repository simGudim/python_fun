import pandas as pd
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
import os
import requests
import json
import time
import math
import urllib3
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import sys


## Update the Canada map with  wget http://download.geofabrik.de/north-america/canada-latest.osm.pbf
## Extarct the data with docker run -t -v C:\Users\sgudim\map:/data osrm/osrm-backend:v5.21.0 osrm-extract -p /opt/car.lua /data/canada-latest.osm.pbf
## Contacrt the data with docker run -t -v C:\Users\sgudim\map:/data osrm/osrm-backend:v5.21.0 osrm-contract /data/canada-latest.osrm
## Start OSRM through Docker with docker run --name dd -t -i -p 5006:5006 -v C:\Users\sgudim\map:/data osrm/osrm-backend:v5.22.0 osrm-routed --algorithm ch --max-table-size=1000000 -p 5006 /data/canada-latest.osrm
## Reset your docker containers docker container prune
## Clean your docker images docker system prune

def dd(indir, outdir, pc2_name, dd_name):

    now = datetime.now()

    print("Building a local server and loading the map...")
    
    # Popen("Z:\Base6\General\Processes\ADW_runner\osrm-backend\osrm_Release\osrm-routed.exe --algorithm ch --max-table-size=1000000 Z:\Base6\General\Processes\ADW_runner\map\canada-latest.osrm --port 5000", stdout=PIPE)
    # sys.path.insert(1, r"C:\Users\sgudim\map")
    # Popen("docker run -t -i -p 5005:5005 -v C:\Users\sgudim\map:/data osrm/osrm-backend:v5.22.0 osrm-routed --algorithm ch --max-table-size=1000000 -p 5005 /data/canada-latest.osrm", stdout=PIPE)
    # Popen("docker run -t -i -p 5005:5005 -v C:\\Users\\sgudim\\map:/data osrm/osrm-backend:v5.22.0 osrm-routed --algorithm ch --max-table-size=1000000 -p 5005 /data/canada-latest.osrm", stdout=PIPE)
    Popen("docker start dd", stdout=PIPE)
    try:
        if requests.get("http://127.0.0.1:5006").status_code == 400:
            print("We good!")
        else:
            raise Exception("Docker not Running! Please run container driveDistance")
    except requests.ConnectionError:
        time.sleep(10)
            
    print("Formating the data...")

    source_df = pd.read_csv(r"Z:\Base6\General\Processes\ADW_runner\files\general_data\FSALDU2019.csv")
    
    destination_df = pd.read_csv(indir)
    source_df = source_df.round(4)
    destination_df = destination_df.round(4)

    source_columns = source_df.columns.to_list()
    destination_columns = destination_df.columns.to_list()

    destination_df["coords"] = destination_df.apply(lambda x: "{},{}".format(x[destination_columns[1]], x[destination_columns[2]]), axis = 1)
    destination_list = destination_df["coords"].values.tolist()

    source_df["coords"] = source_df.apply(lambda x: "{},{}".format(x["CentroidX"], x["CentroidY"]), axis = 1)
    source_list = source_df["coords"].values.tolist()
    label = destination_df[destination_columns[0]].values.tolist()
    destination_dict = dict(zip(range(len(destination_list)), label))
    source_df = source_df[source_columns[0]]

    del destination_df

    if len(source_list) * len(destination_list) > 1000000:
        max_entry = math.floor((1000000 / len(destination_list)) - 100)
        source_chunks = [source_list[x: x + max_entry] for x in range(0, len(source_list), max_entry)]
    else:
        source_chunks = [source_list]

    dist_list = []
    print("Calculating the matrix...")
    for i in source_chunks:
        source_len = len(i)
        source_index = list(range(source_len))
        i.extend(destination_list)
        dest_index = list(range(source_len, len(i)))

        source_idx_str = ";".join(map(str, source_index))
        dest_idx_str = ";".join(map(str, dest_index))
        coords_str = ";".join(i)
        
        url_routes = 'http://127.0.0.1:5006/table/v1/driving/{0}?sources={1}&destinations={2}&annotations=distance'.format(coords_str, source_idx_str, dest_idx_str)
        response = requests.get(url_routes)
        json_geocode = response.json()
    
        mins = [(np.nanmin(np.array(x)/1000), x.index(np.nanmin(np.array(x)))) if x.count(None) != len(x) else (None, None) for x in json_geocode["distances"]]
        dist_list.extend(mins)
        print("Finished processing {} out of {} postalcodes".format(len(dist_list), len(source_list)))

    del source_chunks
    del source_index
    del dest_index
    del coords_str
    del source_idx_str
    del dest_idx_str
    del url_routes

    print("Killing the server and saving the work...")

    # Popen('taskkill /f /im Z:\Base6\General\Processes\ADW_runner\osrm-backend\osrm_Release\osrm-routed.exe' , stdin=PIPE, stdout=PIPE, stderr=PIPE)
    Popen("docker stop dd" , stdin=PIPE, stdout=PIPE, stderr=PIPE)
    df_result = pd.DataFrame(dist_list, columns = ["{}".format(dd_name), "Dest_idx"])
    df_label = pd.DataFrame.from_dict(destination_dict, orient = "index", columns = ["{}".format(pc2_name)])
    source_df = pd.concat([source_df, df_result], axis = 1)
    source_df = pd.merge(source_df, df_label, left_on = "Dest_idx", right_index = True)
    
    dd = source_df[[source_columns[0]] + ["{}".format(dd_name)]]
    dd.to_csv(outdir + "_dd.csv", index = False)

    pc2str = source_df[[source_columns[0]] + ["{}".format(pc2_name)]]
    pc2str.to_csv(outdir + "_pc2str.csv", index = False)
    print(dd.head())
    print(pc2str.head())
    print("Finished Execution in {}".format(datetime.now() - now))

    return outdir + "_dd.csv", outdir + "_pc2str.csv"