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
    status = "At Hub"
    delivery_time = datetime.timedelta(hours=8)
    for package in PO:
        ID = int(package[0])
        address = package[1]
        city = package[2]
        state = package[3]
        zip = package[4]
        deadline = package[5]
        weight = package[6]
        notes = package[7]

        # Creating an Package object to put in hash table
        package_object = Package(ID, address, city, state, zip, deadline, weight, notes, status, delivery_time)

        # Inserting Package ID and Package Info in a hash table
        myHash.insert(ID, package_object)


# Reading CSV Package file with load package method
loadPackageData('CSV_FILES/WGUPS_Package_File.csv')

# Designating packages to trucks
truck1 = [1, 2, 4, 5, 7, 8, 10, 11, 12, 21, 22, 23, 24, 26, 27, 29]
truck2 = [3, 18, 36, 38, 13, 14, 15, 16, 17, 19, 20, 30, 31, 33, 34, 35]
truck3 = [6, 25, 28, 32, 37, 39, 40, 9]

# Loading trucks
loadTruck1 = Truck.Truck(16, 18, 1, truck1, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                         datetime.timedelta(hours=8))
loadTruck2 = Truck.Truck(16, 18, 2, truck2, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                         datetime.timedelta(hours=8))
loadTruck3 = Truck.Truck(16, 18, 3, truck3, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20),
                         datetime.timedelta(hours=8))

# Total mileage variable
total_mileage = 0.0


