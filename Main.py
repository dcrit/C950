# Author: Daniel Crites
# WGU Student ID:002152169
# NHP2 — NHP2 TASK 1: WGUPS ROUTING PROGRAM

import csv
import datetime
import sys

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
    index_for_current_position = 0

    # Emtpy lists need for my delivery process
    column_distant_list = []
    package_keys = []
    list_of_delivery_addresses = []
    list_of_all_addresses = []
    indexes_of_packages = []
    cleaned_list = []
    mileage_list = []

    # Adding all addresses to a list
    for col in address_list():
        list_of_all_addresses.append(col[1])

    # Loading truck and status of packages
    for packageID in truck.packages:
        # Adding Keys to a list
        package_keys.append(packageID)
        # Adding all delivery addresses to a list
        mileage = str(myHash.search(packageID))
        package = mileage.split(", ")
        package[8] = "En route"
        myHash.insert(packageID, package)
        list_of_delivery_addresses.append(package[1])

    # Getting indexes of packages being delivered
    for index in list_of_delivery_addresses:
        for a in list_of_all_addresses:
            if index == a:
                indexes_of_packages.append(list_of_all_addresses.index(index))

    # Creating a comparative list
    comparative_list = indexes_of_packages[:]

    # Packages are being delivered
    while len(indexes_of_packages) > 0:

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

        # Removing empty spaces and converting list to float
        for cell in row_distant_list:
            if cell != "":
                cleaned_list.append(float(cell))

        # Getting mileage distances for packages on route
        for i in indexes_of_packages:
            mileage_list.append(cleaned_list[i])

        # Find the nearest route by using the min function
        shortest_route = min(mileage_list)

        # Checking duplicate values on cleaned list
        duplicates_on_distance_cleaned_list = find_indices(cleaned_list, shortest_route)

        # Counting duplicate distance on next route
        duplicate_distance_on_route = mileage_list.count(shortest_route)

        # Updating packages when they are being delivered
        for mileage in cleaned_list:
            # Handles no duplicates distances and then updates package
            if mileage == shortest_route and duplicate_distance_on_route == 1 and len(
                    duplicates_on_distance_cleaned_list) == 1:
                print("No Dups")
                # Adding mileage to total mileage
                truck_mileage += shortest_route
                # Finding package id from list of keys
                x = comparative_list.index(cleaned_list.index(shortest_route))
                y = int(package_keys[x])
                # Pulling package from hash table to update
                key_value = myHash.search(y)
                print("Key ID = ", key_value)
                # Checking status of package and updating
                if key_value[8] == "En route":
                    key_value[8] = "Delivered"
                    delivery_time = (shortest_route / 18) * 60 * 60
                    dts = datetime.timedelta(seconds=delivery_time)
                    time = time + dts
                    key_value[9] = str(time)
                    myHash.insert(y, key_value)
                    print("Status ", myHash.search(y))
                    index_for_current_position = duplicates_on_distance_cleaned_list[0]
                    p = int(duplicates_on_distance_cleaned_list[0])
                    indexes_of_packages.remove(p)
            # Handles duplicate values on clean list and updates packages
            if mileage == shortest_route and duplicate_distance_on_route == 1 and len(
                    duplicates_on_distance_cleaned_list) > 1:
                # Determining what duplicates need to be delivered and updating package
                for package_id in comparative_list:
                    for duplicate in duplicates_on_distance_cleaned_list:
                        if package_id == duplicate:
                            package_id = package_keys[comparative_list.index(package_id)]
                            key_value = myHash.search(package_id)
                            if key_value[8] == "En route":
                                print("Key Id ", key_value)
                                key_value[8] = "Delivered"
                                delivery_time = (shortest_route / 18) * 60 * 60
                                dts = datetime.timedelta(seconds=delivery_time)
                                time = time + dts
                                key_value[9] = str(time)
                                myHash.insert(package_id, key_value)
                                print(myHash.search(package_id))
                                index_for_current_position = duplicate
                                truck_mileage += shortest_route
                                indexes_of_packages.remove(duplicate)

            # Handles duplicate values on route and updates package
            if mileage == shortest_route and duplicate_distance_on_route > 1 and len(
                    duplicates_on_distance_cleaned_list) == 1:
                print("Dups on route")
                # Adding mileage to truck
                truck_mileage += shortest_route
                # Grabbing first duplicate on  cleaned list
                duplicate = int(duplicates_on_distance_cleaned_list[0])
                # Getting time for distance travel
                delivery_time = (shortest_route / 18) * 60 * 60
                dts = datetime.timedelta(seconds=delivery_time)
                time = time + dts
                indexes = []
                keys = []
                for package_id in comparative_list:
                    if package_id == duplicate:
                        indexes = find_indices(comparative_list, package_id)
                        print("Stuff ", indexes)
                for package_id in indexes:
                    keys.append(package_keys[package_id])
                # Checking package status and then updating package
                for key in keys:
                    package_id = key
                    key_value = myHash.search(package_id)
                    if key_value[8] == "En route":
                        key_value[8] = "Delivered"
                        key_value[9] = str(time)
                        myHash.insert(package_id, key_value)
                        print("key id ", myHash.search(package_id))
                # Removing delivered package for route
                indexes_of_packages = remove_delivered_package(indexes_of_packages, duplicate)
                # Updating position
                index_for_current_position = int(duplicates_on_distance_cleaned_list[0])

            # Handles duplicate values on route and cleaned list
            if mileage == shortest_route and duplicate_distance_on_route > 1 and len(
                    duplicates_on_distance_cleaned_list) > 1:
                # Grabbing first package from duplicate list
                first_package = duplicates_on_distance_cleaned_list[0]
                print("Dups on route and cleaned list")
                for package_id in comparative_list:
                    if package_id == first_package:
                        key = package_keys[comparative_list.index(package_id)]
                        key_value = myHash.search(key)
                        if key_value[8] == "En route":
                            key_value[8] = "Delivered"
                            delivery_time = (shortest_route / 18) * 60 * 60
                            dts = datetime.timedelta(seconds=delivery_time)
                            time = time + dts
                            key_value[9] = str(time)
                            myHash.insert(key, key_value)
                            indexes_of_packages.remove(first_package)
                            index_for_current_position = first_package

        # Returning to hub on last delivery
        if len(indexes_of_packages) == 0:
            print("To hub mileage ", mileage_list[0])
            delivery_time = (mileage_list[0] / 18) * 60 * 60
            dts = datetime.timedelta(seconds=delivery_time)
            time = time + dts
            print("Final Time ", time)
            truck_mileage += mileage_list[0]

            # Updating final times and mileage
            if truck == loadTruck1:
                loadTruck1.return_time = time
                print("Truck 1 ", loadTruck1.return_time)
            if truck == loadTruck2:
                loadTruck2.return_time = time
                print("Truck 2 ", loadTruck2.return_time)
                # Checking which truck has the min time and setting truck 3 depart time
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
    print("Test List ", comparative_list)
    print("Truck mileage ", truck_mileage)
    return truck_mileage


