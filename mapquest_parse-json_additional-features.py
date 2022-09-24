import urllib.parse
import requests
from prettytable import PrettyTable
from colorama import Fore, Style

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "Vw8zXGTGIhSt3hJXReSHkupRk9nwVlZc"

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
        print(Style.RESET_ALL) # remove style
        
    elif json_status == 402:
        print(Fore.RED) # set foreground color to red, red denotes error
        print("\n**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
        print(Style.RESET_ALL) # remove style
        
    elif json_status == 611:
        print(Fore.RED) # set foreground color to red, red denotes error
        print("\n**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")
        print(Style.RESET_ALL) # remove style
        
    else:
        print(Fore.RED) # set foreground color to red, red denotes error
        print("\n**********************************************")
        print("For Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("**********************************************\n")
        print(Style.RESET_ALL) # remove style