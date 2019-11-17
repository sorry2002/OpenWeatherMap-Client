"""
A command-line based client for the OpenWeatherMap API.
 python weather.py -k key.txt
"""
import json, requests, pprint, colorama, sys, time, datetime, weather, argparse
import smtplib, ssl
import getpass
import os


url = "http://api.openweathermap.org/data/2.5/weather?"
url_forecast = "http://api.openweathermap.org/data/2.5/forecast?"

def get_URL(Id, url, key):
    """
    Joins Id, url and key to a complete url in order to access the API

    Id: id of the desirec city
    url: Either the forecast or current weather url
    key: Key to access the API
    """
    complete_url = str(url) + "appid=" + str(key) + "&id=" + str(Id)
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
        if str(city).lower() == e['name'].lower() and len(l)<100:
            l.append(e)
        elif str(city).lower() in e['name'].lower()[:len(city):] and len(l)<100:
            l.append(e)
        # Returns a list of hits for search quary
        # e.g. [{ "id": 628281,    "name": "Homyel’skaya Voblasts’",    "country": "BY",    "coord": {      "lon": 30,      "lat": 52}]
    return l

    """
def get_Data(complete_url):
    Returns a dict using the requests module.

    complete_url: the complete url to either access the forecast or current weather API
    """
    return requests.get(complete_url).json()

def validate_key(key, url):
    """
    Validates the parsed API-Key.
    """
    complete_url = get_URL(search("Berlin")[0]["id"], url, key)
    
    data = get_Data(complete_url)
    
    if data['cod'] == 401:
        # Print error message
        print(colorama.Fore.RED, data['message'])
        return False
    else:
        return True        

def print_current_Weather(Id, url, key):
    """
    Prints multiple lines containing the current weather of a given city.

    Id: id of the desired city
    url: url to access the OpenWeatherMap current weather API. Doc: https://openweathermap.org/current
    key: Key to access the OpenWeatherMap API
    """
    data = get_Data(get_URL(str(Id), url, key))
    s = (f"[+] Weather in {data['name']}, {data['sys']['country']}:\n"
        f"[+] Date:             {time.ctime(data['dt'])}\n"
        f"[+] Description:      {data['weather'][0]['description']}\n"
        f"[+] Temperature:      {data['main']['temp']} K° / {round(data['main']['temp'] - 273.15, 2)} C°\n"
        f"[+] Max. Temperature: {data['main']['temp_max']} K° / {round(data['main']['temp_max'] - 273.15, 2)} C°\n"
        f"[+] Min. Temperature: {data['main']['temp_min']} K° / {round(data['main']['temp_min'] - 273.15, 2)} C°\n"
        f"[+] Pressure:         {data['main']['pressure']} hPa / {round(data['main']['pressure'] / 1000, 2)} Bar\n"
        f"[+] Humidity:         {data['main']['humidity']} %\n"
        f"[+] Windspeed:        {data['wind']['speed']} m/s / {round(data['wind']['speed'] * 3.6, 2)} km/h\n"
        f"[+] Cloudiness:       {data['clouds']['all']} %")
    print(colorama.Fore.WHITE + "\n" + s)
    
def send_current_Weather(Id, url, key, contact):
    """
    Id: id of the desired city
    url: url to access the OpenWeatherMap current weather API. Doc: https://openweathermap.org/current
    key: Key to access the OpenWeatherMap API
    contact: if exists, send an e-mail temp, pressure, humidity
    """
    data = get_Data(get_URL(str(Id), url, key))
    # s = (f"[+] Weather in {data['name']}, {data['sys']['country']}:\n"
    #     f"[+] Date:             {time.ctime(data['dt'])}\n"
    #     f"[+] Description:      {data['weather'][0]['description']}\n"
    #     f"[+] Temperature:      {data['main']['temp']} K° / {round(data['main']['temp'] - 273.15, 2)} C°\n"
    #     f"[+] Max. Temperature: {data['main']['temp_max']} K° / {round(data['main']['temp_max'] - 273.15, 2)} C°\n"
    #     f"[+] Min. Temperature: {data['main']['temp_min']} K° / {round(data['main']['temp_min'] - 273.15, 2)} C°\n"
    #     f"[+] Pressure:         {data['main']['pressure']} hPa / {round(data['main']['pressure'] / 1000, 2)} Bar\n"
    #     f"[+] Humidity:         {data['main']['humidity']} %\n"
    #     f"[+] Windspeed:        {data['wind']['speed']} m/s / {round(data['wind']['speed'] * 3.6, 2)} km/h\n"
    #     f"[+] Cloudiness:       {data['clouds']['all']} %")
    # print(colorama.Fore.WHITE + "\n" + s)
    
    print(env_utils.get_env('GMAIL_USER'))  #=> sradevops@gmail.com
    print(env_utils.get_env('GMAIL_PASSWORD'))
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = env_utils.get_env('GMAIL_USER')
    password = env_utils.get_env('GMAIL_PASSWORD')
    #receiver_email = "sradevops@gmail.com"
    receiver_email = emails

    message = """\
    Subject: Weather from command-line based client for the OpenWeatherMap API
    Weather in {}, 
    Temperature: {}, 
    Pressure: {}, 
    Humidity: {} """.format('name', 'temp', 'pressure', 'humidity')

    context = ssl._create_unverified_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

