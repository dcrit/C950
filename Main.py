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
        package_keys.append(package_list[0])
        list_of_package_info.append(package_list)
        list_of_delivery_addresses.append(package_list[1])

    print("List of delivery addresses ", list_of_delivery_addresses)
    print("Delivery addresses list length ", len(list_of_delivery_addresses))
    print("Package list ", list_of_package_info)

    # Adding all addresses to a list
    for col in address_list():
        list_of_all_addresses.append(col[1])

    # Getting the index of the current address
    for index in list_of_all_addresses:
        if index == current_address:
            index_for_current_position = list_of_all_addresses.index(index)

    # Getting indexes of packages from all addresses
    indexes_of_packages = [list_of_all_addresses.index(c) for c in list_of_delivery_addresses]

    while len(indexes_of_packages) > 0:

        print("Indexes of packages not sorted ", indexes_of_packages)

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
        mileage_list = [cleaned_list[i] for i in indexes_of_packages]
        print("Mileage list = ", mileage_list)
        print("Mileage List length = ", len(mileage_list))

        # Find the nearest route by using the min function
        shortest_route = min(mileage_list)
        print("Shortest route = ", shortest_route)

        # Adding mileage to total mileage
        truck_mileage += shortest_route

        # Breaking loop on last delivery and returning to hub
        if len(indexes_of_packages) == 1:
            print("Last stop index ", index_for_current_position)
            print("To hub mileage ", mileage_list[0])
            truck_mileage += mileage_list[0]
            break

        # Finding the index of the next route
        for item in cleaned_list:
            if item == shortest_route:
                print("Item ", item)
                index_for_current_position = cleaned_list.index(item)
                print("Index of next position ", index_for_current_position)

        # Removing delivered package from truck
        for index in indexes_of_packages:
            if index == index_for_current_position:
                indexes_of_packages.remove(index_for_current_position)

        # Clearing lists
        row_distant_list.clear()
        column_distant_list.clear()
        cleaned_list.clear()
        mileage_list.clear()

        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    print("Truck mileage ", truck_mileage)
    return truck_mileage


total_mileage += delivery_process(loadTruck1)
# total_mileage += delivery_process(loadTruck2)
# total_mileage += delivery_process(loadTruck3)
print("Total Mileage ", total_mileage)
