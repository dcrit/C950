# Author: Daniel Crites
# WGU Student ID:002152169
# NHP2 — NHP2 TASK 1: WGUPS ROUTING PROGRAM

import csv
import HashTable

import CSV_FILES
import HashTable
import Package
import Truck

from HashTable import ChainingHashTable
from Package import Package

# gay
# Reading Address CSV
with open('CSV_FILES/WGUPS_Address_Table.csv') as csv_file_address:
    CSV_Address = csv.reader(csv_file_address)
    CSV_Address = list(CSV_Address)
    # for row in CSV_Address:
    #     print(row)

# Reading Distance CSV
with open('CSV_FILES/WGUPS_Distance_Table.csv') as csv_file_distance:
    CSV_Distance = csv.reader(csv_file_distance)
    CSV_Distance = list(CSV_Distance)

    rows = len(CSV_Distance)
    cols = len(CSV_Distance[0])

    row = 0
    col = 0
    index = 0

    listOfCurrentRoute = []
    listOfRoutesUsingNN = []

    # while (col <= cols):

    for column in CSV_Distance:
        listOfCurrentRoute.append(column[col])
    index = listOfCurrentRoute.index(min(listOfCurrentRoute))
    index += 2
    # print("index ", index)
    # listOfRoutesUsingNN.append(index)
    # print("Current Route", listOfCurrentRoute)
    #
    # print("List of routes", listOfRoutesUsingNN)
    # listOfCurrentRoute.clear()

    for col2 in CSV_Distance:
        listOfCurrentRoute.append(col2[index])
    # listOfCurrentRoute = [ele.lstrip('0') for ele in listOfCurrentRoute]
    # listOfCurrentRoute = list(filter(None, listOfCurrentRoute))

    # listOfCurrentRoute = ['0' if i.strip() == '' else i for i in listOfCurrentRoute]
    # print("Current List", listOfCurrentRoute)
    #
    # index = listOfCurrentRoute.index(min(listOfCurrentRoute))
    #
    # print("index 2 ", index)
    #
    # listOfRoutesUsingNN.append(index)
    # print("List of cur ", listOfRoutesUsingNN)

with open('CSV_FILES/WGUPS_Package_File.csv') as csv_file_package:
    CSV_Package = csv.reader(csv_file_package)
    CSV_Package = list(CSV_Package)



myHash = ChainingHashTable()
def loadPackageData(fileName):
    with open(fileName, encoding='utf-8-sig') as packageData:
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

            myHash.insert(ID,package)


loadPackageData('CSV_FILES/WGUPS_Package_File.csv')

for i in range(len(myHash.table) + 1):
    print("Package ID: {} {}".format(i+1, myHash.search(i+1)))

print("yo", myHash.search(1))