# Delivery Process method
def delivery_process(truck):
    truck_mileage = 0.0
    time = truck.depart_time
    print("Helllo world ", time)
    current_address = truck.address
    index_for_current_position = 0

    column_distant_list = []
    package_keys = []
    list_of_delivery_addresses = []
    list_of_all_addresses = []
    new_list = []

    # Checking load of truck, then adding packages to lists
    for packageID in truck.packages:
        # Adding Keys to a list
        package_keys.append(packageID)
        # Adding all delivery addresses to a list
        r = str(myHash.search(packageID))
        k = r.split(", ")
        list_of_delivery_addresses.append(k[1])

    # Adding all addresses to a list
    for col in address_list():
        list_of_all_addresses.append(col[1])

    # Getting the index of the current address
    for index in list_of_all_addresses:
        if index == current_address:
            index_for_current_position = list_of_all_addresses.index(index)

    # Getting indexes of packages from all addresses
    indexes_of_packages = [list_of_all_addresses.index(c) for c in list_of_delivery_addresses]

    # Creating a compartive list
    test_list = indexes_of_packages[:]

    # Updating package to "En Route" and converting to lists
    for s in truck.packages:
        here = str(myHash.search(s))
        here = here.split(", ")
        here[8] = "En route"
        myHash.insert(s, here)
    count = 0
    # Packages are being delivered
    while len(indexes_of_packages) > 0:
        count += 1
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

        # Getting mileage distances for packages on route
        mileage_list = [cleaned_list[i] for i in indexes_of_packages]

        # Find the nearest route by using the min function
        shortest_route = min(mileage_list)

        # Checking duplicate values on cleaned list
        duplicates_on_distance_cleaned_list = find_indices(cleaned_list, shortest_route)

        # Counting duplicate distance on next route
        duplicate_distance_on_route = mileage_list.count(shortest_route)

        # Updating packages when they are being delivered
        for r in cleaned_list:
            # Handles no duplicates distances and then updates package
            if r == shortest_route and duplicate_distance_on_route == 1 and len(
                    duplicates_on_distance_cleaned_list) == 1:
                print("No Dups")
                x = test_list.index(cleaned_list.index(shortest_route))
                y = int(package_keys[x])
                key_id = myHash.search(y)
                print("Key ID = ", key_id)
                key_id[8] = "Delivered"
                deliverytime = (shortest_route / 18) * 60 * 60
                dts = datetime.timedelta(seconds=deliverytime)
                time = time + dts
                key_id[9] = str(time)
                myHash.insert(y, key_id)
                print("Status ", myHash.search(y))
                # Adding mileage to total mileage
                truck_mileage += shortest_route
                index_for_current_position = duplicates_on_distance_cleaned_list[0]
                p = int(duplicates_on_distance_cleaned_list[0])
                indexes_of_packages.remove(p)

            # Handles duplicate values on clean list and updates packages
            if r == shortest_route and duplicate_distance_on_route == 1 and len(
                    duplicates_on_distance_cleaned_list) > 1:
                print("Dups on duplicates ")
                for s in test_list:
                    for f in duplicates_on_distance_cleaned_list:
                        if s == f:
                            t = test_list.index(s)
                            id = package_keys[t]
                            key_id = myHash.search(id)
                            if key_id[8] == "En route":
                                print("Key Id ", key_id)
                                key_id[8] = "Delivered"
                                deliverytime = (shortest_route / 18) * 60 * 60
                                dts = datetime.timedelta(seconds=deliverytime)
                                time = time + dts
                                key_id[9] = str(time)
                                myHash.insert(id, key_id)
                                index_for_current_position = f
                                truck_mileage += shortest_route
                                indexes_of_packages.remove(f)

            # Handles duplicate values on route and updates package
            if r == shortest_route and duplicate_distance_on_route > 1 and len(
                    duplicates_on_distance_cleaned_list) == 1:
                print("Dups on route")
                truck_mileage += shortest_route
                rat = int(duplicates_on_distance_cleaned_list[0])
                t = []
                for h in test_list:
                    if h == rat:
                        stuff = find_indices(test_list, h)
                        t = [package_keys[i] for i in stuff]
                for g in t:
                    print("g", g)
                    id = g
                    key_id = myHash.search(id)
                    key_id[8] = "Delivered"
                    deliverytime = (shortest_route / 18) * 60 * 60
                    dts = datetime.timedelta(seconds=deliverytime)
                    time = time + dts
                    key_id[9] = str(time)
                    myHash.insert(id, key_id)
                    print("key id ", myHash.search(id))
                # indexes_of_packages.remove(rat)
                indexes_of_packages = [x for x in indexes_of_packages if x != rat]
                hey = int(duplicates_on_distance_cleaned_list[0])
                index_for_current_position = hey

            # Handles duplicate values on route and cleaned list
            if r == shortest_route and duplicate_distance_on_route > 1 and len(duplicates_on_distance_cleaned_list) > 1:
                tut = duplicates_on_distance_cleaned_list[0]
                print("Dups on route and cleaned list")
                for s in test_list:
                    if s == tut:
                        key = package_keys[test_list.index(s)]
                        key_id = myHash.search(key)
                        # key_id = key_id.split(", ")
                        if key_id[8] == "En route":
                            key_id[8] = "Delivered"
                            deliverytime = (shortest_route / 18) * 60 * 60
                            dts = datetime.timedelta(seconds=deliverytime)
                            time = time + dts
                            key_id[9] = str(time)
                            myHash.insert(key, key_id)
                            indexes_of_packages.remove(tut)
                            index_for_current_position = tut

        # Returning to hub on last delivery
        if len(indexes_of_packages) == 0:
            print("To hub mileage ", mileage_list[0])
            deliverytime = (mileage_list[0] / 18) * 60 * 60
            dts = datetime.timedelta(seconds=deliverytime)
            time = time + dts
            print("Final Time ", time)
            truck_mileage += mileage_list[0]
            # Updating final times
            if truck == loadTruck1:
                loadTruck1.return_time = time
                print("Truck 1 ", loadTruck1.return_time)
            if truck == loadTruck2:
                loadTruck2.return_time = time
                print("Truck 1 ", loadTruck2.return_time)
                loadTruck3.depart_time = min(loadTruck1.return_time, loadTruck2.return_time)
                print("RERERE ", loadTruck3.depart_time)
            if truck == loadTruck3:
                loadTruck3.return_time = time
                print("Truck 3 ", loadTruck3.return_time)
                # loadTruck3.depart_time = loadTruck1.return_time
                # loadTruck3.depart_time = min(loadTruck1.return_time, loadTruck2.return_time)
                print("Truck 3")

        # Clearing lists
        row_distant_list.clear()
        column_distant_list.clear()
        cleaned_list.clear()
        mileage_list.clear()

        print(
            "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Test List ", test_list)
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


total_mileage += delivery_process(loadTruck1)
total_mileage += delivery_process(loadTruck2)
total_mileage += delivery_process(loadTruck3)


def ui():
    print("Please choose from the following options:\n"
          "1. Show all package info \n"
          "2. Total Mileage \n"
          "3. Search for a package by time \n"
          "4. Search for all packages by time \n"
          "5. Exit Program \n")
    user_input = int(input("Input number: "))
    print("User Input ", user_input)
    if user_input == 1:
        pack = 1
        while pack < 41:
            print(myHash.search(pack))
            pack += 1
    if user_input == 2:
        print("Total Mileage: ", total_mileage)
    if user_input == 3:
        print("Please enter a time using the following format: '8:00:00' ")
        time = input("Enter a time: ")
        t = myHash.search(1)
        print(t[2])


ui()

def all_pacakage_info():
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
