"""
A command-line based client for the OpenWeatherMap API.
"""
import json, requests, pprint, colorama, sys, time, datetime, weather, argparse

url = "http://api.openweathermap.org/data/2.5/weather?"
url_forecast = "http://api.openweathermap.org/data/2.5/forecast?"

def getURL(Id, url, key):
    """
    Joins Id, url and key to a complete url in order to access the API

    Id: id of the desirec city
    url: Either the forecast or current weather url
    key: Key to access the API
    """
    complete_url = url + "appid=" + key + "&id=" + Id
    return complete_url

def search(city):
    """
    Reads the city.list.json file in the same directory and returns a list with all hits for a given city name which appears in the file.

    city: a string containing the desired city name
    """
    with open("".join(str(sys.path[0]) + "/city.list.json")) as file:
        data = json.load(file)

    l = []
    for e in data:
        try:
            if str(city).lower() == e['name'].lower():
                l.append(e)
        except TypeError:
            print("Invalid city name!")
            break
        # Returns a list of hits for search quary
        # e.g. [{'id': 2950159, 'name': 'Berlin', 'country': 'DE', 'coord': {'lon': 13.41053, 'lat': 52.524368}}]
    return l

def getData(complete_url):
    """
    Returns a dict using the requests module.

    complete_url: the complete url to either access the forecast or current weather API
    """
    return requests.get(complete_url).json()
    

def print_current_Weather(Id, url, key):
    """
    Prints multiple lines containing the current weather of a given city.

    Id: id of the desired city
    url: url to access the OpenWeatherMap current weather API. Doc: https://openweathermap.org/current 
    key: Key to access the OpenWeatherMap API
    """
    data = getData(getURL(str(Id), url, key))
    s = (f"[+] Weather in {data['name']}, {data['sys']['country']}:\n"
        f"[+] Date:             {time.ctime(data['dt'])}\n"
        f"[+] Description:      {data['weather'][0]['description']}\n"
        f"[+] Temperature:      {data['main']['temp']} K° / {round(data['main']['temp'] - 273.15, 2)} C°\n"
        f"[+] Max. Temperature: {data['main']['temp_max']} K° / {round(data['main']['temp_max'] - 273.15, 2)} C°\n"
        f"[+] Min. Temperature: {data['main']['temp_min']} K° / {round(data['main']['temp_min'] - 273.15, 2)} C°\n"
        f"[+] Pressure:         {data['main']['pressure']} hPa / {round(data['main']['pressure'] / 1000, 2)} Bar\n"
        f"[+] Humidity:         {data['main']['humidity']} %\n"
        f"[+] Windspeed:        {data['wind']['speed']} m/s / {data['wind']['speed'] * 3.6} km/h\n"
        f"[+] Cloudiness:       {data['clouds']['all']} %")
    print(colorama.Fore.WHITE + s)

def print_forecast(Id, url_forecast, key):
    """
    Prints multiple lines containing the forecast for a given city.

    Id: id of the desired city
    url_forecast: url to access the OpenWeatherMap forecast API. Doc: https://openweathermap.org/forecast5
    key: Key to access the OpenWeatherMap API.
    """
    data = getData(getURL(str(Id), url_forecast, key))
    print(colorama.Fore.WHITE)
    for i, e in enumerate(data['list']):
        if i == 0:
            print("\n" + str(datetime.date.today()) + ":\n")
        if "00:00:00" in e['dt_txt']:
            print(f"{str(e['dt_txt'])[:10:]}: \n")
        print(f"{str(e['dt_txt'])[11::]}: {e['weather'][0]['description']} at {round(e['main']['temp'] - 273.15, 2)} °C \n", end = "")
        if "21:00:00" in e['dt_txt']:
            print("")

def main(url, url_forecast, key):
    # Initializing colorama to output coloured text
    colorama.init()
    print(colorama.Fore.YELLOW,r"""                
                        |
                    .   |
                        |
          \    *        |     *    .  /
            \        *  |  .        /
         .    \     ___---___     /    .  
                \.--         --./     
     ~-_    *  ./               \.   *   _-~
        ~-_   /                   \   _-~     *
   *       ~-/                     \-~          
     .      |                       |      .     
         * |                         | *          
-----------|  OpenWeatherMap Client  |----------- 
  .        |                         |        .  
        *   |                       | *
           _-\                     /-_    *
     .  _-~ . \                   /   ~-_     
     _-~       `\               /'*      ~-_  
    ~           /`--___   ___--'\           ~
           *  /        ---     .  \   
            /     *     |           \
          /             |   *         \
                     .  |        .
                        |
                        |""")
    print(colorama.Fore.GREEN + "[*] Starting up...")
    time.sleep(0.5)
    print("[*] Ready!", end = '\n \n')
    time.sleep(0.5)

    while True:
        try:
            print(f"{colorama.Fore.GREEN}\n[*] Options: \n[1] Search \n[2] Show current weather \n[3] Show forecast \n[4] Exit")
            inpt = input(":: ")

            # Search for a city
            if inpt == "1":
                print("")
                l = search(input("[City]: "))
                print("")

                # Print the results for the search query
                print("[*] Results:")
                for i, e in enumerate(l, 1):
                    print(f"[{i}] Name: {e['name']}, Country: {e['country']}, ID: {e['id']}")

                # Prints to result if the returned list is empty and coninues the loop
                if l == []:
                    print(colorama.Fore.RED + "[-] No Results!")
                    continue

                print(colorama.Fore.GREEN + "\n[*] Options:")
                print("[1] Show current weather \n[2] Show forecast \n[3] Exit to main menu")
                
                inpt = input(":: ")

                # Show current weather
                if inpt == "1":
                    inpt = input("[City Number]: ")
                    print("")
                    print_current_Weather(l[(int(inpt) - 1)]['id'], url, key)
                    print(colorama.Fore.GREEN)
                # Show forecast
                elif inpt == "2":
                    inpt = input("[City Number]: ")
                    print("")
                    print_forecast(l[int(inpt) - 1]['id'], url_forecast, key)
                    print(colorama.Fore.GREEN)
                # Exit to main menu
                else:
                    continue
            # Show current weather
            elif inpt == "2":
                print_current_Weather(search(input("[City]: "))[0]['id'], url, key)
                print(colorama.Fore.GREEN)
            # Show forecast
            elif inpt == "3":
                print_forecast(search(input("[City]: "))[0]['id'], url_forecast, key)
                print(colorama.Fore.GREEN)
            # Exit
            elif inpt == "4":
                break
            else:
                print(colorama.Fore.RED + "\n[-] Error! Wrong Input!")
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except ConnectionResetError:
            print(colorama.Fore.RED + "ConnectionResetError! Please try again.")
            continue
        except ConnectionAbortedError:
            print(colorama.Fore.RED + "ConncectionAbortedError! Please try again.")
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "A command-line based client for the OpenWeatherMap API.")
    
    parser.add_argument("--key", "-k", help = "API key for OpenWeatherMap")
    parser.add_argument("--doc", help = "Show Documentation", action = "store_true")
    
    args = parser.parse_args()
    
    if args.doc:
        help(weather)
    else:
        main(url, url_forecast, args.key)