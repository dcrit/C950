# Author: Daniel Crites
# WGU Student ID:002152169
# NHP2 — NHP2 TASK 1: WGUPS ROUTING PROGRAM

import csv
import datetime
import Truck
import sys

from HashTable import ChainingHashTable
from Package import Package


# Reading address csv
# Space-time complexity O(n)
def address_list():
    with open('CSV_FILES/WGUPS_Address_Table.csv', encoding="utf-8-sig") as csv_file_address:
        csv_address = csv.reader(csv_file_address)
        csv_address = list(csv_address)
    return csv_address


# Reading package csv
# Space-time complexity O(n)
def package_list():
    with open('CSV_FILES/WGUPS_Package_File.csv', encoding='utf-8-sig') as csv_file_package:
        csv_package = csv.reader(csv_file_package)
        csv_package = list(csv_package)
    return csv_package


# Reading distance csv
# Space-time complexity O(n)
def distance_list():
    with open('CSV_FILES/WGUPS_Distance_Table.csv', encoding="utf-8-sig") as csv_file_distance:
        csv_distance = csv.reader(csv_file_distance)
        csv_distance = list(csv_distance)
    return csv_distance


# Creating hash object
my_hash = ChainingHashTable()


# Loading packages method
# Space-time complexity O(1)
def load_package_data(csvFile):
    packages = package_list()
    status = "At Hub"
    delivery_time = datetime.timedelta(hours=8)
    for package in packages:
        ID = int(package[0])
        address = package[1]
        city = package[2]
        state = package[3]
        zip_code = package[4]
        deadline = package[5]
        weight = package[6]
        notes = package[7]

        # Creating a Package object to put in hash table
        package_object = Package(ID, address, city, state, zip_code, deadline, weight, notes, status, delivery_time)

        # Inserting Package ID and Package Info in a hash table
        my_hash.insert(ID, package_object)


# Reading CSV Package file with load package method
load_package_data('CSV_FILES/WGUPS_Package_File.csv')

# Designating packages to trucks
# truck1 = [1, 2, 4, 5, 7, 8, 10, 11, 12, 21, 22, 23, 24, 26, 27, 29]
# truck2 = [3, 18, 36, 38, 13, 14, 15, 16, 17, 19, 20, 30, 31, 33, 34, 35]
# truck3 = [6, 25, 28, 32, 37, 39, 40, 9]

truck1 = [20, 13, 14, 15, 16, 29, 30, 31, 34, 37, 40, 27, 35, 39, 19, 33]
truck2 = [3, 36, 38, 6, 25, 28, 32, 1]
truck3 = [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 18, 21, 22, 23, 24, 26]

# Loading trucks
loadTruck1 = Truck.Truck(16, 18, 1, truck1, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                         datetime.timedelta(hours=8))
loadTruck2 = Truck.Truck(16, 18, 2, truck2, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
                         datetime.timedelta(hours=8))
loadTruck3 = Truck.Truck(16, 18, 3, truck3, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                         datetime.timedelta(hours=8))

# Total mileage variable
total_mileage = 0.0
time_count = 0


