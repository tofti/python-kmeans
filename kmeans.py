import ast
import csv
import sys
import math
import os
import random
import itertools
import matplotlib.pyplot as mplpyplot
import time
import datetime

# TODO add distortion computation
# TODO add additional functions for centroid init'


def get_header_name_to_idx_maps(headers):
    name_to_idx = {}
    idx_to_name = {}
    for i in range(0, len(headers)):
        name_to_idx[headers[i]] = i
        idx_to_name[i] = headers[i]
    return idx_to_name, name_to_idx


def replace_str_with_float(list_of_list):
    for l in list_of_list:
        for idx in range(0, len(l)):
            try:
                f = string_to_float(l[idx])
                l[idx] = f
            except ValueError:
                pass


def load_csv_to_header_data(filename):
    path = os.path.normpath(os.getcwd() + filename)
    fs = csv.reader(open(path))
    all_row = []
    for r in fs:
        all_row.append(r)

    headers = all_row[0]
    idx_to_name, name_to_idx = get_header_name_to_idx_maps(headers)

    data = {
        'header': headers,
        'rows': all_row[1:],
        'name_to_idx': name_to_idx,
        'idx_to_name': idx_to_name
    }

    replace_str_with_float(data['rows'])

    return data


def load_config(config_file):
    with open(config_file, 'r') as myfile:
        data = myfile.read().replace('\n', '')
    return ast.literal_eval(data)


def project_columns(data, columns_to_project):
    data_h = list(data['header'])
    data_r = list(data['rows'])

    all_cols = list(range(0, len(data_h)))

    columns_to_project_ix = [data['name_to_idx'][name] for name in columns_to_project]
    columns_to_remove = [cidx for cidx in all_cols if cidx not in columns_to_project_ix]

    for delc in sorted(columns_to_remove, reverse=True):
        del data_h[delc]
        for r in data_r:
            del r[delc]

    idx_to_name, name_to_idx = get_header_name_to_idx_maps(data_h)

    return {'header': data_h, 'rows': data_r,
            'name_to_idx': name_to_idx,
            'idx_to_name': idx_to_name}


def project_cluster_atts(datum, cluster_atts_idxs):
    return [datum[x] for x in cluster_atts_idxs]


def rand_init_centroids(data, k, cluster_atts_idxs):
    centroids = list(itertools.repeat(None, k))

    idxs = list(range(0, len(data)))

    for i in range(0, k):
        r = random.randint(0, len(idxs) - 1)
        del idxs[r]
        datum = data[r]
        centroids[i] = project_cluster_atts(datum, cluster_atts_idxs)
    return centroids


def string_to_float(v):
    return float(v)


def assignment_step(centroids, cluster_atts_idx, data_rows):
    cluster_assignment = {}
    for datum_idx in range(0, len(data_rows)):
        datum = data_rows[datum_idx]

        closest_centroid_idx = None
        closest_centroid_distance = None

        for centroid_idx in range(0, len(centroids)):
            centroid_datum = centroids[centroid_idx]

            distance = distance_between(datum, centroid_datum, cluster_atts_idx)

            if closest_centroid_distance is None or distance < closest_centroid_distance:
                closest_centroid_distance = distance
                closest_centroid_idx = centroid_idx

        if closest_centroid_idx not in cluster_assignment:
            cluster_assignment[closest_centroid_idx] = list()
        cluster_assignment[closest_centroid_idx].append(datum_idx)

    return cluster_assignment


def distance_between(datum, centroid_datum, cluster_atts_idxs):
    s = 0
    datum_comparable_atts = project_cluster_atts(datum, cluster_atts_idxs)
    for i in range(0, len(datum_comparable_atts)):
        centroid_datum_att_value = datum_comparable_atts[i]
        try:
            datum_att_value = centroid_datum[i]
        except Exception:
            pass  # TODO bugfix for empty cluster None centroid

        s += math.pow(abs(centroid_datum_att_value - datum_att_value), 2)

    return math.sqrt(s)


def update_centroids(data_rows, cluster_assignments, cluster_atts_idxs, k):
    centroids = list(itertools.repeat(None, k))

    num_of_atts = len(cluster_atts_idxs)

    for cluster_id in sorted(cluster_assignments):
        data_for_cluster_idxs = cluster_assignments[cluster_id]
        new_centroid = list(itertools.repeat(0.0, num_of_atts))

        num_in_cluster = len(data_for_cluster_idxs)

        for data_for_cluster_idx in data_for_cluster_idxs:
            datum = data_rows[data_for_cluster_idx]
            datum_comparable_atts = project_cluster_atts(datum, cluster_atts_idxs)
            for cluster_atts_idx_idx in range(0, num_of_atts):
                new_centroid[cluster_atts_idx_idx] += \
                    datum_comparable_atts[cluster_atts_idx_idx]

        for cluster_atts_idx_idx in range(0, num_of_atts):
            new_centroid[cluster_atts_idx_idx] /= num_in_cluster

        centroids[cluster_id] = new_centroid

    return centroids


image_seq = 0


def plot_cluster_assignments(cluster_assignments, centroids, data_rows, cluster_atts, cluster_atts_idxs, plot_config):
    colors = {0: 'Red', 1: 'Blue', 2: 'Green', 3: 'Purple'}

    plots_configs = plot_config['plots_configs']
    num_of_plots = len(plots_configs)

    fig, subplots = mplpyplot.subplots(1, num_of_plots)
    fig.set_size_inches(4*num_of_plots, 4, forward=True)

    for idx in range(0, len(plots_configs)):
        plot_atts = plots_configs[idx]['plot_atts']
        subplot = subplots[idx]
        for cluster_assignment in cluster_assignments:
            # cluster data - lookup first
            cluster_data = [data_rows[x] for x in cluster_assignments[cluster_assignment]]

            x_att = plot_atts[0]
            y_att = plot_atts[1]

            x_att_centroid_idx = cluster_atts.index(x_att)
            y_att_centroid_idx = cluster_atts.index(y_att)

            x_raw_data_idx = cluster_atts_idxs[x_att_centroid_idx]
            y_raw_data_idx = cluster_atts_idxs[y_att_centroid_idx]

            dataum_axis_x_data = [cluster_datum[x_raw_data_idx] for cluster_datum in cluster_data]
            dataum_axis_y_data = [cluster_datum[y_raw_data_idx] for cluster_datum in cluster_data]
            dataum_axis_x_data, dataum_axis_y_data = sort_for_plot(dataum_axis_x_data, dataum_axis_y_data)

            # subplot.set_aspect("equal")
            subplot.plot(dataum_axis_x_data, dataum_axis_y_data, marker='o', linestyle='', c=colors[cluster_assignment])
            # centroid
            centroid = centroids[cluster_assignment]
            centroid_axis_x_data = [centroid[x_att_centroid_idx]]
            centroid_axis_y_data = [centroid[y_att_centroid_idx]]

            subplot.plot(centroid_axis_x_data, centroid_axis_y_data, marker='+', linestyle='',
                         c=colors[cluster_assignment],
                         ms=20)

            subplot.set_title(x_att + ' / ' + y_att)
    fig.tight_layout()
    fig.show()
    global image_seq

    if 'output_file_prefix' in plot_config:
        fig.savefig(plot_config['output_file_prefix'] + str(image_seq) + ".png")
        image_seq += 1
    mplpyplot.close(fig)


def kmeans(data, k, cluster_atts, cluster_atts_idxs, plot_config):
    # select initial centroids
    data_rows = data['rows']

    centroids = rand_init_centroids(data_rows, k, cluster_atts_idxs)

    cluster_assignments = assignment_step(centroids, cluster_atts_idxs, data_rows)

    plot_cluster_assignments(cluster_assignments, centroids, data_rows,
                             cluster_atts, cluster_atts_idxs, plot_config)

    while True:
        centroids = update_centroids(data_rows, cluster_assignments, cluster_atts_idxs, k)
        next_cluster_assignments = assignment_step(centroids, cluster_atts_idxs, data_rows)
        if cluster_assignments == next_cluster_assignments:
            break
        cluster_assignments = next_cluster_assignments

        plot_cluster_assignments(cluster_assignments, centroids, data_rows,
                                 cluster_atts, cluster_atts_idxs, plot_config)

    plot_cluster_assignments(cluster_assignments, centroids, data_rows,
                             cluster_atts, cluster_atts_idxs, plot_config)

    return cluster_assignments, centroids


def sort_for_plot(x, y):
    return zip(*sorted(zip(x, y)))


def main():
    argv = sys.argv
    print("Command line args are {}: ".format(argv))

    config = load_config(argv[1])

    print(config)

    data = load_csv_to_header_data(config['data_file'])
    data = project_columns(data, config['data_project_columns'])
    print(data)

    k = config['k']
    cluster_atts = config['cluster_atts']
    cluster_atts_idxs = [data['name_to_idx'][x] for x in cluster_atts]

    plot_config = config['plot_config']

    final_cluster_assignments, final_centroids = kmeans(data, k, cluster_atts, cluster_atts_idxs, plot_config)

    data_rows = data['rows']

    plot_cluster_assignments(final_cluster_assignments, final_centroids,
                             data_rows, cluster_atts, cluster_atts_idxs,
                             plot_config)


if __name__ == "__main__": main()
