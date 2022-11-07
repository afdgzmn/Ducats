import urllib.parse
import requests
from prettytable import PrettyTable
from colorama import Fore, Style
from collections import defaultdict
from collections import *

def menu():
    print(Fore.RED) # set foreground color to red
    print ("[1] Enter Location")
    print ("[2] View previously inputted locations")
    print ("[3] View most visited locations")
    print ("[4] View least visited locations")
    print ("[5] Exit")

def prev(location_lst): 
    if (len(location_lst) == 0):
        print("No locations entered yet")
    else:
        print(Fore.YELLOW) # set foreground color to yellow

        #removed the duplicates without having to keep track of the elements’ indices
        for location in location_lst: 
            if location not in newloc_lst:
                newloc_lst.append(location)
        
        #display in a numbering format the inputted locations
        for x, y in enumerate(newloc_lst, 1):
            print (" ", '{}  {}'.format(x, y))

        print("\nTotal Inputs:", len(location_lst)) #displays the total inputted locations

def get_locations(a, setting):
    compare = []
    location_list = []
    if setting == 0:
        compare = min(a.items(), key=lambda x: x[1])
    else:
        compare = max(a.items(), key=lambda x: x[1])

    for key, value in a.items():
        if compare[1] == value:
            location_list.append(key)

    return location_list

def most_visited(location_lst):
    if (len(location_lst) == 0):
        print("No locations entered yet")
    else:
        print(Fore.CYAN) # set foreground color to cyan

        temp = defaultdict(int)

        # determine least visited location
        for sub in location_lst:
            temp[sub] += 1

        least_visited_places = get_locations(temp, 1)

        # build string
        places_string = ""
        for index, item in enumerate(least_visited_places):
            if index != len(least_visited_places) - 1:
                places_string += item + ", "
            else:
                places_string += item

        if len(least_visited_places) > 1:
            print("Most Visited Locations are: " + places_string)
        else:
            print("Most Visited Location is: " + places_string)

        dup = {}

        for x in location_lst:
            if location_lst.count(x) > 0:
                dup[x] = dup.get(x, 0) + 1

        print("%s%s" % (dup, ' visit/s'))

def least_visited(location_lst):
    if (len(location_lst) == 0):
        print("No locations entered yet")
    else:
        print(Fore.GREEN) # set foreground color to green

        temp = defaultdict(int)

        # determine most visited location
        for sub in location_lst:
            temp[sub] += 1

        most_visited_places = get_locations(temp, 0)

        # build string
        places_string = ""
        for index, item in enumerate(most_visited_places):
            if index != len(most_visited_places) - 1:
                places_string += item + ", "
            else:
                places_string += item

        if len(most_visited_places) > 1:
            print("Least Visited Locations are: " + places_string)
        else:
            print("Least Visited Location is: " + places_string)
        
        dup = {}

        for x in location_lst:
            if location_lst.count(x) > 0:
                dup[x] = dup.get(x, 0) + 1

        print("%s%s" % (dup, ' visit/s'))

def location(location_lst):
    main_api = "https://www.mapquestapi.com/directions/v2/route?"
    key = "EbqeMzFFrxwHw0nrQeV4ApcIxfWAfCd4"
        
    while True:
        print(Fore.YELLOW) # set foreground color to yellow
        orig = input("Starting location: ")
        if orig.lower() == "quit" or orig.lower() == "q":
            print(Style.RESET_ALL) # remove style
            break

        dest = input("Destination: ")
        if dest.lower() == "quit" or dest.lower() == "q":
            print(Style.RESET_ALL) # remove style
            break

        # destination is location to be visited
        # append destination only after validating input is not quit
        # format string to title case
        location_lst.append(dest.title())

        url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
        print("URL: " + (url))

        json_data = requests.get(url).json()
        json_status = json_data["info"]["statuscode"]

        if json_status == 0:
            print(Fore.GREEN) # set foreground color to green, green denotes success
            print("API Status: " + str(json_status) + " = A successful route call.")

            tripInfo = PrettyTable()
            tripInfo.header = False # no header
            tripInfo.add_row(["Trip Duration", json_data["route"]["formattedTime"]])
            tripInfo.add_row(["Miles", str("{:.2f}".format(json_data["route"]["distance"]))])
            tripInfo.add_row(["Kilometers", str("{:.2f}".format((json_data["route"]["distance"]) * 1.61))])
            tripInfo.add_row(["Fuel Used (Ltr)", str("{:.2f}".format((json_data["route"][f"fuelUsed"]) * 3.78))])

            tripInfo.align = "l" # left align
            print(Fore.MAGENTA) # set foreground color to magenta
            print(tripInfo)

            directions = PrettyTable()
            directions.field_names = ["Directions from " + orig + " to " + dest]

            for direction in json_data["route"]["legs"][0]["maneuvers"]:
                data = direction["narrative"] + " (" + str("{:.2f}".format((direction["distance"]) * 1.61) + " km)")
                directions.add_row([data])

            directions.align = "l" # left align
            print(Fore.CYAN) # set foreground color to cyan
            print(directions)
                
        elif json_status == 402:
            print(Fore.RED) # set foreground color to red, red denotes error
            print("\n**********************************************")
            print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
            print("**********************************************\n")
                
        elif json_status == 611:
            print(Fore.RED) # set foreground color to red, red denotes error
            print("\n**********************************************")
            print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
            print("**********************************************\n")
            
        else:
            print(Fore.RED) # set foreground color to red, red denotes error
            print("\n**********************************************")
            print("For Status Code: " + str(json_status) + "; Refer to:")
            print("https://developer.mapquest.com/documentation/directions-api/status-codes")
            print("**********************************************\n")

        print(Style.RESET_ALL) # remove style

if __name__ == "__main__":
    location_lst = [] 
    newloc_lst = [] 

    while True:
        menu()
        option = input("Enter your option: ")

        if option == "1":
            #Enter location option
            location(location_lst)
            print(Style.RESET_ALL) # remove style
            
        elif option == "2":
            #View previously inputted locations
            prev(location_lst)
            print(Style.RESET_ALL) # remove style
            
        elif option == "3":
            #View most visited locations
            most_visited(location_lst)
            print(Style.RESET_ALL) # remove style

        elif option == "4":
            #View least visited locations
            least_visited(location_lst)
            print(Style.RESET_ALL) # remove style

        else:
            print("\n\nThank you for using the program!")
            print("Have a safe trip!")
            print(Style.RESET_ALL) # remove style
            break