# Delivery Process method
# Space-time complexity O(n^2)
def delivery_process(truck):
    truck_mileage = 0.0
    depart_time = truck.depart_time
    index_for_current_position = 0
    # global time_count

    # Emtpy lists needed for my delivery process
    column_distant_list = []
    package_keys = []
    list_of_delivery_addresses = []
    list_of_all_addresses = []
    indexes_of_packages = []
    cleaned_list = []
    mileage_list = []

    # Adding all addresses to a list
    # Space-time complexity O(1)
    for col in address_list():
        list_of_all_addresses.append(col[1])

    # Loading truck and status of packages
    # Space-time complexity O(1)
    for packageID in truck.packages:
        # Adding Keys to a list
        package_keys.append(packageID)
        # Adding all delivery addresses to a list
        mileage = str(my_hash.search(packageID))
        package = mileage.split(", ")
        package[8] = "En route"
        my_hash.insert(packageID, package)
        list_of_delivery_addresses.append(package[1])

    # Getting indexes of packages being delivered
    # Space-time complexity O(n^2)
    for index in list_of_delivery_addresses:
        for a in list_of_all_addresses:
            if index == a:
                indexes_of_packages.append(list_of_all_addresses.index(index))
    # Creating a comparative list
    comparative_list = indexes_of_packages[:]

    # Packages are being delivered
    # Space-time complexity O(n)
    while len(indexes_of_packages) > 0:

        # Reading Distance CSV
        csv_distance = distance_list()

        # Adding row from current position index
        row_distant_list = csv_distance[index_for_current_position]

        # Adding column from current position index
        # Space-time complexity O(1)
        for column in csv_distance:
            column_distant_list.append(column[index_for_current_position])

        # Removing extra zero
        column_distant_list.remove('0')

        # Extending row_distant_list list with column_distant_list
        row_distant_list.extend(column_distant_list)

        # Removing empty spaces and converting list to float
        # Space-time complexity O(n)
        for cell in row_distant_list:
            if cell != "":
                cleaned_list.append(float(cell))

        # Getting mileage distances for packages on route
        # Space-time complexity O(1)
        for i in indexes_of_packages:
            mileage_list.append(cleaned_list[i])

        # Find the nearest route by using the min function
        shortest_route = min(mileage_list)

        # Checking for collisions on cleaned list
        collision_on_cleaned_list = find_indices(cleaned_list, shortest_route)

        # Counting collisions on the next route
        collision_on_route = mileage_list.count(shortest_route)

        # Updating packages when they are being delivered
        # Space-time complexity O(n)
        for mileage in cleaned_list:
            # Handles packages with no collision and then updates package
            if mileage == shortest_route and collision_on_route == 1 and len(
                    collision_on_cleaned_list) == 1:
                # Adding mileage to total mileage
                truck_mileage += shortest_route
                # Finding package id from list of keys
                x = comparative_list.index(cleaned_list.index(shortest_route))
                y = int(package_keys[x])
                # Pulling package from hash table to update
                key_value = my_hash.search(y)
                # Checking status of package and updating
                if key_value[8] == "En route":
                    key_value[8] = "Delivered"
                    delivery_time = (shortest_route / 18) * 60 * 60
                    dts = datetime.timedelta(seconds=delivery_time)
                    depart_time = depart_time + dts
                    key_value[9] = str(depart_time)
                    correct_package_time(depart_time)
                    my_hash.insert(y, key_value)
                    index_for_current_position = collision_on_cleaned_list[0]
                    p = int(collision_on_cleaned_list[0])
                    indexes_of_packages.remove(p)
            # Handles collisions values on clean list and updates packages
            # Space-time complexity O(n^2)
            if mileage == shortest_route and collision_on_route == 1 and len(
                    collision_on_cleaned_list) > 1:
                # Determining what collisions need to be delivered and updating package
                for package_id in comparative_list:
                    for duplicate in collision_on_cleaned_list:
                        if package_id == duplicate:
                            package_id = package_keys[comparative_list.index(package_id)]
                            key_value = my_hash.search(package_id)
                            if key_value[8] == "En route":
                                key_value[8] = "Delivered"
                                delivery_time = (shortest_route / 18) * 60 * 60
                                dts = datetime.timedelta(seconds=delivery_time)
                                depart_time = depart_time + dts
                                key_value[9] = str(depart_time)
                                correct_package_time(depart_time)
                                my_hash.insert(package_id, key_value)
                                index_for_current_position = duplicate
                                truck_mileage += shortest_route
                                indexes_of_packages.remove(duplicate)

            # Handles collisions on route and updates package
            # Space-time complexity O(n)
            if mileage == shortest_route and collision_on_route > 1 and len(
                    collision_on_cleaned_list) == 1:
                # Adding mileage to truck
                truck_mileage += shortest_route
                # Grabbing first collision on cleaned list
                duplicate = int(collision_on_cleaned_list[0])
                # Getting time for distance travel
                delivery_time = (shortest_route / 18) * 60 * 60
                dts = datetime.timedelta(seconds=delivery_time)
                depart_time = depart_time + dts
                indexes = []
                keys = []
                for package_id in comparative_list:
                    if package_id == duplicate:
                        indexes = find_indices(comparative_list, package_id)
                for package_id in indexes:
                    keys.append(package_keys[package_id])
                # Checking package status and then updating package
                for key in keys:
                    package_id = key
                    key_value = my_hash.search(package_id)
                    if key_value[8] == "En route":
                        key_value[8] = "Delivered"
                        key_value[9] = str(depart_time)
                        my_hash.insert(package_id, key_value)
                        correct_package_time(depart_time)
                # Removing delivered package for route
                indexes_of_packages = remove_delivered_package(indexes_of_packages, duplicate)
                # Updating position
                index_for_current_position = int(collision_on_cleaned_list[0])

            # Handles collisions on route and cleaned list
            # Space-time complexity O(n)
            if mileage == shortest_route and collision_on_route > 1 and len(
                    collision_on_cleaned_list) > 1:
                # Grabbing first package from collision list
                first_package = collision_on_cleaned_list[0]
                for package_id in comparative_list:
                    if package_id == first_package:
                        key = package_keys[comparative_list.index(package_id)]
                        key_value = my_hash.search(key)
                        if key_value[8] == "En route":
                            key_value[8] = "Delivered"
                            delivery_time = (shortest_route / 18) * 60 * 60
                            dts = datetime.timedelta(seconds=delivery_time)
                            depart_time = depart_time + dts
                            key_value[9] = str(depart_time)
                            correct_package_time(depart_time)
                            my_hash.insert(key, key_value)
                            indexes_of_packages.remove(first_package)
                            index_for_current_position = first_package

        # Returning to hub on last delivery
        if len(indexes_of_packages) == 0:
            delivery_time = (mileage_list[0] / 18) * 60 * 60
            dts = datetime.timedelta(seconds=delivery_time)
            depart_time = depart_time + dts
            truck_mileage += mileage_list[0]
            # Updating final times and mileage
            if truck == loadTruck1:
                loadTruck1.return_time = depart_time
                print("Truck 1 ")
            if truck == loadTruck2:
                loadTruck2.return_time = depart_time
                # Checking which truck has the min time and setting truck 3 depart time
                loadTruck3.depart_time = min(loadTruck1.return_time, loadTruck2.return_time)
            if truck == loadTruck3:
                loadTruck3.return_time = depart_time

        # Clearing lists
        row_distant_list.clear()
        column_distant_list.clear()
        cleaned_list.clear()
        mileage_list.clear()

    # Returning truck mileage
    return truck_mileage


