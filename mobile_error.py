import pandas as pd
# import geopandas as gpd
# import fiona
import matplotlib.pyplot as plt
import multiprocessing as mp
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading
import folium
# from geopandas import GeoDataFrame
# from shapely.geometry import Point

def mobileErrorAnalysis(in_poly, in_points, out_dir, buff_size = 30):

    start = datetime.now()

    fiona.drvsupport.supported_drivers['kml'] = 'rw' # enable KML support which is disabled by default
    fiona.drvsupport.supported_drivers['KML'] = 'rw'

    fiona.drvsupport.supported_drivers['libkml'] = 'rw' # enable KML support which is disabled by default
    fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

    print("Reading the files..")
    poly = gpd.read_file(in_poly)
    points = pd.read_csv(in_points, skipinitialspace = True, usecols=[0,2,3])
    points.rename(columns = {'name' : "Name"}, inplace = True)
    geometry = [Point(xy) for xy in zip(points.lng, points.lat)]
    points = points.drop(['lng', 'lat'], axis=1)
    points = GeoDataFrame(points, crs="EPSG:4326", geometry=geometry)
    


    print("Analyzing {} points in relation to {} polygons".format(points.shape[0], poly.shape[0]))
    print(poly.head())
    print(points.head())

    poly = poly[["Name", "geometry"]]
    points = points[["Name", "geometry"]]

    points["description"] = 1

    map_html = folium.Map((points["geometry"].iloc[0].x, points["geometry"].iloc[0].y), zoom_start=5, tiles='cartodbpositron')
    folium.GeoJson(poly["geometry"]).add_to(map_html)

    poly = poly.to_crs(epsg = 3395)
    points = points.to_crs(epsg = 3395)
    

    print("Making buffer...")
    points["geometry"] = points.geometry.buffer(buff_size)
 
    print("Performing dissolve...")
    points2 = points.dissolve(by='Name', aggfunc='sum').reset_index()
    folium.GeoJson(points2["geometry"]).add_to(map_html)
    

    print("Performing symmetric difference...")
    points3 = gpd.overlay(points,poly, how='symmetric_difference')
    points3.drop(["Name_2"], axis = 1, inplace = True)
    del points
 
    print("Performing dissolve...")
    points3 = points3[['Name_1', 'description', 'geometry']]
    points3 = points3.dissolve(by='Name_1', aggfunc='sum').reset_index()
    points3 = points3.rename(columns={'description': 'Intersecting Buffers'})

    points2 = points2.sort_values(by = ["Name"]).reset_index()
    points3 = points3.sort_values(by = ["Name_1"]).reset_index()
    poly = poly.sort_values(by = ["Name"]).reset_index()


    error_area = points3["geometry"].area
    input_area = points2.area
    store_size = poly["geometry"].area
    ping_count = points2['description']
    store_names = points2['Name']
    int_count = points3['Intersecting Buffers']


    del points2
    del points3
    del poly

    
    df = pd.concat([store_names, input_area, error_area, store_size, ping_count, int_count], axis=1)
    df.rename(columns={0: 'Mobile Ping Buffer Area', 1: 'Ping Buffer Area Outside Store', 
                    2: 'Store Area','description': 'Number of Pings', 
                    'Intersecting Buffers': 'Number of Intersections'}, inplace=True)
    df = df.sort_values(by=["Store Area"]).reset_index()
    df['Area Percent Difference'] = (df['Ping Buffer Area Outside Store'] / df['Mobile Ping Buffer Area'])*100
    df.drop(["index"], axis = 1, inplace = True)
    print(df.head(10))


    print("Creating the charts...")
    ax = plt.figure(figsize = (15, 25))
    ax = df.plot.bar(x='Name', title='Mobile Ping Error Analysis', rot=0, figsize=(15,7.5), colormap='jet')
    ax.title.set_size(20)
    ax.set_xlabel("Store Polygon", fontsize=15)
    ax.set_ylabel("Area (Meters Square)", fontsize=15)
    for i, label in enumerate(list(df.index)):
        score = df.loc[label]['Area Percent Difference']
        height = df.loc[label]['Store Area']
        ax.annotate(r'{}%'.format(str(round(score, 2))), (i, height + 1000), color='darkred', fontsize=15)
    ax.figure.savefig(out_dir +"_barChart.png")
   
    plt.close()
    fig, ax = plt.subplots()
    plt.xlabel("Store Area (Meters Square)", fontsize = 15)
    plt.ylabel("Percent Error", fontsize = 15)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.tick_params(axis='both', which='minor', labelsize=8)
    plt.plot(df['Store Area'], df['Area Percent Difference'],  label = "Percent of Total Buffer Outside Store Polygon")
    plt.title("Mobile Ping Error Rate", fontsize = 20)
    plt.legend(loc=2, prop={'size': 12})

    print("Saving the work..")
    fig.savefig(out_dir + "_lineChart.png")
    df.to_csv(out_dir + "_Table.csv", index=False)
    map_html.save(out_dir + "_Map.html")

    print("Finished execution: {}".format(datetime.now() - start))

    return df