# Removing delivered packages and returning remaining packages
def remove_delivered_package(list, item):
    res = []
    for t in list:
        if t != item:
            res.append(t)
    return res


# Finding indices of a value in a list
def find_indices(l, value):
    return [
        index for index, item in enumerate(l)
        if item == value
    ]


# Starting the delivery process and returning mileage from truck
total_mileage += delivery_process(loadTruck1)
total_mileage += delivery_process(loadTruck2)
total_mileage += delivery_process(loadTruck3)


# User Interface
def ui():
    packages = []
    pack = 1
    # Adding packages to a list
    while pack < 41:
        packages.append(myHash.search(pack))
        pack += 1
    # Options for the user to choose from
    print("Please choose from the following options:\n"
          "1. Show all package info \n"
          "2. Total Mileage \n"
          "3. Search for a package by time \n"
          "4. Exit Program \n")
    user_input = int(input("Input number: "))
    print("User Input ", user_input)
    if user_input == 1:
        print(*packages, sep="\n")
        ui()
    if user_input == 2:
        print("Total Mileage: ", total_mileage)
        ui()
    if user_input == 3:
        print("Please enter a time using the following format: '8:00:00' ")
        time = str(input("Enter a time: "))
        for s in packages:
            if s[9] == time:
                print("Match = ", s)
        ui()
    if user_input == 4:
        sys.exit()


ui()
