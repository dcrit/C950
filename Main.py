# Author: Daniel Crites
# WGU Student ID:002152169
# NHP2 — NHP2 TASK 1: WGUPS ROUTING PROGRAM

import csv
import datetime
import Truck

from HashTable import ChainingHashTable
from Package import Package


# Reading address csv
def address_list():
    with open('CSV_FILES/WGUPS_Address_Table.csv', encoding="utf-8-sig") as csv_file_address:
        csv_address = csv.reader(csv_file_address)
        csv_address = list(csv_address)
    return csv_address


# Reading package csv
def package_list():
    with open('CSV_FILES/WGUPS_Package_File.csv', encoding='utf-8-sig') as csv_file_package:
        csv_package = csv.reader(csv_file_package)
        csv_package = list(csv_package)
    return csv_package


# Reading distance csv
def distance_list():
    with open('CSV_FILES/WGUPS_Distance_Table.csv', encoding="utf-8-sig") as csv_file_distance:
        csv_distance = csv.reader(csv_file_distance)
        csv_distance = list(csv_distance)
    return csv_distance


# Creating hash object
myHash = ChainingHashTable()


# Loading packages method
def loadPackageData(csvFile):
    PO = package_list()
    test = Package
    for package in PO:
        ID = int(package[0])
        address = package[1]
        city = package[2]
        state = package[3]
        zip = package[4]
        deadline = package[5]
        weight = package[6]
        package[7] = "Not Delivered"
        package = package
        # Inserting Package ID and Package Info in a hash table
        myHash.insert(ID, package)


# Reading CSV Package file with load package method
loadPackageData('CSV_FILES/WGUPS_Package_File.csv')


# Designating packages to trucks
truck1 = [1, 2, 4, 5, 7, 8, 10, 11, 12, 21, 22, 23, 24, 26, 27, 29]
truck2 = [3, 18, 36, 38, 13, 14, 15, 16, 17, 19, 20, 30, 31, 33, 34, 35]
truck3 = [6, 25, 28, 32, 37, 39, 40, 9]

