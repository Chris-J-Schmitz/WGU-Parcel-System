# Author: Chris Schmitz / Student ID : 001366917
# WGU C950 

#import
import csv
import datetime




#Loading the CSV files for addressess and distances
with open("addressess.csv") as addyCSV:
    AddressCSV = csv.reader(addyCSV)
    AddressCSV = list(AddressCSV)
with open("distances.csv") as disCSV:
    DistanceCSV = csv.reader(disCSV)
    DistanceCSV = list(DistanceCSV)   



#Crete all classes

#Creating the hash table
class HashTable:
    def __init__(self, initialcapacity=40):
        self.table = []
        for i in range(initialcapacity):
            self.table.append([])

    #Inserts a new item into the hash table and will update an item in the list already
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        #if not in the bucket, insert item to the end of the list    
        key_value = [key, item]
        bucket_list.append(key_value)
        return True
    #Searches the hash table for an item with the matching key
    #Will return the item if founcd, or None if not found
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # Search key in bucket
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]  # Value
        return None
        
    #Removes an item with matching key from the hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #removes the item if it is present
        if key in bucket_list:
            bucket_list.remove(key)

#Creating package class to store package info
class Packages:
    def __init__(self, ID, street, city, state, zip,deadline,weight, status,departureTime,deliveryTime):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departureTime = None #departureTime
        self.deliveryTime = None #deliveryTime

    def __str__(self):
        return "ID: %s, %-20s, %s, %s,%s, Deadline: %s,%s,%s,Departure Time: %s,Delivery Time: %s" % (self.ID, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status, self.departureTime, self.deliveryTime)   
    #Updates the status of a package 
    def statusUpdate(self, timeChange):
        if self.deliveryTime == None:
            self.status = "At the hub"
        elif timeChange < self.departureTime:
            self.status = "At the hub"   
        elif timeChange < self.deliveryTime:
            self.status = "En route"     
        else:
            self.status = "Delivered" 
        #will change the address for package 9 to the correct address once it's been received
        if self.ID == 9: 
            if timeChange > datetime.timedelta (hours=10, minutes= 20):
                self.street = "410 S State St"  
                self.zip = "84111"  
            else:
                self.street = "300 State St"
                self.zip = "84103"     

#Creating the trucks
class Trucks:
    def __init__(self, speed, miles, currentLocation, departTime, packages):
        self.speed = speed
        self.miles = miles
        self.currentLocation = currentLocation
        self.time = departTime
        self.departTime = departTime
        self.packages = packages

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self.speed, self.miles, self.currentLocation, self.time, self.departTime, self.packages)

#All Classes Created


#Creating the Packages with info from the CSV to go into the Hash Table
def loadPackageData(filename, packageHash):
    with open(filename) as package_info:
        packageData = csv.reader(package_info)
        for package in packageData:
            pID = int(package[0])
            pStreet = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "At Hub" #Default status
            pDepartureTime = None #Assigned once packaage departs
            pDeliveryTime = None #Assigned once packaage is delivered 

            #Creates package with the package info
            p = Packages(pID, pStreet, pCity, pState, pZip, pDeadline, pWeight, pStatus, pDepartureTime, pDeliveryTime)
            #Inserting Package into the hash table
            packageHash.insert(pID, p)

#Hash table for the packages
packageHash = HashTable() 


#pulls data from CSV into the function
loadPackageData('packages.csv',packageHash)



#manually loading the trucks and assigning them a departure time
truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),[1,13,14,15,16,19,20,29,30,31,34,37,40]) #All packages that must be delivered either together or before 10:30AM
truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=10),[3,18,6,25,28,32,8,10,11,12,17,21,22,23]) #
truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),[2,4,5,7,9,26,33,35,36,38,39,24,27]) 

#finds the minimum distance for the next address
def minAddress(address):
    for row in AddressCSV:
        if address in row[2]:
           return int(row[0])


#finds the distance between two addresses
def distanceBetween(address1,address2):
    distance = DistanceCSV[address1][address2]
    if distance == '':
        distance = DistanceCSV[address2][address1]
    return float(distance)




#algorithm to deliver the packages on the truck
def deliverPackages(truck):
    
    #Creates a list of packages
    enroute = [packageHash.search(packageID) for packageID in truck.packages]

    truck.packages.clear()

    #while there are still packages to deliver
    while len(enroute) > 0:
        #Arbitrary number to ensure the next address will be a shorter distance
        nextAddress = 1000
        nextPackage = None
        
        for package in enroute:
            if package is None:
                
                continue
            #Ensures that these delayed packages meet the delivery deadline 
            if package.ID in [25, 6]:
                nextPackage = package
                nextAddress = distanceBetween(minAddress(truck.currentLocation), minAddress(package.street))
                break
            
            distance = distanceBetween(minAddress(truck.currentLocation), minAddress(package.street))
            if distance <= nextAddress:
                nextAddress = distance
                nextPackage = package
        
        if nextPackage is None:
            break
        

        #updates truck values and removes the now delivered package
        truck.packages.append(nextPackage.ID)    
        enroute.remove(nextPackage)
        truck.miles += nextAddress
        truck.currentLocation = nextPackage.street
        truck.time += datetime.timedelta(hours=nextAddress / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departTime


        


#Begin delivering packages
deliverPackages(truck1)
deliverPackages(truck2)
#Ensures truck 3 won't leave until either truck 1 or 2 have returned
truck3.departTime = min(truck1.time, truck2.time)
deliverPackages(truck3)

#title
print("WGU Parcel System")
#total miles for all of the trucks
print ("The overall miles are:", (truck1.miles + truck2.miles + truck3.miles))


#UI
while True:
    userTime = input("Please enter a time for which you'd like to see the status of each package. Format: HH:MM. ")

    # Check if the input contains exactly one colon
    if userTime.count(':') != 1:
        print("Please enter the time in the correct format (HH:MM).")
        continue

    try:
        (h, m) = userTime.split(":")
        timeChange = datetime.timedelta(hours=int(h), minutes=int(m))
    except ValueError:
        print("Invalid time format. Please enter the time in the correct format (HH:MM).")
        continue

    try:
        userInput = input("Enter the Package ID or nothing at all: ")
        if userInput.strip() == '':
            userInput = range(1, 41)
        else:
            userInput = [int(userInput)]
    except ValueError:
        print("Invalid input. Please enter a valid Package ID or nothing at all.")

    for packageID in userInput:
        package = packageHash.search(packageID)
        if package is None:
            print(f"No package found for ID: {packageID}")
        else:
            package.statusUpdate(timeChange)
            # Check if the package is delivered after the specified time
            if package.deliveryTime is None:
                print(f"Package ID: {package.ID: <2}, Status: {package.status}, Delivery Time: TBD")
            elif package.deliveryTime <= timeChange:
                print(str(package))
            else:
                print(f"Package ID: {package.ID: <2}, Status: {package.status}, Delivery Time: TBD")
 
