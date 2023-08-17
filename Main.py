# Author: Daniel Crites
# WGU Student ID:002152169
# NHP2 — NHP2 TASK 1: WGUPS ROUTING PROGRAM

import csv
import datetime

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
    # for row in CSV_Address:
    #     print("Address file ", row)
    # indexContents = CSV_Address[0][1]
    # print("Index ", indexContents)
# Reading Distance CSV
with open('CSV_FILES/WGUPS_Distance_Table.csv', encoding="utf-8-sig") as csv_file_distance:
    CSV_Distance = csv.reader(csv_file_distance)
    CSV_Distance = list(CSV_Distance)

    rows = len(CSV_Distance)
    cols = len(CSV_Distance[0])

    # row = 0
    # col = 0
    # index = 0

    listOfCurrentRoute = []
    listOfRoutesUsingNN = []

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

with open('CSV_FILES/WGUPS_Package_File.csv', encoding='utf-8-sig') as csv_file_package:
    CSV_Package = csv.reader(csv_file_package)
    CSV_Package = list(CSV_Package)
    # my_dict = dict()
    # for index, value in enumerate(CSV_Package):
    #     my_dict[index + 1] = value
    # print("my dict", my_dict)

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


def distance_in_between(x_value, y_value):
    distance = CSV_Distance[x_value][y_value]
    if distance == '':
        distance = CSV_Distance[y_value][x_value]

    print("Distance ", distance)


if myHash.search(5):
    print("Match", myHash.search(5))
    keyAddress = myHash.search(5)
    print("Key Address", keyAddress[1])
print("yo", myHash.search(1))


def delivery_process(truck):
    empty_list = []
    current_address = truck.address
    listOfCurrentRoute = []
    row = 0
    col = 0
    index = 0

    for column in CSV_Distance:
        listOfCurrentRoute.append(column[col])


    #listOfCurrentRoute = ['0' if i.strip() == '' else i for i in listOfCurrentRoute]
    listOfCurrentRoute = [ele.lstrip('0') for ele in listOfCurrentRoute]
    cleaned_list = [ele for ele in listOfCurrentRoute if ele.strip()]
    # index = listOfCurrentRoute.index(min(listOfCurrentRoute))
    index = cleaned_list.index(min(cleaned_list)) + 1
    print("List Of Current Route ", cleaned_list)

    print("Index ", index)
    print("Current Address ", current_address)

    for packageID in truck.packages:
        package_list = myHash.search(packageID)
        empty_list.append(package_list)

    print("Inside package list", empty_list)


delivery_process(loadTruck1)