# Loading trucks
loadTruck1 = Truck.Truck(16, 18, 1, truck1, 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
loadTruck2 = Truck.Truck(16, 18, 2, truck2, 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
loadTruck3 = Truck.Truck(16, 18, 3, truck3, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

# Total mileage variable
total_mileage = 0.0

# Delivery Process method
def delivery_process(truck):
    truck_mileage = 0.0
    current_address = truck.address
    hub_address = "4001 South 700 East"
    index_for_current_position = 0

    list_of_package_info = []
    column_distant_list = []
    package_keys = []
    list_of_delivery_addresses = []
    list_of_all_addresses = []


    # Checking load of truck, then adding packages to lists
    for packageID in truck.packages:
        package_list = myHash.search(packageID)
        package_keys.append(int(package_list[0]))
        list_of_package_info.append(package_list)
        list_of_delivery_addresses.append(package_list[1])

    print("List keys ", package_keys)
    # Adding all addresses to a list
    for col in address_list():
        list_of_all_addresses.append(col[1])

    # Getting the index of the current address
    for index in list_of_all_addresses:
        if index == current_address:
            index_for_current_position = list_of_all_addresses.index(index)

    # Getting indexes of packages from all addresses
    indexes_of_packages = [list_of_all_addresses.index(c) for c in list_of_delivery_addresses]

    test_list = indexes_of_packages[:]
    print("TEst List ", test_list)
    print("Test list length ", len(test_list))

    # Packages are being delivered
    count = 0
    while len(indexes_of_packages) > 0:

        count += 1
        print("Indexes of packages not sorted ", indexes_of_packages)
        print("Index position ", index_for_current_position)
        # Reading Distance CSV
        csv_distance = distance_list()

        # Adding row from current position index
        row_distant_list = csv_distance[index_for_current_position]

        # Adding column from current position index
        for column in csv_distance:
            column_distant_list.append(column[index_for_current_position])

        # Removing extra zero
        column_distant_list.remove('0')

        # Extending row_distant_list list with column_distant_list
        row_distant_list.extend(column_distant_list)

        # Removing empty spaces and moving data to 'cleaned list'
        cleaned_list = [ele for ele in row_distant_list if ele.strip()]

        # Converting str list to float
        cleaned_list = [float(ele) for ele in cleaned_list]
        print("Cleaned List = ", cleaned_list)

        # Getting mileage distances for packages on route
        mileage_list = [cleaned_list[i] for i in indexes_of_packages]
        print("Mileage List = ", mileage_list)

        # Find the nearest route by using the min function
        shortest_route = min(mileage_list)
        print("Shortest route = ", shortest_route)
        shortest_route_index = mileage_list.index(min(mileage_list))
        print("Shortest route index ", shortest_route_index)

        duplicates_on_distance_cleaned_list = find_indices(cleaned_list, shortest_route)
        print("Dups on cleaned list = ", duplicates_on_distance_cleaned_list)
        # Counting duplicate distance on next route
        duplicate_distance_on_route = mileage_list.count(shortest_route)
        boo = find_indices(mileage_list, shortest_route)
        print("Dups on mileage list ", duplicate_distance_on_route)

        index_taker = 0

        # Working hererer!!!!!!!!!!!!!!!!!!
        for r in cleaned_list:

            if r == shortest_route and duplicate_distance_on_route == 1 and len(duplicates_on_distance_cleaned_list) == 1:
                x = test_list.index(cleaned_list.index(shortest_route))
                print("X = ", x)
                y = int(package_keys[x])
                print("Y = ", y)
                key_id = myHash.search(y)
                print("Key ID = ", key_id)
                key_id[7] = "Delivered"
                myHash.insert(y, key_id)
                print("Status ", myHash.search(y))
                # Adding mileage to total mileage
                truck_mileage += shortest_route
                index_for_current_position = duplicates_on_distance_cleaned_list[0]
                print("Shortest route ", shortest_route)
                print("Total Mileage ", truck_mileage)
                p = int(duplicates_on_distance_cleaned_list[0])
                indexes_of_packages.remove(p)

            # Checking if duplicates on cleaned list
            if r == shortest_route and duplicate_distance_on_route == 1 and len(duplicates_on_distance_cleaned_list) > 1:
                print("yoooo")
                for s in test_list:
                    for f in duplicates_on_distance_cleaned_list:
                        if s == f:
                            t = test_list.index(s)
                            id = package_keys[t]
                            key_id = myHash.search(id)
                            if key_id[7] == "Not Delivered":
                                print("Key Id ", key_id)
                                key_id[7] = "Delivered"
                                print("status ", myHash.search(id))
                                print("Total Mileage ", truck_mileage)
                                index_for_current_position = f
                                truck_mileage += shortest_route
                                print("Shorest route ", shortest_route)
                                indexes_of_packages.remove(f)

            # Checking if dups are on current route
            if r == shortest_route and duplicate_distance_on_route > 1 and len(duplicates_on_distance_cleaned_list) == 1:
                print("??????????????????????????????????")
                truck_mileage += shortest_route
                print("Shorest route ", shortest_route)
                print("Total Mileage ", truck_mileage)
                print("dups on clean ", duplicates_on_distance_cleaned_list)
                print("Dups on route BOOOOOOOOOOOO ", boo)
                rat = int(duplicates_on_distance_cleaned_list[0])
                t = []
                print("RATT ",  rat)
                for h in test_list:
                    if h == rat:
                        stuff = find_indices(test_list, h)
                        print("Stuff ",  stuff)
                        t = [package_keys[i] for i in stuff]
                        print("TTTtttt ", t)
                for g in t:
                    print("g", g)
                    id = g
                    key_id = myHash.search(id)
                    print("key id ", key_id)
                    key_id[7] = "Delivered"
                    print("key id ", key_id)
                indexes_of_packages.remove(rat)
                hey = int(duplicates_on_distance_cleaned_list[0])
                index_for_current_position = hey

            if r == shortest_route and duplicate_distance_on_route > 1 and len(duplicates_on_distance_cleaned_list) > 1:
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& ")

        print("package keys ", package_keys)
        print("test list ", test_list)
        print("test list length ", len(test_list))
        print("index of current postion ", index_for_current_position)
        print("Pacakgae indexes ", indexes_of_packages)

        # Finding the index of the next route
        # for item in cleaned_list:
        #     if item == shortest_route:
        #         index_for_current_position = cleaned_list.index(item)
        #         print("Index of next position ", index_for_current_position)

        # Returning to hub on last delivery
        if len(indexes_of_packages) == 0:
                print("Last stop index ", index_for_current_position)
                print("To hub mileage ", mileage_list[0])
                truck_mileage += mileage_list[0]

        # Removing delivered package from truck
        # indexes_of_packages = remove_delivered_package(indexes_of_packages, index_for_current_position)

        # Clearing lists
        row_distant_list.clear()
        column_distant_list.clear()
        cleaned_list.clear()
        mileage_list.clear()

        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("fdafsadfsdf ", test_list)
    print("Truck mileage ", truck_mileage)
    return truck_mileage


def remove_delivered_package(list, item):
    res = []
    for t in list:
        if t != item:
            res.append(t)
    return res

def find_indices(l, value):
    return [
        index for index, item in enumerate(l)
        if item == value
    ]


def updating_packages(list, position, keys):
    for a in list:
        key_id = []
        if a == position:
            x = list.index(a)
            print("X = ", x)
            y = int(keys[x])
            print("Y = ", y)
            key_id = myHash.search(y)
            print("Key ID = ", key_id)
            key_id[7] = "Delivered"
            myHash.insert(y, key_id)

total_mileage += delivery_process(loadTruck1)
# total_mileage += delivery_process(loadTruck2)
total_mileage += delivery_process(loadTruck3)
print("Total Mileage ", total_mileage)
print("Truck 1 ")
print("Checking packages 1 ", myHash.search(1))
print("Checking packages 2 ", myHash.search(2))
print("Checking packages 4 ", myHash.search(4))
print("Checking packages 5 ", myHash.search(5))
print("Checking packages 7 ", myHash.search(7))
print("Checking packages 8 ", myHash.search(8))
print("Checking packages 10 ", myHash.search(10))
print("Checking packages 11 ", myHash.search(11))
print("Checking packages 12 ", myHash.search(12))
print("Checking packages 21 ", myHash.search(21))
print("Checking packages 22 ", myHash.search(22))
print("Checking packages 23 ", myHash.search(23))
print("Checking packages 24 ", myHash.search(24))
print("Checking packages 26 ", myHash.search(26))
print("Checking packages 27 ", myHash.search(27))
print("Checking packages 29 ", myHash.search(29))
print("\n")
print("Truck 2")
print("Total Mileage ", total_mileage)
print("Checking packages 3 ", myHash.search(3))
print("Checking packages 18 ", myHash.search(18))
print("Checking packages 36 ", myHash.search(36))
print("Checking packages 38 ", myHash.search(38))
print("Checking packages 13 ", myHash.search(13))
print("Checking packages 14 ", myHash.search(14))
print("Checking packages 15 ", myHash.search(15))
print("Checking packages 16 ", myHash.search(16))
print("Checking packages 17 ", myHash.search(17))
print("Checking packages 19 ", myHash.search(19))
print("Checking packages 20 ", myHash.search(20))
print("Checking packages 30 ", myHash.search(30))
print("Checking packages 31 ", myHash.search(31))
print("Checking packages 33 ", myHash.search(33))
print("Checking packages 34 ", myHash.search(34))
print("Checking packages 35 ", myHash.search(35))
print("\n")
print("Truck 3")
print("Total Mileage ", total_mileage)
print("Checking packages 6 ", myHash.search(6))
print("Checking packages 25 ", myHash.search(25))
print("Checking packages 28 ", myHash.search(28))
print("Checking packages 32 ", myHash.search(32))
print("Checking packages 37 ", myHash.search(37))
print("Checking packages 39 ", myHash.search(39))
print("Checking packages 40 ", myHash.search(40))
print("Checking packages 9 ", myHash.search(9))