import json, requests, pprint, colorama, sys, time

colorama.init()


APIkey = "857c4d16c4f5b771c726a6a0e6f60f70"
url = "http://api.openweathermap.org/data/2.5/weather?"

def setCity(Id, url, APIkey):
    complete_url = url + "appid=" + APIkey + "&id=" + Id
    return complete_url

def search(city):
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
    return requests.get(complete_url).json()

def print_current_Weather(Id, url, APIkey):
    data = getData(setCity(str(Id), url, APIkey))
    s = (f"[+] Weather in {data['name']}, {data['sys']['country']}:\n"
        f"[+] Date:             {time.ctime(data['dt'])}\n"
        f"[+] Description:      {data['weather'][0]['description']}\n"
        f"[+] Temperature:      {data['main']['temp']} K° / {round(data['main']['temp'] - 273.15, 2)} C°\n"
        f"[+] Max. Temperature: {data['main']['temp_max']} K° / {round(data['main']['temp_max'] - 273.15, 2)} C°\n"
        f"[+] Min. Temperature: {data['main']['temp_min']} K° / {round(data['main']['temp_min'] - 273.15, 2)} C°\n"
        f"[+] Pressure:         {data['main']['pressure']} hPa / {round(data['main']['pressure'] / 1000, 2)} Bar\n"
        f"[+] Humidity:         {data['main']['humidity']} %\n"
        f"[+] Windspeed:        {data['wind']['speed']} m/s / {data['wind']['speed'] * 3.6} km/h\n"
        f"[+] Cloudiness:       {data['clouds']['all']} %\n")
    print("\n" + s)

def main(url, key):
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
    time.sleep(1)
    print("[*] Ready!", end = '\n \n')
    time.sleep(0.75)

    while True:
        print("\n[*] Options: \n[1] Search \n[2] Show current weather \n[3] Show forecast")
        inpt = input(":: ")

        # Search for a city
        if inpt == "1":
            print("")
            l = search(input("[City]: "))
            print("")
            print("[*] Results:")
            for i, e in enumerate(l, 1):
                print(f"[{i}] Name: {e['name']}, Country: {e['country']}, ID: {e['id']}")
            
            print("\n[*] Options:")
            print("[1] Show current weather \n[2] Show forecast \n[3] Exit to main menu")
            
            inpt = input(":: ")

            if inpt == "1":
                inpt = input("[City Number]: ")
                print("")
                print_current_Weather(l[(int(inpt) - 1)]['id'], url, key)
            elif inpt == "2":
                pass
            else:
                continue
        # Show current weather
        elif inpt == "2":
            print_current_Weather(search(input("[City]: "))[0]['id'], url, key)



if __name__ == "__main__":
    main(url, APIkey)