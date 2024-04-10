from django.core.management.base import BaseCommand, CommandError
import requests
import googlemaps
import csv
import itertools
import responses
class Command(BaseCommand):
        # remplir avec votre clé API Google Maps
        API_KEY='AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk'
        gmaps = googlemaps.Client(key='AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk')
        csv_file_path ='Fakedata.csv'
        #def add_arguments(self, parser):
        #    parser.add_argument(csv_file_path, type=str, help='Path to the CSV file')
        
        def handle(self,*args,**kwargs):
            # remplir avec votre clé API Google Maps
            gmaps = googlemaps.Client(key='AIzaSyBawSSjukicDdh7sfbVcToVktSypmWwQmk')

            def read_line_csv(csv_file_path, begin, end ):
                with open(csv_file_path, 'r', newline='', encoding='ISO-8859-1') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    for _ in range(begin):
                        next(reader)
                    return list(itertools.islice(reader, end-begin))
            for line in range(0, 903, 100):
                part = read_line_csv(self.csv_file_path, line, line+100)
                print('***************************************************************')
                for i in range(0,100):
                    name_camping = part[i]["camping"].split(sep='/')[0]
                    camping_postal_adress = part[i]["camping"].split(sep='/')[1]
                    country_camping = part[i]["camping"].split(sep='/')[3]
                    country_client = part[i]["Country"]
                    city = part[i]["City"].split(sep=" ")[0]
                    year = part[i]["Year"]
                    transport = part[i]["Transport"]
                    print()
        # directions_result = gmaps.directions("Sydney Town Hall",
        #                                     "Parramatta, NSW",
        #                                     mode="driving",)
        #stock la distance dans une variable.
        # distance = directions_result[0]['legs'][0]['distance']['text']

    # def geolocalisation():
    #     city = 'london'
    #     api_url = 'https://api.api-ninjas.com/v1/geocoding?city='+city+''
    #     response = requests.get(api_url, headers={'X-Api-Key': '9ZhwyUW2uIaDzkXe5sdiYHPxJLGnahYLWNwA6UdX'})
    #     if response.status_code == requests.codes.ok:
    #         print(response.text)
    #     else:
    #         print("Error:", response.status_code, response.text)
    #     return response.text

    # def calculDistance():
    #     url = "https://api.myptv.com/routing/v1/routes?waypoints="+response.text["latitude"]+"&waypoints="+response.text["longitude"]+"&options[trafficMode]=AVERAGE"
    #     headers = {
    #         'apiKey': "RVVfNGUyN2U1NmU1M2U2NDM1NzhkODRjNGVmMjhmMmIxYzI6ZDNjMTc1ZmEtMTI0OS00OTk4LWJmN2QtMjk5M2I2YmU2ZGQy"
    #     }
    #     response = requests.request("GET", url, headers=headers)
    #     print(response.text.encode('utf8'))
    
   
    # geolocalisation()
    # calculDistance()