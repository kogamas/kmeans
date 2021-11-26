'''
k means assignment
implement the k means clustering algorithm
@author kogamas
'''

import pandas as pd
import numpy as np
import csv
import random

CSV_PATH = "input.csv"


def read_csv(csv_path):
    dataframe = pd.read_csv(csv_path, delimiter=";", decimal=",", skiprows=2, header=None)
    return dataframe


# param dimensions (x,y) exclusive and how many points to make
# returns a list of random points in the dimensions given
def random_point(x_dim, y_dim, count):
    points = []
    for i in range(count):
        x = random.randrange(0, x_dim)
        y = random.randrange(0, y_dim)
        points.append([x, y])
    return points


# param dimensions of the data
# return indices of the randomly selected points
def random_indices(x_dim, count):
    indices = []
    for i in range(count):
        x = random.randrange(0, x_dim)
        indices.append(x)
    return indices

# param dataframe with the actual values
# param list of the points randomly selected
# return values of the points
def get_values_of_points(value_dataframe: pd.DataFrame, point_list):
    values = []
    value_list = value_dataframe.values.tolist()
    for point in point_list:
        values.append(value_list[point])

    return values

# param two points
# return manhattan distance between those 2 points
def distance(point_a : pd.DataFrame, point_b: pd.DataFrame):
    return_value = abs(point_a.iloc[0] - point_b.iloc[0]) + abs(point_a.iloc[1] - point_b.iloc[1])
    return_value = float(return_value)
    return return_value

# param list of seeds(for clusters) and data
# returns new df with points assigned to clusters
def assign_to_cluster(seed_points_list, data : pd.DataFrame):
    seed_points_df = pd.DataFrame(seed_points_list)
    seed_list = []
    counter = 0
    for data_point in data.loc[:, data.columns!='cluster'].iterrows():
        for seed_point in seed_points_df.iterrows():
            dist = distance(data_point[1], seed_point[1])
            if(counter == 0):
                temp_min = dist
                seed_list.append(0)
            elif(dist < temp_min):
                seed_list.pop()
                seed_list.append(counter)
                temp_min = dist
            counter += 1
        counter = 0
    if 'cluster' in data:
        data['cluster'] = seed_list
    else:
        data.insert(loc=0, column="cluster", value=seed_list)
    return data

# param data, old list of cluster centers/ seeds
# return new list of centered seeds/cluster centers
def center_seeds_in_clusters(df : pd.DataFrame, old_seed_list):
    number_of_clusters = df['cluster'].max() + 1
    seed_list = []
    for i in range(number_of_clusters):
        filtered_df = df[df['cluster'].isin([i])]
        # todo insert for loop to work with inf columns
        mean = filtered_df.mean()
        mean_x = mean[0]
        mean_y = mean[1]
        seed_list.append([mean[0], mean[1]])
        if seed_list == old_seed_list:
            global clustering_done
            clustering_done = True
        else:
            global iterations_of_clustering
            iterations_of_clustering += 1
    return seed_list

# param everything needed for the csv
# creates the csv needed for handin
def create_output_csv(number_of_clusters, cluster_list: pd.DataFrame, number_of_iterations, rows, columns, df: pd.DataFrame):
    path = "output.csv"
    with open(path, "w", newline="\n") as file:
        writer = csv.writer(file, delimiter=";", dialect="excel")
        writer.writerow([number_of_clusters])
        for point in cluster_list:
            writer.writerow(point)

        writer.writerow([number_of_iterations])
        writer.writerow([rows, columns])
        #df.to_csv(path_or_buf=path, index=False,  sep = ";", header = False)
    f = open(path, "a")
    str = df.to_csv(index=False, sep=";", header=False, escapechar=None, line_terminator='\n')
    f.write(str)
    f.close()



# initially read the data
df = read_csv(CSV_PATH)

# set the dimensions and parameters todo: read this form file
number_of_clusters = 3
rows = 15
columns = 2
# set some vars
iterations_of_clustering = 0
clustering_done = False

# create x random points
seed_points = random_indices(rows, number_of_clusters)


# get values of the x random points in a seed list
seed_values = get_values_of_points(df, seed_points)



# assign the data to clusters and center the seeds in the clsuters
# while not done cluster it

while True:
    if clustering_done:
        print(iterations_of_clustering)
        print(df)
        create_output_csv(number_of_clusters, seed_values, iterations_of_clustering, rows, columns, df)
        break
    else:
        df = assign_to_cluster(seed_values, df)
        seed_values = center_seeds_in_clusters(df, seed_values)

