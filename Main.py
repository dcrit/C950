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

with open('CSV_FILES/WGUPS_Package_File.csv') as test:
    CSV_Package = csv.reader(test)
    CSV_Package = list(CSV_Package)
    # for row in CSV_Package:
    #     print(row)
    # print(CSV_Package[0][])

# def distance(x, y):
#     d = CSV_Distance[x][y]
#     if d == '':
#         d = CSV_Distance[y][x]
#     print(d)
#     return float(d)
#
#
# print(distance(6, 2))

# with open('CSV_FILES/WGUPS_Distance_Table.csv') as df:
