# Author: Daniel Crites
# WGU Student ID:002152169
# NHP2 — NHP2 TASK 1: WGUPS ROUTING PROGRAM

import csv
import datetime
import Truck

from HashTable import ChainingHashTable


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

            # Inserting Package ID and Package Info in a hash table
            myHash.insert(ID, package)


# Reading CSV Package file with load package method
loadPackageData('CSV_FILES/WGUPS_Package_File.csv')

truck1 = [1, 2, 4, 5, 7, 8, 10, 11, 12, 21, 22, 23, 24, 26, 27, 29]
truck2 = [3, 18, 36, 38, 13, 14, 15, 16, 17, 19, 20, 30, 31, 33, 34, 35]
truck3 = [6, 25, 28, 32, 37, 39, 40, 9]

loadTruck1 = Truck.Truck(16, 18, 1, truck1, 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
loadTruck2 = Truck.Truck(16, 18, 2, truck2, 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
loadTruck3 = Truck.Truck(16, 18, 3, truck3, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))


def cool_func(list1, list2):
    blank = []
    for trip in list1:
       # print("Trip ", trip)
        for f in list2:
            if f != 0:
                if trip == list2.index(f):
                    print("list2 index = ", list2.index(f))
                    print("Trip 2 ", trip)
                    blank.append(f)
    print("Blank ", blank)
    return blank


total_mileage = 0.0


# Delivery Process method
def delivery_process(truck):
    truck_mileage = 0.0
    current_address = truck.address
    index_for_current_position = 0

    list_of_package_info = []
    column_distant_list = []
    package_keys = []
    list_of_delivery_addresses = []
    list_of_all_addresses = []
    mileage_list = []

    shortest_route = 0.0

    keys = []
    values = []

    # Checking load of truck, then adding packages to lists
    for packageID in truck.packages:
        package_list = myHash.search(packageID)
        package_keys.append(package_list[0])
        keys.append(package_list[0])
        list_of_package_info.append(package_list)
        list_of_delivery_addresses.append(package_list[1])
        values.append(package_list[1])


    print("List of delivery addresses ", list_of_delivery_addresses)
    # Adding all addresses to a list
    for col in address_list():
        list_of_all_addresses.append(col[1])

    for t in list_of_all_addresses:
        if t == current_address:
            index_for_current_position = list_of_all_addresses.index(t)

    # Getting indexes of packages from all addresses
    indexes_of_packages = [list_of_all_addresses.index(c) for c in list_of_delivery_addresses]
    print("Indexs of packages ", indexes_of_packages)

    dictionary = dict(zip(indexes_of_packages, values))
    print("Dict ", dictionary)
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

        # Removing empty spaces and moving data to 'cleaned list'
        cleaned_list = [ele for ele in row_distant_list if ele.strip()]

        # Converting str list to float
        cleaned_list = [float(ele) for ele in cleaned_list]
        print("Cleaned List ", cleaned_list)

        # Getting mileage distances for packages on route
        mileage_list = cool_func(indexes_of_packages, cleaned_list)
        print("Mileage List ", mileage_list)


        if len(mileage_list) == 0:
            print("Yoo ", cleaned_list)
            for h in list_of_all_addresses:
                if h == index_for_current_position:
                    print("H ", h)
            break

        shortest_route = min(mileage_list)
        truck_mileage += shortest_route

        # Finding the index of the next route
        for item in cleaned_list:
            if item == shortest_route:
                index_for_current_position = cleaned_list.index(item)

        # Removing indexes from index of packages
        for j in indexes_of_packages:
            if j == index_for_current_position:
                indexes_of_packages.remove(index_for_current_position)

        # Clearing lists
        row_distant_list.clear()
        column_distant_list.clear()
        cleaned_list.clear()
        mileage_list.clear()

    print("Truck mileage ", truck_mileage)
    return truck_mileage

        # print("List Of Current Route ", cleaned_list)
        # print("Current Address ", current_address)


# total_mileage += delivery_process(loadTruck1)
total_mileage += delivery_process(loadTruck2)
# total_mileage += delivery_process(loadTruck3)
print("Total Mileage ", total_mileage)

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
# for i in range(len(myHash.table) + 1):
#     print("Package ID: {} {}".format(i + 1, myHash.search(i + 1)))
#
# def second_smallest(numbers):
# #     m1 = m2 = float('inf')
# #     for x in numbers:
# #         if x <= m1:
# #             m1, m2 = x, m1
# #         elif x < m2:
# #             m2 = x
# #     return m2
# def smallest_num_in_list(list):
#     any = list[0]
#     for a in list:
#         if a != 0:
#             if a < any:
#                 any = a
#     return any
