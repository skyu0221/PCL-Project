import numpy as np
import csv

DATA_SET_CSV = ["source1.csv", "target1.csv"]
MICRO = 1

def main():

    dataset = []
    dataset_directory = []
    # number of feature, number of rows
    dataset_size = []

    for dataset_csv in DATA_SET_CSV:
        with open(dataset_csv, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            directory = next(data)
            dataset_directory.append(directory)
            current_data = [[] for _ in range(len(directory))]
            counter = 0
            for row in data:
                counter += 1
                for i in range(len(row)):
                    try:
                        current_data[i].append(float(row[i]))
                    except ValueError:
                        current_data[i].append(row[i])

            dataset.append(current_data)
            dataset_size.append([len(directory), counter])

    dataset = np.array(dataset)
    dataset_size = np.array(dataset_size)
    total_m = int(np.sum(dataset_size[:, 1]))
    total_p = int(np.sum(dataset_size[:, 0]) - len(DATA_SET_CSV))

    cap_x = [[] for _ in range(len(DATA_SET_CSV))]
    cap_v = [[] for _ in range(len(DATA_SET_CSV))]
    cap_w = [np.array([]) for _ in range(len(DATA_SET_CSV))]
    cap_d = [np.array([]) for _ in range(len(DATA_SET_CSV))]
    cap_l = [np.array([]) for _ in range(len(DATA_SET_CSV))]

    for i in range(len(cap_x)):
        cap_x[i] = dataset[i][:-1].astype(np.float)
    for i in range(len(cap_v)):
        cap_v[i] = dataset[i][-1]

    # Similarity matrix
    cap_w_s = np.zeros((total_m, total_m))
    for i in range(total_m):
        for j in range(total_m):
            a = 0
            b = 0
            while i >= dataset_size[a][1]:
                a += 1
                i -= dataset_size[a][1]
            while j >= dataset_size[b][1]:
                b += 1
                j -= dataset_size[b][1]
            if cap_v[a][i] != "None" and cap_v[a][i] == cap_v[b][j]:
                cap_w_s[i][j] = 1.0

    # Similarity diagonal row sum matrix
    cap_d_s = np.zeros((total_m, total_m))
    for i in range(total_m):
        cap_d_s[i][i] = np.sum(cap_w_s[i, :])

    # Similarity combinatorial Laplacian matrix
    cap_l_s = cap_d_s - cap_w_s

    # dissimilarity matrix
    cap_w_d = np.zeros((total_m, total_m))
    for i in range(total_m):
        for j in range(total_m):
            a = 0
            b = 0
            while i >= dataset_size[a][1]:
                a += 1
                i -= dataset_size[a][1]
            while j >= dataset_size[b][1]:
                b += 1
                j -= dataset_size[b][1]
            if cap_v[a][i] != "None" and cap_v[b][j] != "None" and cap_v[a][i] != cap_v[b][j]:
                cap_w_d[i][j] = 1.0

    # Dissimilarity diagonal row sum matrix
    cap_d_d = np.zeros((total_m, total_m))
    for i in range(total_m):
        cap_d_d[i][i] = np.sum(cap_w_d[i, :])

    # Dissimilarity combinatorial Laplacian matrix
    cap_l_d = cap_d_d - cap_w_d

    for k in range(len(cap_w)):

        # W_k
        cap_w[k] = np.zeros((dataset_size[k][1], dataset_size[k][1]))
        for i in range(dataset_size[k][1]):
            for j in range(dataset_size[k][1]):
                cap_w[k][i][j] = np.exp(-np.linalg.norm(np.array(cap_x[k][:, i]) - np.array(cap_x[k][:, j])))

        # D_k
        cap_d[k] = np.zeros((dataset_size[k][1], dataset_size[k][1]))
        for i in range(dataset_size[k][1]):
            cap_d[k][i][i] = np.sum(cap_w[k][i, :])

        # L_k
        cap_l[k] = cap_d[k] - cap_w[k]

    # L
    cap_ll = np.zeros((total_m, total_m))
    current = 0
    for k in range(len(DATA_SET_CSV)):
        cap_ll[current:current + dataset_size[k][1],
               current:current + dataset_size[k][1]] = cap_l[k]
        current += dataset_size[k][1]

    # Z
    cap_z = np.zeros((total_p, total_m))
    current_row = 0
    current_column = 0
    for k in range(len(DATA_SET_CSV)):
        cap_z[current_row:current_row + dataset_size[k][0] - 1,
              current_column:current_column + dataset_size[k][1]] = cap_x[k]
        current_row += dataset_size[k][0] - 1
        current_column += dataset_size[k][1]
    # Compute f
    cap_a = np.dot(cap_z, MICRO * cap_ll + cap_l_s)
    cap_a = np.dot(cap_a, np.transpose(cap_z))
    cap_a_right = np.dot(cap_z, cap_l_d)
    cap_a_right = np.dot(cap_a_right, np.transpose(cap_z))
    cap_a = np.dot(np.linalg.inv(cap_a_right), cap_a)

    eigenvalue, gamma = np.linalg.eig(cap_a)
    combine = np.concatenate((eigenvalue.reshape((1, eigenvalue.size)), gamma))
    f = combine[:, np.argsort(combine[0])][1:]


if __name__ == "__main__":
    main()
