# Author: Daniel Crites
# WGU Student ID:002152169
# NHP2 — NHP2 TASK 1: WGUPS ROUTING PROGRAM

import csv
import datetime
import re

import HashTable

import CSV_FILES
import HashTable
import Package
import Truck

from HashTable import ChainingHashTable
from Package import Package

# Reading Address CSV
with open('CSV_FILES/WGUPS_Address_Table.csv', encoding="utf-8-sig") as csv_file_address:
    CSV_Address = csv.reader(csv_file_address)
    CSV_Address = list(CSV_Address)



with open('CSV_FILES/WGUPS_Package_File.csv', encoding='utf-8-sig') as csv_file_package:
    CSV_Package = csv.reader(csv_file_package)
    CSV_Package = list(CSV_Package)

myHash = ChainingHashTable()


def loadPackageData(csvFile):
    with open(csvFile, encoding='utf-8-sig') as packageData:
        PO = csv.reader(packageData, delimiter=',')

        for package in PO:
            ID = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            deadline = package[5]
            weight = package[6]
            status = package[7]

            package = package

            myHash.insert(ID, package)


loadPackageData('CSV_FILES/WGUPS_Package_File.csv')

# for i in range(len(myHash.table) + 1):
#     print("Package ID: {} {}".format(i + 1, myHash.search(i + 1)))
#


truck1 = [1, 2, 4, 5, 7, 8, 10, 11, 12, 21, 22, 23, 24, 26, 27, 29]
truck2 = [3, 18, 36, 38, 13, 14, 15, 16, 17, 19, 20, 30, 31, 33, 34, 35]
truck3 = [6, 25, 28, 32, 37, 39, 40, 9]

loadTruck1 = Truck.Truck(16, 18, 1, truck1, 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
loadTruck2 = Truck.Truck(16, 18, 2, truck2, 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
loadTruck3 = Truck.Truck(16, 18, 3, truck3, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))





def second_smallest(numbers):
    m1 = m2 = float('inf')
    for x in numbers:
        if x <= m1:
            m1, m2 = x, m1
        elif x < m2:
            m2 = x
    print("Second Smallest ", m2)


def delivery_process(truck):
    current_address = truck.address


    empty_list = []
    column_distant_list = []
    package_keys = []
    list_of_delivery_addresses = []
    list_of_all_addresses = []

    truck_mileage = 0.0

    shortest_route = 0
    index = 0
    count = 0

    index_for_current_position = 0

    keys = []
    values = []

    # Checking load of truck, then adding packages to lists
    for packageID in truck.packages:
        package_list = myHash.search(packageID)
        package_keys.append(package_list[0])
        keys.append(package_list[0])
        empty_list.append(package_list)
        list_of_delivery_addresses.append(package_list[1])
        values.append(package_list[1])

    dictionary = dict(zip(keys, values))
    # print("Dict ", dictionary)

    # Adding all addresses to a list
    for col in CSV_Address:
        list_of_all_addresses.append(col[1])

    for t in list_of_all_addresses:
        if t == current_address:
            index_for_current_position = list_of_all_addresses.index(t)

    dumb = [list_of_all_addresses.index(c) for c in list_of_delivery_addresses]


    while count < 16:
        # Reading Distance CSV
        with open('CSV_FILES/WGUPS_Distance_Table.csv', encoding="utf-8-sig") as csv_file_distance:
            CSV_Distance = csv.reader(csv_file_distance)
            CSV_Distance = list(CSV_Distance)

        print("Count = ", count)
        print("Big Balls ", CSV_Distance)
        # Adding row from current position index
        row_distant_list = CSV_Distance[index_for_current_position]
        print("row distance ", row_distant_list)

        # Adding column from current position index
        print("CSV Distance list ", CSV_Distance)
        for column in CSV_Distance:
            column_distant_list.append(column[index_for_current_position])
        print("Column distant list ",  column_distant_list)

        # Removing extra zero
        print("Column Distant List ", column_distant_list)
        column_distant_list.remove('0')

        # Extending row_distant_list list with column_distant_list
        row_distant_list.extend(column_distant_list)

        # Removing empty spaces and moving data to 'cleaned list'
        cleaned_list = [ele for ele in row_distant_list if ele.strip()]

        # Clearing row and column list
        row_distant_list.clear()
        column_distant_list.clear()


        print("Cleaned List ", cleaned_list)
        # Finding the index of the second-smallest number
        for item in cleaned_list:
            if item != 0:
                shortest_route = item
                index = cleaned_list.index(item)
                mileage = float(shortest_route)

        print("Shortest Route ", shortest_route)
        truck_mileage += mileage
        print("Truck Mileage ", truck_mileage)
        index_for_current_position = index


        count += 1

        # print("List Of Current Route ", cleaned_list)
        # print("Current Address ", current_address)


delivery_process(loadTruck1)

# Garbage Code
# index = listOfCurrentRoute.index(min(listOfCurrentRoute))
# listOfCurrentRoute = ['0' if i.strip() == '' else i for i in listOfCurrentRoute]
# if myHash.search(5):
#     print("Match", myHash.search(5))
#     keyAddress = myHash.search(5)
#     print("Key Address", keyAddress[1])
# print("yo", myHash.search(1))
# my_dict = dict()
# for index, value in enumerate(CSV_Package):
#     my_dict[index + 1] = value
# print("my dict", my_dict)

# selmt = min(cleaned_list)
# cleaned_list.pop(cleaned_list.index(selmt))
# sselmt = min(cleaned_list)
# truck_mileage = float(sselmt)
# for num in cleaned_list:
#     if num <= sm:
#         sm, ssm = num, sm
#     elif num < ssm:
#         ssm = num

# rows = len(CSV_Distance)
# cols = len(CSV_Distance[0])

# row = 0
# col = 0
# index = 0

# listOfCurrentRoute = []
# listOfRoutesUsingNN = []

# while (col <= cols):

# for column in CSV_Distance:
#     listOfCurrentRoute.append(column[col])
# index = listOfCurrentRoute.index(min(listOfCurrentRoute))
# index += 2
# print("index ", index)
# listOfRoutesUsingNN.append(index)
# print("Current Route", listOfCurrentRoute)
#
# print("List of routes", listOfRoutesUsingNN)
# listOfCurrentRoute.clear()
#
# for col2 in CSV_Distance:
#     listOfCurrentRoute.append(col2[index])
# listOfCurrentRoute = [ele.lstrip('0') for ele in listOfCurrentRoute]
# listOfCurrentRoute = list(filter(None, listOfCurrentRoute))
#
# listOfCurrentRoute = ['0' if i.strip() == '' else i for i in listOfCurrentRoute]
# print("Current List", listOfCurrentRoute)
#
# index = listOfCurrentRoute.index(min(listOfCurrentRoute))
#
# print("index 2 ", index)
#
# listOfRoutesUsingNN.append(index)
# print("List of cur ", listOfRoutesUsingNN)

# Holy Fuck it works!!!!!!!!!!!!!
# z = [0 for i in range(len(list_of_delivery_addresses))]
# for i, j in enumerate(list_of_delivery_addresses):
#     for k, l in enumerate(list_of_all_addresses):
#         if j == l:
#             z[i] = k
#             break
# print("SUPPPRET GAY ", z)

# list_3 = []
# for r in range(len(list_of_delivery_addresses)):
#     for j in range(len(list_of_all_addresses)):
#         if list_of_delivery_addresses[r] == list_of_all_addresses[j]:
#             list_3.append(j)
# print("List 3 ", list_3)
