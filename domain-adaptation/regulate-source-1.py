import csv
import os
import numpy as np
from sklearn.linear_model import LinearRegression


def merge_file():

    with open("./source-1/df_co2.csv", 'r') as merge_1:
        with open("./source-1/df_vav.csv", 'r') as merge_2:
            with open("./source-1/df_occ_aligned.csv", 'r') as merge_3:
                with open("./source-1/merged-source.csv", 'w', newline="") as result:

                    file_1 = csv.reader(merge_1, delimiter=',')
                    file_2 = csv.reader(merge_2, delimiter=',')
                    file_3 = csv.reader(merge_3, delimiter=',')
                    output = csv.writer(result, delimiter=',')

                    files = (file_1, file_2, file_3)
                    for file in files:
                        next(file)

                    merge_line = [["datetime",
                                   "508-co2", "508-damper", "508-occupant",
                                   "604-co2", "604-damper", "604-occupant",
                                   "511-co2", "511-damper", "511-occupant",
                                   "601-co2", "601-damper", "601-occupant"]]

                    for i in range(len(files)):
                        row_number = 0
                        for row in files[i]:
                            row_number += 1

                            if row_number == len(merge_line):
                                merge_line.append([""] * 13)
                                merge_line[row_number][0] = row[0]
                            merge_line[row_number][10 + i] = row[1]
                            merge_line[row_number][4 + i] = row[2]
                            merge_line[row_number][1 + i] = row[3]
                            merge_line[row_number][7 + i] = row[4]

                    for line in merge_line:
                        if '' not in line:
                            output.writerow(line)


def regulate():
    if not os.path.exists("./source-1/merged-source.csv"):
        merge_file()

    with open("./source-1/merged-source.csv", 'r') as in_file:
        with open("./source-1/regulate-source.csv", 'w', newline="") as result:

            data = csv.reader(in_file, delimiter=',')
            output = csv.writer(result, delimiter=',')

            output.writerow(next(data))

            all_data = []
            rooms = [[[], []], [[], []], [[], []], [[], []]]
            process = [[[], []], [[], []], [[], []], [[], []]]
            value = [[], [], [], []]
            coef = [[], [], [], []]
            q = [[], [], [], []]

            for row in data:
                all_data.append(row)
                for i in range(len(rooms)):
                    rooms[i][0].append(float(row[i * 3 + 1]))
                    rooms[i][1].append(float(row[i * 3 + 2]))

            rooms = np.asarray(rooms)

            for room in range(len(rooms)):
                for sensor in range(2):
                    process[room][sensor].append(0.0)
                    for data in range(1, len(rooms[room][sensor])):
                        process[room][sensor].append(rooms[room][sensor][data] - np.mean(rooms[room][sensor][:data]))

            for room in range(len(rooms)):
                process_value = [process[room][1][:-1]]
                process_value = np.concatenate((process_value, [process[room][0][1:]]))
                value[room] = [rooms[room][1][:-1]]
                value[room] = np.concatenate((value[room], [rooms[room][0][1:]]))

                regression = LinearRegression()
                regression.fit(np.transpose(process_value), process[room][0][:-1])
                coef[room] = regression.coef_

            for room in range(len(rooms)):
                q[room] = rooms[room][0][1:] - (np.transpose(coef[room] * np.transpose(value[room])).sum(axis=0))

            for i in range(len(all_data) - 1):
                for room in range(len(rooms)):
                    all_data[i][room * 3 + 1] = q[room][i]
                output.writerow(all_data[i])


def save_for_adaptation():
    if not os.path.exists("./source-1/regulate-source.csv"):
        regulate()

    with open("./source-1/regulate-source.csv", 'r') as in_file:
        with open("./source1.csv", 'w', newline="") as result:

            data = csv.reader(in_file, delimiter=',')
            output = csv.writer(result, delimiter=',')

            next(data)
            output.writerow(["CO2", "Damper", "Occupant"])

            for row in data:
                for i in range(4):
                    output.writerow(row[i * 3 + 1:i * 3 + 4])


if __name__ == "__main__":
    save_for_adaptation()
