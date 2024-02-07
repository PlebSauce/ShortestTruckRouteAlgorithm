# main.py
# Author: Jordan Nicholls
# Student ID: 011459778
#
# Takes an object-oriented approach by creating packages and trucks in a separate
# class and creates objects from those classes.
import csv
import Truck
import datetime
from builtins import ValueError
from HashTable import HashTable
from Packages import Packages

# Opening and reading from our CSV files
with open('CSV/addressCSV.csv') as csvfileAddress:
    addressCSV = csv.reader(csvfileAddress)
    addressCSV = list(addressCSV)
with open('CSV/distanceCSV.csv') as csvfileDist:
    distanceCSV = csv.reader(csvfileDist)
    distanceCSV = list(distanceCSV)
with open('CSV/packageCSV.csv') as csvfilePackage:
    packageCSV = csv.reader(csvfilePackage)
    packageCSV = list(packageCSV)


# Citing Source: W-3_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy_Dijkstra.py
# Loading our hash table with package information from our csv file
def load_packages(filename, packageHash):
    with open(filename) as packagesCSV:
        packageInfo = csv.reader(packagesCSV)
        next(packageInfo)
        for package in packageInfo:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = 'At Hub'

            # creating a new package object for each of the 40 packages
            p = Packages(pID, pAddress, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus)

            # inserting our new package object into our hash table
            packageHash.insert(pID, p)


# initializing our package hash table
packageHash = HashTable()

# calling our loader using the packageCSV file and putting it into our newly created
# hash table
load_packages("CSV/packageCSV.csv", packageHash)

# Manually load each truck
truck1 = Truck.Truck([1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40], 0.0, "4001 South 700 East",datetime.timedelta(hours=8))
truck2 = Truck.Truck([3, 6, 9, 18, 25, 28, 32, 35, 36, 38, 39], 0.0, "4001 South 700 East",datetime.timedelta(hours=9, minutes=5))
truck3 = Truck.Truck([2, 4, 5, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 33], 0.0, "4001 South 700 East", datetime.timedelta(hours=11))


# method to be used for calculating the distance based on our distanceCSV file
def calculate_distance(address1, address2):
    distance = distanceCSV[address1][address2]
    if distance == '':
        distance = distanceCSV[address2][address1]
    return float(distance)


# Method for getting the key from a given address. This helps because this key maps to
# our distanceCSV file.
def get_address_key(address):
    for row in addressCSV:
        if address in row[2]:
            return int(row[0])


# Our algorithm that does most of the work. This uses the nearest neighbor algorithm
def truck_deliver_algo(truck):
    # Extract truck packages into new list to perform a sort later on in the algo
    # and be placed back in truck when the next shortest distance is found
    toBeDelivered=[]
    for packageID in truck.packages:
        packageToLoad = packageHash.search(packageID)
        toBeDelivered.append(packageToLoad)
    truck.packages.clear()

    # this loop runs while there are still packages to be delivered. Previously we
    # loaded this list with all items from the truck. Now we will take those items out
    # and put them back into our truck with the shortest distance being selected at
    # each loop
    while len(toBeDelivered) > 0:
        next_dist = 300.0
        next_package = None
        # Find the shortest distance
        for somePackage in toBeDelivered:
            if calculate_distance(get_address_key(truck.currLocation), get_address_key(somePackage.address)) <= next_dist:
                next_dist = calculate_distance(get_address_key(truck.currLocation), get_address_key(somePackage.address))
                next_package = somePackage
        # Add shortest back to truck packages, remove from temp list
        truck.packages.append(next_package.ID)
        toBeDelivered.remove(next_package)
        # Add dist to truck millage
        truck.millage += next_dist
        # Update truck address
        truck.currLocation = next_package.address
        # Update time
        truck.time += datetime.timedelta(hours=next_dist / 18)
        next_package.deliveredTime = truck.time
        next_package.initialTime = truck.initialTime


if __name__ == '__main__':
    print('Western Governors University Parcel Service (WGUPS)')
    # run the algorithm with 3 truck objects
    truck_deliver_algo(truck1)
    truck_deliver_algo(truck2)
    # before running 3rd, wait until one truck gets back
    truck3.initialTime = min(truck1.time, truck2.time)
    truck_deliver_algo(truck3)
    # Display total millage
    print('Total millage:')
    print(truck1.millage + truck2.millage + truck3.millage)

    # Prompt user to enter a time for which they would like to see the status of
    # each package. Uses try-except to ensure value meets the requirements
    userTime = input("Enter the time (format HH:MM) for which you would like to see the status of a package: ")
    try:
        (h, m) = userTime.split(":")
        deltaTimeConvert = datetime.timedelta(hours=int(h),minutes=int(m))
        # Prompt user whether they want a specific package or all (single may be
        # useful for debugging)
        SingleOrAll = input("Enter SINGLE for info on 1 package. Enter ALL for info on all packages (use all caps): ")
        if SingleOrAll == "SINGLE":
            try:
                # Prompt user to enter which package they would like to search for
                entry = int(input("Enter the package ID: "))
                searchedPackage = packageHash.search(entry)
                searchedPackage.status_update(deltaTimeConvert)
                print(str(searchedPackage))
            except AttributeError:
                print("Entry must be between 1-41")
                exit()
        elif SingleOrAll == "ALL":
            for package in range(1, 41):
                searchedPackage = packageHash.search(package)
                searchedPackage.status_update(deltaTimeConvert)
                print(str(searchedPackage))
        else:
            print("Invalid input, exiting...")
            exit()
    except ValueError:
        print("Entry invalid, make sure format is correct")
        exit()


# SOURCES CITED:
# Citing Source: W-3_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy_Dijkstra.py
# Citing Source: "Python: Creating a HASHMAP using Lists" by Oggi AI - Artificial Intelligence Today
# Citing Source: WGU Zybooks: "C949: Data Structures and Algorithms I" Figure 15.10.2
