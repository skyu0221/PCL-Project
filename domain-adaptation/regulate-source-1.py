import csv
import os


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
                                   "601-co2", "601-damper", "601-occupant",]]

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
            merge_line = []
            counter = [0.] * 4
            count_number = [0] * 4

            for row in data:
                merge_line.append(row)
                for i in range(4):
                    if float(row[i * 3 + 3]) == 0:
                        count_number[i] += 1
                        counter[i] += float(row[i * 3 + 1])

            for i in range(len(counter)):
                counter[i] //= count_number[i]

            for line in merge_line:
                for i in range(4):
                    line[i * 3 + 1] = str(max(float(line[i * 3 + 1]) - counter[i], 0))
                output.writerow(line)


if __name__ == "__main__":
    regulate()