def print_forecast(Id, url_forecast, key):
    """
    Prints multiple lines containing the forecast for a given city.

    Id: id of the desired city
    url_forecast: url to access the OpenWeatherMap forecast API. Doc: https://openweathermap.org/forecast5
    key: Key to access the OpenWeatherMap API.
    """
    data = get_Data(get_URL(str(Id), url_forecast, key))
    print(colorama.Fore.WHITE)
    for i, e in enumerate(data['list']):
        if i == 0 and str(datetime.date.today()) in e['dt_txt']:
            print("\n[*] " + str(datetime.date.today()) + ":\n")
        if "00:00:00" in e['dt_txt']:
            print(f"[*] {str(e['dt_txt'])[:10:]}: \n")
        print(f"[+] {str(e['dt_txt'])[11::]}: {e['weather'][0]['description']} at {round(e['main']['temp'] - 273.15, 2)} °C \n", end = "")
        if "21:00:00" in e['dt_txt']:
            print("")

def main(url, url_forecast, key):
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
                print(colorama.Fore.WHITE)

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
                    if args.mail:
                        for contact in args.mail:
                            send_current_Weather(input("")[0]['id'], url, key, contact)
                    else:
                        try:
                                print_current_Weather(search(input("[City]: "))[0]['id'], url, key)
                        except (KeyError, IndexError) as err:
                                print(colorama.Fore.RED + "\n[-] Error: " + str(err) + ": invalid city")
            # Show forecast
            elif inpt == "3":
                try:
                    print_forecast(search(input("[City]: "))[0]['id'], url_forecast, key)
                except (KeyError, IndexError) as err:
                    print(colorama.Fore.RED + "\n[-] Error: " + str(err) + ": invalid city")
            # Exit
            elif inpt == "4":
                break
            else:
                print(colorama.Fore.RED + "\n[-] Error! Wrong Input!")
        except (ConnectionResetError, ConnectionAbortedError, ConnectionError, ConnectionRefusedError) as err:
            print(colorama.Fore.RED + "A connection error occured! Exiting!")
            break
        except KeyboardInterrupt as err:
            print(colorama.Fore.RED + "\nExiting!")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A command-line based client for the OpenWeatherMap API.")
    parser.add_argument("--key", "-k", help="API key for OpenWeatherMap or path to single line text file containing the key.")
    parser.add_argument("--mail", "-m", 
                        type=str, 
                        metavar='mail', 
                        help="Write e-mail to send an e-mail with current temperature, pressure, humidity to all recipients from emails list."
                        )
    parser.add_argument("--doc", help="Show Documentation", action="store_true")
    args = parser.parse_args()

    if args.doc:
        help(weather)
        
    elif args.mail:
        # emails = []
        #     for a_contact in args.mail:
        #     emails.append(a_contact.split(","))
        #     return emails

        print ("list mail to: "+ args.mail)
            
        [i 
        for x in args.mail.split(',') 
        if x 
        for i in x.split(' ') 
        if i]
                # ['mail@mail.com', 'mail92@mail.com', 'mail43@mail.com', 'mail34@mail.com']

        print ("list sending mail to: "+ args.mail)

    elif args.mail == None:
        # print weather data to console
        print ("print weather data to console: "+ args.mail)

    elif args.key == None:
        # Try to open key.txt for API-Key
        try:
            with open("".join(str(sys.path[0]) + "/key.txt"), "r") as file:
                main(url, url_forecast, file.read())
                file.close()
        except FileNotFoundError as err:
            print(colorama.Fore.RED + "[-] Error:", err)
            print(colorama.Fore.YELLOW + "Create a file called key.txt with your API-Key in the same directory or parse the key with --key or -r when executing.")
            print(colorama.Fore.WHITE)
            parser.print_help()
    elif args.key != None:
        if str(args.key).isalnum() and validate_key(args.key, url):
            main(url, url_forecast, args.key)
        else:
            # Try to open parsed key value as path to file
            try:
                with open(args.key, "r") as file:
                    main(url, url_forecast, file.read())
                    file.close()
            except:
                exit()