# Removing delivered packages and returning remaining packages
# Space-time complexity O(n)
def remove_delivered_package(list, item):
    res = []
    for t in list:
        if t != item:
            res.append(t)
    return res


# Finding indices of a value in a list
# Space-time complexity O(n)
def find_indices(list, value):
    return [
        index for index, item in enumerate(list)
        if item == value
    ]


# Correct Address of Package 9 at 10:20:00
# Space-time complexity O(n)
def correct_package_time(time):
    time_correction = datetime.timedelta(hours=10, minutes=20, seconds=00)
    global time_count
    if time >= time_correction and time_count == 0:
        re = str(my_hash.search(9)).split(',')
        re[1] = "410 S State St"
        re[7] = "Address Corrected"
        re = ', '.join(re)
        my_hash.insert(9, re)
        time_count += 1


def Repeat(x):
    _size = len(x)
    repeated = []
    for i in range(_size):
        k = i + 1
        for j in range(k, _size):
            if x[i] == x[j] and x[i] not in repeated:
                repeated.append(str(x[i]))
                # print("index ", x.index(i))
    return repeated


# Starting the delivery process and returning mileage from truck
total_mileage += delivery_process(loadTruck1)
total_mileage += delivery_process(loadTruck2)
total_mileage += delivery_process(loadTruck3)


