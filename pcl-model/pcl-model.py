import csv


class Room:

    def __init__(self, room_number, floor, room_type):

        self.__room_number = room_number
        self.__floor = floor
        self.__type = room_type
        self.__direct_neighbor = dict()
        self.__indirect_neighbor = dict()

    def get_floor(self):
        return self.__floor

    def get_type(self):
        return self.__type

    def get_neighbors(self):
        return {"direct": self.__direct_neighbor,
                "indirect": self.__indirect_neighbor}

    def add_direct_neighbor(self, neighbor):
        self.__direct_neighbor[str(neighbor)] = neighbor

    def add_indirect_neighbor(self, neighbor):
        self.__indirect_neighbor[str(neighbor)] = neighbor

    def remove_neighbor(self, neighbor):
        self.__direct_neighbor.pop(str(neighbor), None)
        self.__indirect_neighbor.pop(str(neighbor), None)

    def is_direct_neighbor(self, neighbor):
        return self.__direct_neighbor.get(str(neighbor), None)

    def get_neighbor(self, neighbor):
        direct = self.__direct_neighbor.get(str(neighbor), None)
        if direct is None:
            return self.__indirect_neighbor.get(str(neighbor), None)
        return direct

    def __str__(self):
        return self.__room_number


class Building:

    def __init__(self):
        self.floor = dict()
        self.__total_room = 0

    def total_floor(self):
        return len(self.floor)

    def total_room_numbers(self):
        return self.__total_room

    def get_room_numbers(self, floor):
        return len(self.floor[floor])

    def build(self, file_name):

        rooms = dict()

        with open(file_name, 'r') as building_csv:
            building_info = csv.reader(building_csv, delimiter=',')
            row_counter = -1

            for line in building_info:
                row_counter += 1
                if row_counter == 0:
                    continue
                rooms[line[0]] = Room(line[0], line[1], line[2])
                if line[1] not in self.floor.keys():
                    self.floor[line[1]] = dict()
                self.floor[line[1]][line[0]] = rooms[line[0]]

        self.__total_room = row_counter

        print("Found %i rooms in %s." % (row_counter, file_name))
        print("Building the model, please wait.")

        with open(file_name, 'r') as building_csv:
            building_info = csv.reader(building_csv, delimiter=',')
            row_counter = -1

            for line in building_info:
                row_counter += 1
                if row_counter == 0:
                    continue

                neighbor_info = line[4:]
                direct_link = True
                current = self.floor[line[1]][line[0]]

                for neighbor in neighbor_info:
                    if len(neighbor) == 0:
                        if direct_link:
                            direct_link = False
                            continue
                        else:
                            break
                    if direct_link:
                        current.add_direct_neighbor(rooms[neighbor])
                        rooms[neighbor].add_direct_neighbor(current)
                    else:
                        current.add_indirect_neighbor(rooms[neighbor])
                        rooms[neighbor].add_indirect_neighbor(current)

        print("Model for %s successfully built." % file_name)


if __name__ == "__main__":
    building_1 = Building()
    building_1.build("building-1-room-info.csv")
    # print(building_1.total_floor())
    # print(building_1.total_room_numbers())
    # print(building_1.floor["Outside"]["Outside"].get_neighbors()["direct"].keys())
    building_5 = Building()
    building_5.build("building-5-room-info.csv")
    # print(building_5.total_floor())
    # print(building_5.total_room_numbers())
    # print(building_5.floor["Outside"]["Outside"].get_neighbors()["direct"].keys())
