import requests
import json
import configparser
from datetime import date,timedelta,datetime

# Config File
config = configparser.ConfigParser()
config.read('config.cfg')


payload={}
headers = {}

url = config['URL']['urlAddress']
countries = [e.strip() for e in config.get('Countries', 'countryList').split(',')]

dataInsert = []

yesterday = date.today() - timedelta(days=1)
yesterday.strftime('%Y-%m-%d')


sDate = str(yesterday)
eDate = str(yesterday)

urlDynamic = url.replace("TAG_SDATE",sDate)
urlDynamic = urlDynamic.replace("TAG_EDATE",eDate)


for idx,c in enumerate(countries):
    
    if "TAG_COUNTRY" in urlDynamic:
        urlDynamic = urlDynamic.replace("TAG_COUNTRY", str(c))
    else:
        previousCountry = countries[idx-1]
        urlDynamic = urlDynamic.replace(previousCountry, str(c))
    
    # Getting the response 
    response = requests.request("GET", urlDynamic, headers=headers, data=payload)

    # Converting Response Text to a Dictionary
    response_dict = json.loads(response.text)

    # Printing only a few values
    row = {'Pais': response_dict[0]["country"], 'Casos': response_dict[0]["confirmed_daily"], 'Recuperados': response_dict[0]["recovered_daily"], 'Fallecidos': response_dict[0]["deaths_daily"] }
    dataInsert.append(row)

print(dataInsert)