# User Interface
# Space-time complexity O(n^2)
def ui():


    truck1 = []
    truck2 = []
    truck3 = []

    here = []
    two = []
    pack = 1
    while pack < 41:
        here.append(my_hash.search(pack))
        u = my_hash.search(pack)[9]
        (hours, minutes, seconds) = u.split(":")
        time_convert = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        two.append(time_convert)
        pack += 1
    packages = here[:]
    delivery_times = two[:]
    # Adding packages to a list
    # Space-time complexity O(n)


    # Options for the user to choose from
    print("Please choose from the following options:\n"
          "1. Show all package info \n"
          "2. Total Mileage \n"
          "3. Search for a package by time \n"
          "4. Search packages between times \n"
          "5. Search all package statuses for a given time \n"
          "6. Exit Program \n")
    user_input = None
    try:
        user_input = int(input("Input number: "))
    except ValueError:
        print("Please enter a valid number \n")
    # Prints all the packages
    if user_input == 1:
        # package_info = []
        # pack = 1
        # while pack < 41:
        #     package_info.append(my_hash.search(pack))
        #     pack += 1
        print(*packages, sep="\n")

    # Prints the total mileage
    if user_input == 2:
        print("Total Mileage: ", total_mileage, "\n")

    # Prints delivered package given a time
    if user_input == 3:
        print("Please enter a time using the following format: '8:00:00' ")
        time = str(input("Enter a time: "))
        for s in packages:
            if s[9] == time:
                print("Match = ", s)
        if time not in packages:
            print("Nothing found \n")
    # Prints delivered packages between given times
    if user_input == 4:
        print("Please enter a 24 hour start time and end time using the following format: '8:00:00' ")
        count = 0
        try:
            start_time = str(input("Enter start time: "))
            end_time = str(input("Enter a end time: "))
            (hours, minutes, seconds) = start_time.split(":")
            start_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            (hours, minutes, seconds) = end_time.split(":")
            end_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            # Looking for times in between start and end times
            # Space-time Complexity O(n)
            for j in delivery_times:
                if start_time <= j <= end_time:
                    print("Found: ", str(my_hash.search(int(delivery_times.index(j) + 1))))
                    count += 1
            if count == 0:
                print("All packages have been delivered before given times. \n"
                      "Please choose different times. \n")

        except ValueError:
            print("Enter a valid time \n")
    # Prints all package status given a time
    if user_input == 5:
        try:
            print("Please enter a 24 hour time using the following format: '8:00:00' ")
            time = str(input("Enter time: "))
            (hours, minutes, seconds) = time.split(":")
            time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

            uniqueList = []
            duplicateList = []

            for i in delivery_times:
                if i not in uniqueList:
                    uniqueList.append(delivery_times.index(i) + 1)
                elif i not in duplicateList:
                    duplicateList.append(delivery_times.index(i))

            dupy = list(sorted(set(range(uniqueList[0], uniqueList[-1])) - set(uniqueList)))
            res_list = [uniqueList[i - 1] for i in dupy]
            print("Res list ",  res_list)
            t1 = list(loadTruck1.packages)
            t2 = list(loadTruck2.packages)
            t3 = list(loadTruck3.packages)

            for s in delivery_times:
                if s <= time:
                    for t in t1:
                        if t == delivery_times.index(s) + 1 and delivery_times.index(s) + 1 not in res_list:
                            key = list(my_hash.search(t))[:]
                            truck = "Delivered on Truck 1"
                            key.insert(0, truck)
                            truck1.append(key)
                            t1.remove(t)

                        if t == delivery_times.index(s) + 1 and delivery_times.index(s) + 1 in res_list:
                            er = find_indices(uniqueList, t)
                            for y in er:
                                key = my_hash.search(y + 1)[:]
                                truck = "Delivered on Truck 1"
                                key.insert(0, truck)
                                truck1.append(key)
                                t1.remove(y + 1)

                    for b in t2:
                        if delivery_times.index(s) + 1 == b and delivery_times.index(s) + 1 not in res_list:
                            key = list(my_hash.search(b))[:]
                            truck = "Delivered on Truck 2"
                            key.insert(0, truck)
                            truck2.append(key)
                            t2.remove(b)

                        if b == delivery_times.index(s) + 1 and delivery_times.index(s) + 1 in res_list:
                            er = find_indices(uniqueList, b)

                    for r in t3:
                        if delivery_times.index(s) + 1 == r and delivery_times.index(s) + 1 not in res_list:
                            print("RRRR 1 ", r)
                            key = list(my_hash.search(r))[:]
                            truck = "Delivered on Truck 3"
                            key.insert(0, truck)
                            truck3.append(key)
                            t3.remove(r)
                        if r == delivery_times.index(s) + 1 and delivery_times.index(s) + 1 in res_list:
                            er = find_indices(uniqueList, r)
                            print("RRRR 2 ", r)
                            total = 0
                            for y in er:
                                key = my_hash.search(y + 1)[:]
                                truck = "Delivered on Truck 3"
                                key.insert(0, truck)
                                total += 1
                                truck3.append(key)
                                t3.remove(y + 1)

                if s > time >= datetime.timedelta(hours=int(8), minutes=int(0), seconds=int(0)):
                    for t in t1:
                        if delivery_times.index(s) + 1 == t and delivery_times.index(s) + 1 not in res_list:
                            key = list(my_hash.search(delivery_times.index(s) + 1))[:]
                            key.insert(0, "En route on Truck 1")
                            key[9] = "En Route"
                            key[10] = ""
                            truck1.append(key)
                            t1.remove(t)
                        if t == delivery_times.index(s) + 1 and delivery_times.index(s) + 1 in res_list:
                            er = find_indices(uniqueList, t)
                            print("ERER t12 ", er)
                            for y in er:
                                key = my_hash.search(y + 1)[:]
                                truck = "En route Truck 1"
                                key.insert(0, truck)
                                truck1.append(key)
                                t1.remove(y + 1)
                    for b in t2:
                        if delivery_times.index(s) + 1 == b and delivery_times.index(s) + 1 not in res_list and time < datetime.timedelta(hours=int(9), minutes=int(5), seconds=int(0)):
                            print("Check it")
                            key = my_hash.search(delivery_times.index(s) + 1)[:]
                            key.insert(0, "At hub on Truck 2")
                            key[9] = "At hub"
                            key[10] = ""
                            truck2.append(key)
                            t2.remove(b)

                        if delivery_times.index(s) + 1 == b and delivery_times.index(s) + 1 not in res_list and time > datetime.timedelta(hours=int(9), minutes=int(5), seconds=int(0)) :
                            print("here ", b)
                            er = find_indices(uniqueList, b)
                            print("ERER t21 ", er)
                            key = list(my_hash.search(delivery_times.index(s) + 1))[:]
                            key.insert(0, "En route on Truck 2")
                            key[9] = "En Route"
                            key[10] = ""
                            truck2.append(key)
                            t2.remove(b)
                        if b == delivery_times.index(s) + 1 and delivery_times.index(s) + 1 in res_list:
                            er = find_indices(uniqueList, b)
                            print("ERER t22 ", er)
                            for y in er:
                                key = my_hash.search(y + 1)[:]
                                truck = "En route Truck 2"
                                key.insert(0, truck)
                                truck2.append(key)
                                t2.remove(y + 1)

                    for r in t3:
                        if delivery_times.index(s) + 1 == r and time < loadTruck2.return_time and delivery_times.index(s) + 1 not in res_list:
                            er = find_indices(uniqueList, r)
                            print("t3 1", er)
                            key = list(my_hash.search(delivery_times.index(s) + 1))[:]
                            key.insert(0, "En route on Truck 3")
                            key[9] = "En Route"
                            key[10] = ""
                            truck3.append(key)
                            t3.remove(r)
                        if delivery_times.index(s) + 1 == r and time > loadTruck2.return_time and delivery_times.index(s) + 1 not in res_list:
                            er = find_indices(uniqueList, r)
                            print("t3 2", er)
                            key = list(my_hash.search(delivery_times.index(s) + 1))[:]
                            key.insert(0, "En route on Truck 3")
                            key[9] = "En Route"
                            key[10] = ""
                            truck3.append(key)
                            t3.remove(r)
                        if delivery_times.index(s) + 1 == r and time < loadTruck2.return_time and delivery_times.index(s) + 1 in res_list:
                            er = find_indices(uniqueList, r)
                            print("t3 3", er)
                            for y in er:
                                key = my_hash.search(y + 1)[:]
                                truck = "En route Truck 3"
                                key.insert(0, truck)
                                truck3.append(key)
                                t3.remove(y + 1)
                        if delivery_times.index(s) + 1 == r and time > loadTruck2.return_time and delivery_times.index(s) + 1 in res_list:
                            er = find_indices(uniqueList, r)
                            print("t3 4", er)
                            key = list(my_hash.search(delivery_times.index(s) + 1))[:]
                            key.insert(0, "En route on Truck 3")
                            key[9] = "En Route"
                            key[10] = ""
                            truck3.append(key)
                            t3.remove(r)
                if s > time < datetime.timedelta(hours=int(8), minutes=int(0), seconds=int(0)):
                    print("Yooo ")

            print("Truck 1", *truck1, sep="\n")
            print("Truck 1 length ", len(truck1))
            print("Truck 2", *truck2, sep="\n")
            print("Truck 2 ", len(truck2))
            print("Truck 3", *truck3, sep="\n")
            print("Truck 3 length ", len(truck3))

            print("t1 ", t1)
            print("t2 ", t2)
            print("t3 ", t3)

        except ValueError:
            print("Please enter a valid time ")

    if user_input == 6:
        sys.exit()
    ui()


ui()
