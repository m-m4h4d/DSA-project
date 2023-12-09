# ...

import dataclasses


run_this_cell = False
#  !pip install -U googlemaps
# !pip install substring

if run_this_cell == True:

    import googlemaps
    import pandas as pd
    import requests
    import numpy as np
    import re
    import substring

    # Replace this with your console.google.com API key
    key = "<PUT YOUR CONSOLE.GOOGLE.COM API KEY HERE>"

    # extract elevation float from the API data output string
    def extract_float_from_API_string(my):
        s1 = my
        s1 = s1[40:]
        s = substring.substringByChar(s1, startChar=":", endChar="\n")
        s = s.strip()
        s = re.sub(": ", "", s)
        s = re.sub(",", "", s)
        # print(float(s))
        return float(s)

    # set the url (must include long, lat, and user URL key)
    def get_elevation(lat, lon):
        url = ""
        url += "https://maps.googleapis.com/maps/api/elevation/json?locations="
        url += str(lat)
        url += "%2C"
        url += str(lon)
        url += "&key="
        url += key

        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        return extract_float_from_API_string(response.text)

    # ...

    # Replace the following code with your specific parameters
    area_wid = 26
    area_hei = 26
    lat_lon_increment_size = 0.003
    start_lat = 34.2822  # Replace with your desired start latitude
    start_lon = 118.5506  # Replace with your desired start longitude

    # ...

    # Save the generated elevation data to a CSV file
    f = open('mnist_train_small.csv', 'w')
    for item in dataclasses:
        for i in range(len(item)):
            if i == 0:
                f.write(str(item[i]))
            else:
                f.write(',' + str(item[i]))
        f.write('\n')
    f.close()